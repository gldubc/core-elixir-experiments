#!/usr/bin/env python3
import argparse
import csv
import subprocess
import os
import signal
import sys
import datetime
import json
import math
import re
import shutil
import statistics
import threading
from pathlib import Path

# Configuration
DEFAULT_ELIXIR_ROOT = Path(__file__).resolve().parents[1] / "main"
ELIXIR_PATH = DEFAULT_ELIXIR_ROOT / "bin"
ELIXIR_EXECUTABLE = ELIXIR_PATH / "elixir"
MIX_PATH = ELIXIR_PATH / "mix"
os.environ["PATH"] = f"{ELIXIR_PATH}:{os.environ['PATH']}"

SCRIPT_DIR = Path(__file__).resolve().parent
MAIN_REPOS_DIR = SCRIPT_DIR / "repos"
WORKTREE_REPOS_DIR = SCRIPT_DIR / "repos-worktrees"
MONTHLY_CLEAN_MARKER = ".perf-last-clean-month"
MONTHLY_CLEAN_PATHS = ("_build", "deps")

REPOSITORY_SPECS = [
    {
        "name": "HexPm",
        "dir": "hexpm",
        "url": "https://github.com/hexpm/hexpm.git",
    },
    {
        "name": "Phoenix",
        "dir": "phoenix",
        "url": "https://github.com/phoenixframework/phoenix.git",
    },
    {
        "name": "PhoenixLiveView",
        "dir": "phoenix_live_view",
        "url": "https://github.com/phoenixframework/phoenix_live_view.git",
    },
    {
        "name": "Livebook",
        "dir": "livebook",
        "url": "https://github.com/livebook-dev/livebook.git",
    },
    {
        "name": "Credo",
        "dir": "credo",
        "url": "https://github.com/rrrene/credo.git",
    },
    {
        "name": "ExDoc",
        "dir": "ex_doc",
        "url": "https://github.com/elixir-lang/ex_doc.git",
    },
    {
        "name": "Nerves",
        "dir": "nerves",
        "url": "https://github.com/nerves-project/nerves.git",
    },
    {
        "name": "Ecto",
        "dir": "ecto",
        "url": "https://github.com/elixir-ecto/ecto.git",
    },
    {
        "name": "Postgrex",
        "dir": "postgrex",
        "url": "https://github.com/elixir-ecto/postgrex.git",
    },
    {
        "name": "Flame",
        "dir": "flame",
        "url": "https://github.com/phoenixframework/flame.git",
    },
    {
        "name": "Ash",
        "dir": "ash",
        "url": "https://github.com/ash-project/ash.git",
    },
    {
        "name": "Spitfire",
        "dir": "spitfire",
        "url": "https://github.com/elixir-tools/spitfire.git",
    },
    {
        "name": "SQL",
        "dir": "sql",
        "url": "https://github.com/elixir-dbvisor/sql.git",
    },
    {
        "name": "OpenApiSpex",
        "dir": "open_api_spex",
        "url": "https://github.com/open-api-spex/open_api_spex.git",
    },
    {
        "name": "MixSBOM",
        "dir": "mix_sbom",
        "url": "https://github.com/erlef/mix_sbom.git",
    },
    {
        "name": "AbsintheFederation",
        "dir": "absinthe_federation",
        "url": "https://github.com/DivvyPayHQ/absinthe_federation.git",
    },
    {
        "name": "Blockscout",
        "dir": "blockscout",
        "url": "https://github.com/blockscout/blockscout.git",
    },
]

REPO_NAMES = [repo["name"] for repo in REPOSITORY_SPECS]
DEFAULT_REPO_NAMES = [repo["name"] for repo in REPOSITORY_SPECS if repo.get("default", True)]
RESULTS_DIR = Path("results")
SERIOUS_RUN_DEFAULT_RUNS = 10
SERIOUS_RUN_DEFAULT_WARMUPS = 2
DEFAULT_COMPILE_TIMEOUT_SECONDS = 15
DEFAULT_DEPS_COMPILE_TIMEOUT_SECONDS = DEFAULT_COMPILE_TIMEOUT_SECONDS * 20
COMPILE_TIMEOUT_RETURNCODE = 124
EZSTD_BUILD_DEPS_PATH = Path("deps") / "ezstd" / "build_deps.sh"
EZSTD_ZSTD_RELATIVE_DIR = Path("deps") / "ezstd" / "_build" / "deps" / "zstd"
EZSTD_ZSTD_SUCCESS_FILE = Path("lib") / "libzstd.a"
TYPE_WARNING_COUNT_MARKER = "__EPT_TYPE_WARNING_COUNT__="
TYPE_WARNING_COUNTER_CODE = r"""
Mix.start()

defmodule EPT.TypeWarningCounter do
  def count do
    Mix.Project.in_project(:ept_type_warning_counter, File.cwd!(), fn _ ->
      diagnostics_for_project()
      |> Enum.count(&type_warning?/1)
    end)
  end

  defp diagnostics_for_project do
    case Mix.Project.apps_paths() do
      nil ->
        Mix.Tasks.Compile.Elixir.diagnostics()

      apps ->
        apps
        |> Enum.sort_by(fn {app, _path} -> app end)
        |> Enum.flat_map(fn {app, path} ->
          Mix.Project.in_project(app, path, fn _ -> diagnostics_for_project() end)
        end)
    end
  end

  defp type_warning?(%{severity: :warning, details: %{typing_traces: _}}), do: true
  defp type_warning?(_), do: false
end

IO.puts("__EPT_TYPE_WARNING_COUNT__=#{EPT.TypeWarningCounter.count()}")
"""


def configure_elixir_bin(bin_dir):
    global ELIXIR_PATH, ELIXIR_EXECUTABLE, MIX_PATH
    ELIXIR_PATH = bin_dir
    ELIXIR_EXECUTABLE = ELIXIR_PATH / "elixir"
    MIX_PATH = ELIXIR_PATH / "mix"

    # Put the selected toolchain first in PATH, without duplicate entries.
    existing = [p for p in os.environ.get("PATH", "").split(os.pathsep) if p]
    bin_dir_str = str(ELIXIR_PATH)
    existing = [p for p in existing if p != bin_dir_str]
    os.environ["PATH"] = os.pathsep.join([bin_dir_str] + existing)


def run(cmd, cwd=None, capture=False):
    """Run shell command safely."""
    if capture:
        return subprocess.run(cmd, cwd=cwd, shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True).stdout.strip()
    else:
        subprocess.run(cmd, cwd=cwd, shell=True, check=False)


def git_command(repo_path, cmd):
    return subprocess.run(
        cmd,
        cwd=repo_path,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )


def git_command_args(repo_path, args):
    return subprocess.run(
        ["git", *args],
        cwd=repo_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def process_streams(result):
    return "\n".join(
        stream.strip()
        for stream in [result.stdout, result.stderr]
        if stream and stream.strip()
    )


def print_process_streams(result):
    output = process_streams(result)
    if output:
        print(output)


def run_deps_get(repo_path):
    return subprocess.run(
        [str(MIX_PATH), "deps.get"],
        cwd=repo_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


def hex_archive_requirement_mismatch(output):
    return 'Archive "hex-' in output and "does not match requirement" in output


def update_local_hex_archive(repo_path, status):
    result = subprocess.run(
        [str(MIX_PATH), "local.hex", "--force"],
        cwd=repo_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    output = process_streams(result)
    if output:
        status(output)
    return result.returncode == 0


def build_repositories(repo_dir):
    repositories = []

    for repo in REPOSITORY_SPECS:
        checkout_path = repo_dir / repo["dir"]
        project_path = checkout_path / repo.get("mix_subdir", "")
        repositories.append({**repo, "checkout_path": checkout_path, "path": project_path})

    return repositories


def worktree_repo_slug(selected_elixir_root):
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", selected_elixir_root.name).strip("-")
    return slug or "worktree"


def worktree_repos_dir(selected_elixir_root):
    return SCRIPT_DIR / f"repos-{worktree_repo_slug(selected_elixir_root)}"


def repo_bucket_for_root(selected_elixir_root, requested_bucket):
    if requested_bucket == "main":
        return "main", MAIN_REPOS_DIR, None
    if requested_bucket == "worktrees":
        return "worktrees", WORKTREE_REPOS_DIR, MAIN_REPOS_DIR
    if requested_bucket == "shared":
        return "shared", MAIN_REPOS_DIR, None

    selected = selected_elixir_root.expanduser().resolve()
    main = DEFAULT_ELIXIR_ROOT.expanduser().resolve()
    if selected == main:
        return "main", MAIN_REPOS_DIR, None
    slug = worktree_repo_slug(selected)
    return f"worktree:{slug}", worktree_repos_dir(selected), MAIN_REPOS_DIR


def repo_head(repo_path):
    result = git_command_args(repo_path, ["rev-parse", "HEAD"])
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def repo_has_tracked_changes(repo_path):
    result = git_command_args(repo_path, ["status", "--porcelain", "--untracked-files=no"])
    return result.returncode != 0 or bool(result.stdout.strip())


def deps_get(repo_path, repo_name, status):
    status(f"Fetching dependencies for {repo_name} in {repo_path}")
    result = run_deps_get(repo_path)
    output = process_streams(result)
    if result.returncode != 0 and hex_archive_requirement_mismatch(output):
        status("Hex archive does not match the project requirement; updating Hex and retrying deps.get.")
        if update_local_hex_archive(repo_path, status):
            result = run_deps_get(repo_path)
            output = process_streams(result)

    if result.returncode != 0:
        status(f"Failed to fetch dependencies for {repo_name}.")
        if output:
            status(output)
        return False, f"deps.get failed (exit {result.returncode})"
    return True, None


def deps_compile(repo_path, repo_name, status, compile_timeout=DEFAULT_DEPS_COMPILE_TIMEOUT_SECONDS):
    status(f"Compiling dependencies for {repo_name} in {repo_path}")
    timed_out = False
    with subprocess.Popen(
        [str(MIX_PATH), "deps.compile", "--force"],
        cwd=repo_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        start_new_session=True,
    ) as proc:
        try:
            output, _ = proc.communicate(timeout=compile_timeout)
            returncode = proc.returncode
        except subprocess.TimeoutExpired:
            timed_out = True
            stop_compile_process(proc)
            output, _ = proc.communicate()
            returncode = COMPILE_TIMEOUT_RETURNCODE

    if timed_out:
        status(
            f"Timed out compiling dependencies for {repo_name} "
            f"after {format_seconds(compile_timeout)} seconds."
        )
        if output:
            status(output.strip())
        return False, f"deps compile timeout after {format_seconds(compile_timeout)} s"

    if returncode != 0:
        status(f"Failed to compile dependencies for {repo_name}.")
        if output:
            status(output.strip())
        return False, f"deps compile failed (exit {returncode})"
    return True, None


def patch_credo_regex_compatibility(repo_path, repo_name, status):
    credo_config_comment_finder = (
        repo_path /
        "deps" /
        "credo" /
        "lib" /
        "credo" /
        "check" /
        "config_comment_finder.ex"
    )

    if not credo_config_comment_finder.exists():
        return True

    try:
        source = credo_config_comment_finder.read_text()
    except OSError as exc:
        status(f"Failed to read Credo compatibility patch target for {repo_name}: {exc}")
        return False

    patched = source.replace(r"([\w-\:]+)", r"([\w\-\:]+)")
    if patched == source:
        return True

    try:
        credo_config_comment_finder.write_text(patched)
    except OSError as exc:
        status(f"Failed to patch Credo compatibility issue for {repo_name}: {exc}")
        return False

    status(f"Patched Credo regex compatibility issue for {repo_name}.")
    return True


def ezstd_zstd_cache_candidates(repo_path):
    target = (repo_path / EZSTD_ZSTD_RELATIVE_DIR).resolve()
    seen = set()

    for bucket in sorted(SCRIPT_DIR.glob("repos*")):
        if not bucket.is_dir():
            continue

        for root in [bucket / "blockscout", bucket / "blockscout" / "blockscout"]:
            candidate = root / EZSTD_ZSTD_RELATIVE_DIR
            resolved = candidate.resolve()
            key = str(resolved)
            if key in seen or resolved == target:
                continue
            seen.add(key)
            yield candidate


def seed_ezstd_zstd_cache(repo_path, repo_name, status):
    if repo_name != "Blockscout":
        return True

    target = repo_path / EZSTD_ZSTD_RELATIVE_DIR
    if (target / EZSTD_ZSTD_SUCCESS_FILE).is_file():
        return True

    source = next(
        (
            candidate for candidate in ezstd_zstd_cache_candidates(repo_path)
            if (candidate / EZSTD_ZSTD_SUCCESS_FILE).is_file()
        ),
        None,
    )
    if source is None:
        return True

    try:
        if target.exists() or target.is_symlink():
            clean_path(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target, symlinks=True)
    except OSError as exc:
        status(f"Failed to seed ezstd zstd cache for {repo_name}: {exc}")
        return False

    status(f"Seeded ezstd zstd cache for {repo_name} from {source}.")
    return True


def patch_ezstd_tag_checkout(repo_path, repo_name, status):
    build_deps = repo_path / EZSTD_BUILD_DEPS_PATH
    if not build_deps.exists():
        return True

    try:
        source = build_deps.read_text()
    except OSError as exc:
        status(f"Failed to read ezstd dependency patch target for {repo_name}: {exc}")
        return False

    fetch_tag_line = '    fail_check git fetch --force "$repo_url" "refs/tags/$tag:refs/tags/$tag"\n'
    if fetch_tag_line in source:
        return True

    checkout_line = '    fail_check git checkout "$tag"\n'
    patched = source.replace(checkout_line, fetch_tag_line + checkout_line, 1)
    if patched == source:
        return True

    try:
        build_deps.write_text(patched)
    except OSError as exc:
        status(f"Failed to patch ezstd tag checkout for {repo_name}: {exc}")
        return False

    status(f"Patched ezstd tag checkout for {repo_name}.")
    return True


def patch_known_dependency_issues(repo_path, repo_name, status):
    if not patch_credo_regex_compatibility(repo_path, repo_name, status):
        return False
    if not seed_ezstd_zstd_cache(repo_path, repo_name, status):
        return False
    if not patch_ezstd_tag_checkout(repo_path, repo_name, status):
        return False
    return True


def ensure_deps_compiled(
    repo_path,
    repo_name,
    elixir_cache_key,
    status,
    deps_compile_timeout=DEFAULT_DEPS_COMPILE_TIMEOUT_SECONDS,
    rebuild_on_commit_change=True,
):
    sentinel = repo_path / "_build" / ".perf-deps-compiled"
    repo_cache_key = repo_head(repo_path) or "unknown"
    cache_key = f"{elixir_cache_key}:{repo_cache_key}"

    if sentinel.exists():
        if not rebuild_on_commit_change:
            return True, None
        if sentinel.read_text().strip() == cache_key:
            return True, None

    ok, failure = deps_get(repo_path, repo_name, status)
    if not ok:
        return False, failure

    if not patch_known_dependency_issues(repo_path, repo_name, status):
        return False, "dependency patch failed"

    ok, failure = deps_compile(repo_path, repo_name, status, deps_compile_timeout)
    if not ok:
        return False, failure

    sentinel.parent.mkdir(parents=True, exist_ok=True)
    sentinel.write_text(cache_key + "\n")
    return True, None


def sync_repo_to_source(repo_path, source_path, repo_name, status, sync_commit_changes=True):
    if source_path is None or repo_path == source_path:
        return True

    if not source_path.exists():
        if repo_path.exists():
            status(f"Warning: sync source {source_path} missing for {repo_name}; using existing checkout.")
            return True
        status(f"Warning: {repo_path} missing and sync source {source_path} missing; skipping.")
        return False

    if not (source_path / ".git").exists():
        status(f"Warning: sync source {source_path} is not a git repository; skipping {repo_name}.")
        return False

    if not repo_path.exists():
        status(f"Cloning {repo_name} into isolated worktree repo bucket from {source_path}")
        repo_path.parent.mkdir(parents=True, exist_ok=True)
        clone = subprocess.run(
            ["git", "clone", "--no-hardlinks", str(source_path), str(repo_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if clone.returncode != 0:
            status(f"Failed to clone {repo_name} from {source_path}.")
            output = process_streams(clone)
            if output:
                status(output)
            return False
    elif not (repo_path / ".git").exists():
        status(f"Warning: {repo_path} exists but is not a git repository; skipping {repo_name}.")
        return False

    source_commit = repo_head(source_path)
    target_commit = repo_head(repo_path)
    if source_commit is None or target_commit is None:
        status(f"Warning: unable to read git commits for {repo_name}; skipping sync.")
        return False

    if source_commit != target_commit:
        if not sync_commit_changes:
            status(
                f"Keeping {repo_name} at {target_commit[:12]}; "
                f"sync source is at {source_commit[:12]}."
            )
            return True

        if repo_has_tracked_changes(repo_path):
            status(
                f"Warning: {repo_name} has tracked local changes in {repo_path}; "
                "not moving it to the main repo commit."
            )
            return False

        fetch = git_command_args(repo_path, ["fetch", "--quiet", str(source_path), source_commit])
        if fetch.returncode != 0:
            status(f"Warning: failed to fetch {source_commit} for {repo_name} from {source_path}.")
            output = process_streams(fetch)
            if output:
                status(output)
            return False

        checkout = git_command_args(repo_path, ["checkout", "--detach", "--quiet", source_commit])
        if checkout.returncode != 0:
            status(f"Warning: failed to checkout {source_commit} for {repo_name}.")
            output = process_streams(checkout)
            if output:
                status(output)
            return False

        status(f"Synced {repo_name} to {source_commit[:12]} from the main repo bucket.")

    return True


def clean_path(path):
    if path.is_symlink() or path.is_file():
        path.unlink()
    else:
        shutil.rmtree(path)


def clean_repo_cache_paths(repo_path, repo_name, status):
    removed = []
    failed = False

    for relative_path in MONTHLY_CLEAN_PATHS:
        path = repo_path / relative_path
        if not path.exists() and not path.is_symlink():
            continue

        try:
            clean_path(path)
        except OSError as exc:
            status(f"Warning: failed to clean {path} for {repo_name}: {exc}")
            failed = True
        else:
            removed.append(relative_path)

    if removed:
        status(f"Cleaned {repo_name} repo cache paths: {', '.join(removed)}")

    return not failed


def monthly_clean_repo_bucket(repo_bucket, repo_dir, repositories, status):
    if repo_dir == MAIN_REPOS_DIR:
        return True

    current_month = datetime.date.today().strftime("%Y-%m")
    marker = repo_dir / MONTHLY_CLEAN_MARKER

    try:
        if marker.exists() and marker.read_text().strip() == current_month:
            return True
    except OSError as exc:
        status(f"Warning: failed to read monthly cleanup marker {marker}: {exc}")

    if repo_dir.exists() and not repo_dir.is_dir():
        status(f"Warning: cannot monthly-clean {repo_bucket}: {repo_dir} is not a directory.")
        return False

    status(f"Monthly cleanup for repository bucket {repo_bucket} ({repo_dir})")
    repo_dir.mkdir(parents=True, exist_ok=True)

    failed = False
    for repo in repositories:
        repo_path = repo["path"]
        if not repo_path.exists():
            continue
        if not clean_repo_cache_paths(repo_path, repo["name"], status):
            failed = True

    if failed:
        status(f"Warning: monthly cleanup for {repo_bucket} had errors; marker was not updated.")
        return False

    try:
        marker.write_text(current_month + "\n")
    except OSError as exc:
        status(f"Warning: failed to update monthly cleanup marker {marker}: {exc}")
        return False

    return True


def format_seconds(seconds):
    return f"{seconds:g}"


def positive_seconds(value):
    try:
        seconds = float(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a number of seconds") from exc
    if seconds <= 0:
        raise argparse.ArgumentTypeError("must be greater than 0")
    if not math.isfinite(seconds):
        raise argparse.ArgumentTypeError("must be finite")
    return seconds


def signal_process_group(proc, sig):
    try:
        os.killpg(os.getpgid(proc.pid), sig)
        return True
    except ProcessLookupError:
        return True
    except OSError:
        return False


def stop_compile_process(proc):
    if proc.poll() is not None:
        return
    if not signal_process_group(proc, signal.SIGTERM):
        proc.terminate()
    try:
        proc.wait(timeout=2)
        return
    except subprocess.TimeoutExpired:
        pass

    if not signal_process_group(proc, signal.SIGKILL):
        proc.kill()
    proc.wait()


def run_compile(
    repo_path,
    perf_path,
    show_output,
    run_label=None,
    validate_compile_env=True,
    compile_timeout=DEFAULT_COMPILE_TIMEOUT_SECONDS,
    extra_env=None,
):
    cmd = [
        str(MIX_PATH),
        "compile",
        "--force",
        "--profile",
        "time",
        "--no-deps-check",
        "--no-elixir-version-check",
        "--no-prune-code-paths",
        "--no-warnings-as-errors",
    ]
    if not validate_compile_env:
        cmd.append("--no-validate-compile-env")
    with open(perf_path, "a+", encoding="utf-8") as perf:
        if run_label:
            perf.write(f"{run_label}\n")
        perf.flush()
        output_start = perf.tell()
        timed_out = False

        if show_output:
            output_lines = []
            with subprocess.Popen(
                cmd,
                cwd=repo_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                start_new_session=True,
                env=extra_env,
            ) as proc:
                def stream_output():
                    for line in proc.stdout:
                        output_lines.append(line)
                        perf.write(line)
                        print(line, end="", flush=True)

                output_thread = threading.Thread(target=stream_output)
                output_thread.start()
                try:
                    returncode = proc.wait(timeout=compile_timeout)
                except subprocess.TimeoutExpired:
                    timed_out = True
                    stop_compile_process(proc)
                    returncode = COMPILE_TIMEOUT_RETURNCODE
                output_thread.join()
        else:
            with subprocess.Popen(
                cmd,
                cwd=repo_path,
                stdout=perf,
                stderr=subprocess.STDOUT,
                text=True,
                start_new_session=True,
                env=extra_env,
            ) as proc:
                try:
                    returncode = proc.wait(timeout=compile_timeout)
                except subprocess.TimeoutExpired:
                    timed_out = True
                    stop_compile_process(proc)
                    returncode = COMPILE_TIMEOUT_RETURNCODE

        if timed_out:
            timeout_message = (
                f"\nCompilation timed out after {format_seconds(compile_timeout)} seconds; "
                "stopped mix compile.\n"
            )
            perf.write(timeout_message)
            if show_output:
                output_lines.append(timeout_message)
                print(timeout_message, end="", flush=True)

        perf.write("\n")
        perf.flush()
        if show_output:
            output = "".join(output_lines)
        else:
            perf.seek(output_start)
            output = perf.read()
        return returncode, output


def count_type_warnings(repo_path):
    result = subprocess.run(
        [str(ELIXIR_EXECUTABLE), "-e", TYPE_WARNING_COUNTER_CODE],
        cwd=repo_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    output = result.stdout or ""
    match = re.search(
        rf"^{re.escape(TYPE_WARNING_COUNT_MARKER)}([0-9]+)\s*$",
        output,
        re.MULTILINE,
    )

    if result.returncode != 0:
        return None, f"type warning count failed (exit {result.returncode})", output.strip()
    if match is None:
        return None, "type warning count missing from counter output", output.strip()
    return int(match.group(1)), None, output.strip()


def get_elixir_version():
    commands = [
        f"{ELIXIR_PATH}/elixir --version",
        "elixir --version",
        f"{MIX_PATH} --version",
    ]
    for cmd in commands:
        out = run(cmd, capture=True)
        for line in out.splitlines():
            line = line.strip()
            if line.startswith("Elixir "):
                return line.split()[1]
    return "unknown"


def get_git_metadata(path):
    resolved = Path(path).expanduser().resolve()
    unknown = {
        "repo": "unknown",
        "branch": "unknown",
        "commit": "unknown",
    }

    repo = subprocess.run(
        ["git", "-C", str(resolved), "rev-parse", "--show-toplevel"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if repo.returncode != 0:
        return unknown

    branch = subprocess.run(
        ["git", "-C", str(resolved), "symbolic-ref", "--quiet", "--short", "HEAD"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    commit = subprocess.run(
        ["git", "-C", str(resolved), "rev-parse", "HEAD"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    if commit.returncode != 0:
        return unknown

    branch_name = branch.stdout.strip() if branch.returncode == 0 else "detached"
    return {
        "repo": repo.stdout.strip() or "unknown",
        "branch": branch_name or "unknown",
        "commit": commit.stdout.strip() or "unknown",
    }


def source_dirs(repo_path):
    repo_path = Path(repo_path)
    dirs = []

    root_lib = repo_path / "lib"
    if root_lib.is_dir():
        dirs.append(root_lib)

    apps_dir = repo_path / "apps"
    if apps_dir.is_dir():
        for app_dir in sorted(apps_dir.iterdir()):
            app_lib = app_dir / "lib"
            if app_lib.is_dir():
                dirs.append(app_lib)

    return dirs


def source_files(repo_path):
    files = []
    for source_dir in source_dirs(repo_path):
        files.extend(path for path in source_dir.rglob("*") if path.suffix in (".ex", ".exs"))
    return files


def count_loc(repo_path):
    count = 0
    for path in source_files(repo_path):
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        count += sum(1 for line in lines if line.strip() and not line.lstrip().startswith("#"))
    return count


def count_files(repo_path):
    return len(source_files(repo_path))


def count_modules(repo_path):
    count = 0
    for path in source_files(repo_path):
        try:
            lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            continue
        count += sum(1 for line in lines if re.match(r"^\s*defmodule", line))
    return count


def extract_profile_time(output, keyword):
    seconds = []
    for line in output.splitlines():
        if keyword not in line:
            continue
        match = re.search(r"in\s+([0-9]+(?:\.[0-9]+)?)\s*ms", line)
        if match:
            seconds.append(float(match.group(1)) / 1000.0)
    return sum(seconds) if seconds else None


def extract_compile_metrics(output):
    tc_time = extract_profile_time(output, "Finished group pass check")
    comp_time = extract_profile_time(output, "Finished compilation cycle")
    return tc_time, comp_time


def t_critical_95(df):
    # Two-tailed 95% t critical values for 1..30 degrees of freedom.
    table = {
        1: 12.706, 2: 4.303, 3: 3.182, 4: 2.776, 5: 2.571, 6: 2.447,
        7: 2.365, 8: 2.306, 9: 2.262, 10: 2.228, 11: 2.201, 12: 2.179,
        13: 2.160, 14: 2.145, 15: 2.131, 16: 2.120, 17: 2.110, 18: 2.101,
        19: 2.093, 20: 2.086, 21: 2.080, 22: 2.074, 23: 2.069, 24: 2.064,
        25: 2.060, 26: 2.056, 27: 2.052, 28: 2.048, 29: 2.045, 30: 2.042,
    }
    return table.get(df, 1.960)


def summarize_samples(samples):
    if not samples:
        return None
    n = len(samples)
    mean = statistics.fmean(samples)
    if n < 2:
        return {
            "n": n,
            "mean": mean,
            "stddev": 0.0,
            "stderr": 0.0,
            "ci95": 0.0,
        }
    stddev = statistics.stdev(samples)
    stderr = stddev / math.sqrt(n)
    ci95 = t_critical_95(n - 1) * stderr
    return {
        "n": n,
        "mean": mean,
        "stddev": stddev,
        "stderr": stderr,
        "ci95": ci95,
    }


def format_tc_value(row, serious_run):
    if row.get("tc_status"):
        return row["tc_status"]
    if row.get("timed_out"):
        return f"timeout after {format_seconds(row['timeout_seconds'])} s"
    if serious_run:
        return f"{row['tc_mean']:.3f} +- {row['tc_ci95']:.3f} s"
    return f"{row['tc_time']:.3f} s"


def format_type_warnings_value(row):
    if "type_warnings" in row:
        return str(row["type_warnings"])
    return row.get("type_warning_status", "not counted")


def summarize_type_warning_counts(counts, failure=None):
    if failure:
        return {"type_warning_status": failure}
    if not counts:
        return {"type_warning_status": "not compiled"}

    unique_counts = sorted(set(counts))
    if len(unique_counts) == 1:
        return {"type_warnings": unique_counts[0]}

    return {
        "type_warning_status": (
            "inconsistent counts: " +
            ", ".join(str(count) for count in counts)
        )
    }


def format_tc_table(repo_data, serious_run, include_type_warnings=False):
    if serious_run:
        header = "| Codebase | LoC | Files | Modules | TC Time (mean +- 95% CI) |"
        separator = "|---|---:|---:|---:|---:|"
    else:
        header = "| Codebase | LoC | Files | Modules | TC Time |"
        separator = "|---|---:|---:|---:|---:|"

    if include_type_warnings:
        header = header + " Type Warnings |"
        separator = separator + "---:|"

    lines = [header, separator]
    for row in repo_data:
        type_warnings_cell = (
            f" {format_type_warnings_value(row)} |" if include_type_warnings else ""
        )
        lines.append(
            f"| {row['name']} | {row['loc']:,} | {row['files']} | {row['modules']} | "
            f"{format_tc_value(row, serious_run)} |{type_warnings_cell}"
        )
    return "\n".join(lines) + "\n"


def tc_status_row(repo_path, repo_name, tc_status):
    return {
        "loc": count_loc(repo_path),
        "name": repo_name,
        "files": count_files(repo_path),
        "modules": count_modules(repo_path),
        "tc_status": tc_status,
        "type_warning_status": "not compiled",
    }


def reinit_repo(repo_path, repo_name):
    print(f"Reinitializing {repo_name} in {repo_path}")
    if not repo_path.exists():
        print(f"Warning: {repo_path} does not exist, skipping...")
        return
    run("rm -rf _build deps", cwd=repo_path)
    run(f"{MIX_PATH} deps.get", cwd=repo_path)
    print(f"Completed reinitializing {repo_name}\n")


def clone_repo(checkout_path, project_path, repo_name, repo_url):
    print(f"Preparing {repo_name} in {checkout_path}")
    if checkout_path.exists():
        if not checkout_path.is_dir():
            print(f"Warning: {checkout_path} exists but is not a directory, skipping...")
            return False
        if not (checkout_path / ".git").exists():
            print(f"Warning: {checkout_path} exists but is not a git repository, skipping...")
            return False
        print(f"{repo_name} already exists, skipping clone.")
    else:
        checkout_path.parent.mkdir(parents=True, exist_ok=True)
        clone = subprocess.run(
            ["git", "clone", repo_url, str(checkout_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        if clone.returncode != 0:
            print(f"Failed to clone {repo_name}.")
            print_process_streams(clone)
            print()
            return False
        print_process_streams(clone)

    if not project_path.exists():
        print(f"Warning: {project_path} does not exist, skipping dependency fetch...")
        return False

    ok, _ = deps_get(project_path, repo_name, print)
    if not ok:
        print()
        return False
    print(f"Completed preparing {repo_name}\n")
    return True


def reset_repo(repo_path, repo_name):
    print(f"Resetting {repo_name} repository in {repo_path}")
    if not repo_path.exists():
        print(f"Warning: {repo_path} does not exist, skipping...")
        return False

    fetch = git_command(repo_path, "git fetch --all --prune")
    if fetch.returncode != 0:
        print("Failed to fetch updates.")
        print_process_streams(fetch)
        print()
        return False
    print_process_streams(fetch)

    upstream = git_command(repo_path, "git rev-parse --abbrev-ref --symbolic-full-name @{u}")
    if upstream.returncode == 0:
        target = upstream.stdout.strip()
    else:
        branch = git_command(repo_path, "git rev-parse --abbrev-ref HEAD")
        if branch.returncode != 0:
            print("Unable to determine current branch.")
            print_process_streams(branch)
            print()
            return False
        target = f"origin/{branch.stdout.strip()}"

    reset = git_command(repo_path, f"git reset --hard {target}")
    if reset.returncode != 0:
        print("Failed to reset repository.")
        print_process_streams(reset)
        print()
        return False
    print_process_streams(reset)

    clean = git_command(repo_path, "git clean -fd")
    if clean.returncode != 0:
        print("Failed to clean repository.")
        print_process_streams(clean)
        print()
        return False
    print_process_streams(clean)
    print("Reset complete.\n")
    return True


def pull_repo(repo_path, repo_name, autostash=False, reset_before=False):
    print(f"Pulling latest {repo_name} in {repo_path}")
    if not repo_path.exists():
        print(f"Warning: {repo_path} does not exist, skipping...")
        return False
    if reset_before:
        if not reset_repo(repo_path, repo_name):
            print("Skipping pull because reset failed.\n")
            return False

    stashed = False
    pull_success = False

    try:
        while True:
            result = git_command(repo_path, "git pull --ff-only")
            if result.returncode == 0:
                print_process_streams(result)
                pull_success = True
                break

            combined = "\n".join(filter(None, [result.stdout, result.stderr])).lower()
            needs_stash = "would be overwritten" in combined or "please commit your changes or stash them" in combined

            if autostash and not stashed and needs_stash:
                print("Local changes detected; stashing before retry...")
                stash = git_command(repo_path, "git stash push --include-untracked --message 'perf.py auto-stash'")
                if stash.returncode != 0:
                    print("Failed to stash local changes.")
                    print_process_streams(stash)
                    break
                stashed = True
                print_process_streams(stash)
                print("Retrying pull...\n")
                continue

            print(f"Failed updating {repo_name}.")
            print_process_streams(result)
            break
    finally:
        if stashed:
            pop = git_command(repo_path, "git stash pop")
            if pop.returncode != 0:
                print("Warning: failed to restore local changes, please resolve manually.")
                print_process_streams(pop)
                pull_success = False
            else:
                print_process_streams(pop)
                print("Restored local changes.")

    if pull_success:
        print(f"Completed updating {repo_name}\n")
    else:
        print()

    return pull_success


def should_process_repo(name, selected):
    return not selected or name in selected


def guard_exactness_compile_env(guard_root, run_id, repo_name, repo_path):
    raw_dir = guard_root / "raw" / repo_name
    raw_dir.mkdir(parents=True, exist_ok=True)

    env = os.environ.copy()
    env["ELIXIR_GUARD_EXACTNESS_DIR"] = str(raw_dir.resolve())
    env["ELIXIR_GUARD_EXACTNESS_PROJECT"] = repo_name
    env["ELIXIR_GUARD_EXACTNESS_REPO_ROOT"] = str(Path(repo_path).resolve())
    env["ELIXIR_GUARD_EXACTNESS_RUN_ID"] = run_id
    return env, raw_dir


def read_guard_exactness_rows(raw_dir):
    rows = []
    jsonl_files = sorted(raw_dir.glob("*.jsonl")) if raw_dir.exists() else []

    for path in jsonl_files:
        with path.open("r", encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError as exc:
                    raise RuntimeError(f"invalid JSON in {path}:{line_number}: {exc}") from exc
                row["_jsonl_file"] = str(path)
                rows.append(row)

    return rows, jsonl_files


def guard_exactness_existing_records(guard_root):
    raw_root = guard_root / "raw"
    records = []

    if not raw_root.is_dir():
        return records

    for raw_dir in sorted(path for path in raw_root.iterdir() if path.is_dir()):
        rows, _jsonl_files = read_guard_exactness_rows(raw_dir)
        repo_root = next((row.get("repo_root") for row in rows if row.get("repo_root")), None)
        if repo_root is None:
            repo_root = raw_dir
        records.append({
            "name": raw_dir.name,
            "repo_path": Path(repo_root),
            "raw_dir": raw_dir,
        })

    return records


def relative_guard_file(row, repo_path):
    file = row.get("file") or ""
    if not file:
        return ""

    path = Path(file)
    if not path.is_absolute():
        return file

    try:
        return str(path.resolve().relative_to(Path(repo_path).resolve()))
    except ValueError:
        return None


def retained_guard_row(row, repo_path):
    if row.get("generated") is True:
        return None

    relative = relative_guard_file(row, repo_path)
    if relative is None:
        return None

    parts = Path(relative).parts
    if parts and parts[0] in {"deps", "_build"}:
        return None
    if "_build" in parts:
        return None

    row = dict(row)
    row["file"] = relative
    return row


def join_guard_values(values):
    return " | ".join(str(value) for value in (values or []))


def deduplicate_guard_rows(rows):
    deduped = {}

    for row in rows:
        key = (
            row.get("project"),
            row.get("file"),
            row.get("line"),
            row.get("column"),
            row.get("module"),
            row.get("function"),
            row.get("site_kind"),
            tuple(row.get("patterns") or []),
            tuple(row.get("guards") or []),
        )

        entry = deduped.get(key)
        if entry is None:
            entry = {
                "project": row.get("project"),
                "file": row.get("file"),
                "line": row.get("line"),
                "column": row.get("column"),
                "module": row.get("module"),
                "function": row.get("function"),
                "site_kind": row.get("site_kind"),
                "guard_count": row.get("guard_count") or 0,
                "exact": row.get("exact") is True,
                "invocations": 0,
                "patterns": row.get("patterns") or [],
                "guards": row.get("guards") or [],
                "possible_arg_types": row.get("possible_arg_types") or [],
                "sure_arg_types": row.get("sure_arg_types") or [],
                "expected_arg_types": row.get("expected_arg_types") or [],
                "stack_modes": set(),
                "reverse_arrows": set(),
            }
            deduped[key] = entry
        else:
            entry["exact"] = entry["exact"] and row.get("exact") is True

        entry["invocations"] += 1
        if row.get("stack_mode"):
            entry["stack_modes"].add(row["stack_mode"])
        if row.get("reverse_arrow"):
            entry["reverse_arrows"].add(row["reverse_arrow"])

    return list(deduped.values())


def guard_exactness_ratio(numerator, denominator):
    return "" if denominator == 0 else f"{numerator / denominator:.4f}"


def latex_escape(value):
    value = str(value)
    replacements = {
        "\\": "\\textbackslash{}",
        "&": "\\&",
        "%": "\\%",
        "$": "\\$",
        "#": "\\#",
        "_": "\\_",
        "{": "\\{",
        "}": "\\}",
        "~": "\\textasciitilde{}",
        "^": "\\textasciicircum{}",
    }
    return "".join(replacements.get(char, char) for char in value)


def write_guard_exactness_outputs(guard_root, repo_records, elixir_version, elixir_git, args, status):
    guard_root.mkdir(parents=True, exist_ok=True)
    all_rows = []
    summary_rows = []
    repo_metadata = []

    for record in repo_records:
        raw_rows, jsonl_files = read_guard_exactness_rows(record["raw_dir"])
        retained_rows = [
            retained
            for row in raw_rows
            for retained in [retained_guard_row(row, record["repo_path"])]
            if retained is not None
        ]
        deduped_rows = deduplicate_guard_rows(retained_rows)
        analyzed = len(deduped_rows)
        exact = sum(1 for row in deduped_rows if row["exact"])
        guarded = [row for row in deduped_rows if row["guard_count"] > 0]
        guarded_exact = sum(1 for row in guarded if row["exact"])

        summary_rows.append({
            "project": record["name"],
            "analyzed_pairs": analyzed,
            "exact_pairs": exact,
            "exactness_ratio": guard_exactness_ratio(exact, analyzed),
            "guarded_analyzed_pairs": len(guarded),
            "guarded_exact_pairs": guarded_exact,
            "guarded_exactness_ratio": guard_exactness_ratio(guarded_exact, len(guarded)),
            "raw_rows": len(raw_rows),
            "retained_invocations": len(retained_rows),
            "jsonl_files": len(jsonl_files),
        })

        for row in deduped_rows:
            row["stack_modes"] = ", ".join(sorted(row["stack_modes"]))
            row["reverse_arrows"] = ", ".join(sorted(row["reverse_arrows"]))
            all_rows.append(row)

        repo_metadata.append({
            "name": record["name"],
            "path": str(record["repo_path"]),
            "raw_dir": str(record["raw_dir"]),
            "git": get_git_metadata(record["repo_path"]),
            "raw_rows": len(raw_rows),
            "retained_invocations": len(retained_rows),
            "deduplicated_rows": analyzed,
        })

    rows_path = guard_root / "guard_exactness_rows.csv"
    with rows_path.open("w", encoding="utf-8", newline="") as file:
        fieldnames = [
            "project",
            "file",
            "line",
            "column",
            "module",
            "function",
            "site_kind",
            "guard_count",
            "exact",
            "invocations",
            "patterns",
            "guards",
            "possible_arg_types",
            "sure_arg_types",
            "expected_arg_types",
            "stack_modes",
            "reverse_arrows",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for row in sorted(all_rows, key=lambda r: (r["project"], r["file"], r["line"] or 0)):
            writer.writerow({
                **{key: row.get(key) for key in fieldnames},
                "patterns": join_guard_values(row["patterns"]),
                "guards": join_guard_values(row["guards"]),
                "possible_arg_types": join_guard_values(row["possible_arg_types"]),
                "sure_arg_types": join_guard_values(row["sure_arg_types"]),
                "expected_arg_types": join_guard_values(row["expected_arg_types"]),
            })

    summary_path = guard_root / "guard_exactness_summary.csv"
    with summary_path.open("w", encoding="utf-8", newline="") as file:
        fieldnames = [
            "project",
            "analyzed_pairs",
            "exact_pairs",
            "exactness_ratio",
            "guarded_analyzed_pairs",
            "guarded_exact_pairs",
            "guarded_exactness_ratio",
            "raw_rows",
            "retained_invocations",
            "jsonl_files",
        ]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summary_rows)

    tex_path = guard_root / "precise_guards_table.tex"
    with tex_path.open("w", encoding="utf-8") as file:
        file.write("\\begin{tabular}{|l|r|r|}\n")
        file.write("\\hline\n")
        file.write("\\textbf{Library} & \\textbf{Analyzed Pairs} & \\textbf{Exact Pairs} \\\\\n")
        file.write("\\hline\n")
        for row in summary_rows:
            file.write(
                f"{latex_escape(row['project'])} & "
                f"{row['analyzed_pairs']:,} & "
                f"{row['exact_pairs']:,} \\\\\n"
            )
        file.write("\\hline\n")
        file.write("\\end{tabular}\n")

    metadata_path = guard_root / "metadata.json"
    metadata = {
        "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "guard_exactness_dir": str(guard_root),
        "elixir_version": elixir_version,
        "elixir_git": elixir_git,
        "args": vars(args),
        "repositories": repo_metadata,
        "outputs": {
            "rows": str(rows_path),
            "summary": str(summary_path),
            "tex": str(tex_path),
            "metadata": str(metadata_path),
        },
    }
    metadata_path.write_text(json.dumps(metadata, indent=2, sort_keys=True) + "\n")

    status(f"Guard exactness rows: {rows_path}")
    status(f"Guard exactness summary: {summary_path}")
    status(f"Guard exactness TeX table: {tex_path}")
    status(f"Guard exactness metadata: {metadata_path}")


def main():
    parser = argparse.ArgumentParser(description="Compile multiple Elixir repos with profiling")
    parser.add_argument("-r", "--repo", action="append", help="Select repository by name")
    parser.add_argument(
        "--elixir-root",
        help=f"Path to Elixir root containing bin/ (default: {DEFAULT_ELIXIR_ROOT})"
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Output file name/path (default: results/result-<timestamp>.txt)"
    )
    parser.add_argument(
        "--clone",
        action="store_true",
        help="Clone missing repositories and run mix deps.get"
    )
    parser.add_argument(
        "--repo-bucket",
        choices=["auto", "main", "worktrees", "shared"],
        default="auto",
        help=(
            "Repository checkout bucket to use. 'auto' uses repos for the main "
            "Elixir checkout and repos-<worktree-name> for each other Elixir "
            "worktree. 'worktrees' uses the legacy shared repos-worktrees bucket."
        )
    )
    parser.add_argument(
        "--no-sync-repos",
        action="store_true",
        help="Do not sync worktree-bucket repositories to the main-bucket git commits before compiling"
    )
    parser.add_argument(
        "--no-rebuild-on-commit-change",
        action="store_true",
        help=(
            "Do not refresh worktree repo checkouts or recompile deps solely because "
            "Elixir/repo commits changed; once deps are built, keep reusing them"
        )
    )
    parser.add_argument("--reinit", action="store_true", help="Clean and re-fetch deps")
    parser.add_argument("--pull", action="store_true", help="Run git pull for repositories")
    parser.add_argument(
        "--pull-autostash",
        action="store_true",
        help="Temporarily stash and restore local changes if pull needs a clean tree"
    )
    parser.add_argument(
        "--pull-reset",
        action="store_true",
        help="Fetch and reset each repository to its upstream before pulling"
    )
    parser.add_argument(
        "--show-output",
        action="store_true",
        help="Stream compilation output to stdout while still logging to perf.txt"
    )
    parser.add_argument(
        "--no-validate-compile-env",
        action="store_true",
        help="Pass --no-validate-compile-env to mix compile"
    )
    parser.add_argument(
        "--compile-timeout",
        type=positive_seconds,
        default=DEFAULT_COMPILE_TIMEOUT_SECONDS,
        metavar="SECONDS",
        help=(
            "Stop each measured repo mix compile after SECONDS seconds "
            f"(default: {format_seconds(DEFAULT_COMPILE_TIMEOUT_SECONDS)})"
        )
    )
    parser.add_argument(
        "--deps-compile-timeout",
        type=positive_seconds,
        default=DEFAULT_DEPS_COMPILE_TIMEOUT_SECONDS,
        metavar="SECONDS",
        help=(
            "Stop worktree-bucket dependency compilation after SECONDS seconds "
            f"(default: {format_seconds(DEFAULT_DEPS_COMPILE_TIMEOUT_SECONDS)})"
        )
    )
    parser.add_argument(
        "--tc-table",
        action="store_true",
        help="Write and print a plain Markdown table with only type-checking times"
    )
    parser.add_argument(
        "--type-warnings",
        action="store_true",
        help=(
            "Count Elixir type-warning diagnostics from the compiled project "
            "and include the count in result tables"
        )
    )
    parser.add_argument(
        "--guard-exactness",
        action="store_true",
        help=(
            "Collect guard-exactness JSONL emitted by the Elixir type checker "
            "and write CSV/TeX summaries under results/guard-exactness"
        )
    )
    parser.add_argument(
        "--guard-exactness-run-id",
        help="Use a fixed guard-exactness run id instead of a timestamp"
    )
    parser.add_argument(
        "--guard-exactness-root",
        help="Use an explicit guard-exactness output directory"
    )
    parser.add_argument(
        "--guard-exactness-summarize-only",
        action="store_true",
        help="Read an existing guard-exactness raw directory and regenerate summary outputs"
    )
    parser.add_argument(
        "--serious-run",
        action="store_true",
        help="Run repeated measurements with warmups and 95%% confidence intervals"
    )
    parser.add_argument(
        "--serious-runs",
        type=int,
        default=SERIOUS_RUN_DEFAULT_RUNS,
        help=f"Measured runs per repo for --serious-run (default: {SERIOUS_RUN_DEFAULT_RUNS})"
    )
    parser.add_argument(
        "--serious-warmups",
        type=int,
        default=SERIOUS_RUN_DEFAULT_WARMUPS,
        help=f"Warmup runs per repo for --serious-run (default: {SERIOUS_RUN_DEFAULT_WARMUPS})"
    )
    parser.add_argument("-l", "--list", action="store_true", help="List repositories")
    args = parser.parse_args()
    status_stream = sys.stderr if args.tc_table else sys.stdout

    def status(*values, **kwargs):
        print(*values, file=status_stream, **kwargs)

    if args.pull_autostash and args.pull_reset:
        parser.error("--pull-autostash and --pull-reset cannot be used together.")
    if args.guard_exactness_summarize_only:
        args.guard_exactness = True
    if not args.serious_run and (
        args.serious_runs != SERIOUS_RUN_DEFAULT_RUNS or
        args.serious_warmups != SERIOUS_RUN_DEFAULT_WARMUPS
    ):
        parser.error("--serious-runs/--serious-warmups require --serious-run.")
    if args.serious_runs < 2:
        parser.error("--serious-runs must be at least 2.")
    if args.serious_warmups < 0:
        parser.error("--serious-warmups must be 0 or greater.")

    selected_elixir_root = Path(args.elixir_root).expanduser() if args.elixir_root else DEFAULT_ELIXIR_ROOT
    selected_bin = selected_elixir_root / "bin"
    if not selected_bin.is_dir():
        parser.error(f"Elixir root '{selected_elixir_root}' does not contain a bin directory.")
    if not (selected_bin / "mix").exists():
        parser.error(f"Elixir bin directory '{selected_bin}' does not contain mix.")
    if not os.access(selected_bin / "mix", os.X_OK):
        parser.error(f"'{selected_bin / 'mix'}' is not executable.")
    if args.type_warnings and not (selected_bin / "elixir").exists():
        parser.error(f"Elixir bin directory '{selected_bin}' does not contain elixir.")
    if args.type_warnings and not os.access(selected_bin / "elixir", os.X_OK):
        parser.error(f"'{selected_bin / 'elixir'}' is not executable.")
    configure_elixir_bin(selected_bin)

    repo_bucket, repo_dir, sync_source_dir = repo_bucket_for_root(
        selected_elixir_root,
        args.repo_bucket
    )
    if args.no_sync_repos:
        sync_source_dir = None
    repositories = build_repositories(repo_dir)

    if args.list:
        print("Available repositories:")
        for name in REPO_NAMES:
            print(" ", name)
        sys.exit(0)

    selected_repos = args.repo or DEFAULT_REPO_NAMES
    now = datetime.datetime.now().strftime("%m%d-%H%M")
    perf_path = Path.cwd() / "perf.txt"
    if args.output:
        output_path = Path(args.output).expanduser()
        result_path = output_path if output_path.is_absolute() else Path.cwd() / output_path
    else:
        result_path = Path.cwd() / RESULTS_DIR / f"result-{now}.txt"
    result_path.parent.mkdir(parents=True, exist_ok=True)
    perf_path.unlink(missing_ok=True)
    result_path.unlink(missing_ok=True)

    guard_run_id = args.guard_exactness_run_id or datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

    if args.guard_exactness_root:
        guard_root = Path(args.guard_exactness_root).expanduser()
        guard_root = guard_root if guard_root.is_absolute() else Path.cwd() / guard_root
        if args.guard_exactness_run_id is None:
            guard_run_id = guard_root.name
    else:
        guard_root = Path.cwd() / RESULTS_DIR / "guard-exactness" / guard_run_id

    guard_repo_records = []
    if args.guard_exactness:
        guard_root.mkdir(parents=True, exist_ok=True)

    elixir_version = get_elixir_version()
    elixir_git = get_git_metadata(selected_elixir_root)
    elixir_cache_key = elixir_git["commit"] if elixir_git["commit"] != "unknown" else elixir_version
    status(f"Using Elixir version: {elixir_version}")
    status(f"Elixir source: {elixir_git['repo']}")
    status(f"Elixir branch: {elixir_git['branch']}")
    status(f"Elixir commit: {elixir_git['commit']}")
    status(f"Repo compilation timeout: {format_seconds(args.compile_timeout)} seconds")
    status(f"Dependency compilation timeout: {format_seconds(args.deps_compile_timeout)} seconds")
    status(f"Repository bucket: {repo_bucket} ({repo_dir})")
    if args.type_warnings:
        status("Type warning counting: enabled")
    if args.guard_exactness:
        status(f"Guard exactness collection: enabled ({guard_root})")
    if args.no_rebuild_on_commit_change:
        status("Commit-change repo/deps rebuilds: disabled")
    if sync_source_dir is not None:
        status(f"Repository sync source: {sync_source_dir}")
    selected_repositories = [
        repo for repo in repositories
        if should_process_repo(repo["name"], selected_repos)
    ]
    monthly_clean_repo_bucket(repo_bucket, repo_dir, selected_repositories, status)
    if args.serious_run:
        status(
            "Serious-run protocol: "
            f"{args.serious_warmups} warmup runs + {args.serious_runs} measured runs per repo."
        )
        status("Error estimate: 95% confidence interval half-width from Student's t * standard error.")

    if args.guard_exactness_summarize_only:
        write_guard_exactness_outputs(
            guard_root,
            guard_exactness_existing_records(guard_root),
            elixir_version,
            elixir_git,
            args,
            status,
        )
        return

    clone_failures = False
    if args.clone:
        print("Ensuring repositories are cloned and dependencies are fetched...\n")
        for repo in repositories:
            repo_path = repo["path"]
            checkout_path = repo["checkout_path"]
            repo_name = repo["name"]
            if should_process_repo(repo_name, selected_repos):
                ok = clone_repo(checkout_path, repo_path, repo_name, repo["url"])
                clone_failures = clone_failures or not ok
        if clone_failures:
            print("Repository clone/setup complete with errors.")
            sys.exit(1)
        print("Repository clone/setup complete.\n")
        if not args.pull and not args.reinit:
            return

    pull_failures = False
    if args.pull:
        print("Running git pull across repositories...\n")
        pull_repositories = build_repositories(sync_source_dir) if sync_source_dir is not None else repositories
        for repo in pull_repositories:
            checkout_path = repo["checkout_path"]
            repo_name = repo["name"]
            if should_process_repo(repo_name, selected_repos):
                ok = pull_repo(
                    checkout_path,
                    repo_name,
                    autostash=args.pull_autostash,
                    reset_before=args.pull_reset
                )
                pull_failures = pull_failures or not ok
        if pull_failures:
            print("Git pull complete with errors.")
        else:
            print("Git pull complete.")
        if not args.reinit:
            if pull_failures:
                sys.exit(1)
            return

    # Handle reinit mode
    if args.reinit:
        print("Running in reinit mode...\n")
        for repo in repositories:
            repo_path = repo["path"]
            repo_name = repo["name"]
            if should_process_repo(repo_name, selected_repos):
                reinit_repo(repo_path, repo_name)
        print("Reinit complete.")
        return

    if not args.tc_table:
        # Start LaTeX table
        with open(result_path, "w") as f:
            f.write(f"% Elixir version: {elixir_version}\n")
            f.write(f"% Elixir source: {elixir_git['repo']}\n")
            f.write(f"% Elixir branch: {elixir_git['branch']}\n")
            f.write(f"% Elixir commit: {elixir_git['commit']}\n")
            f.write(f"% Repo compilation timeout: {format_seconds(args.compile_timeout)} seconds\n")
            f.write(
                "% Dependency compilation timeout: "
                f"{format_seconds(args.deps_compile_timeout)} seconds\n"
            )
            if args.type_warnings:
                f.write("% Type warning counting: enabled; project/umbrella apps only, dependencies excluded\n")
            if args.no_rebuild_on_commit_change:
                f.write("% Commit-change repo/deps rebuilds: disabled\n")
            if args.serious_run:
                f.write("% Protocol: serious-run\n")
                f.write(f"% Warmup runs per repo: {args.serious_warmups}\n")
                f.write(f"% Measured runs per repo: {args.serious_runs}\n")
                f.write("% Error estimate: 95% CI half-width (Student's t * sample stddev / sqrt(n))\n")
            column_spec = "|l|r|r|r|r|r|"
            if args.type_warnings:
                column_spec = "|l|r|r|r|r|r|r|"
            f.write(f"\\begin{{center}}\n\\begin{{tabular}}{{{column_spec}}}\n")
            f.write("\\hline\\rowcolor{violet2}\n")
            if args.serious_run:
                header = "Codebase & LoC & Files & Modules & TC Time (mean +- 95\\% CI) & Compilation Time (mean +- 95\\% CI)"
            else:
                header = "Codebase & LoC & Files & Modules & TC Time & Compilation Time"
            if args.type_warnings:
                header += " & Type Warnings"
            f.write(f"{header} \\\\\n")
            f.write("\\hline\n")

    repo_data = []

    def record_type_warning_count(repo_path, repo_name, counts, current_failure):
        if not args.type_warnings or current_failure:
            return current_failure

        count, failure, counter_output = count_type_warnings(repo_path)
        if failure:
            status(f"Warning: failed to count type warnings for {repo_name}: {failure}.")
            if counter_output:
                status(counter_output)
            return failure

        counts.append(count)
        return None

    for repo in repositories:
        repo_path = repo["path"]
        checkout_path = repo["checkout_path"]
        repo_name = repo["name"]
        if not should_process_repo(repo_name, selected_repos):
            continue
        sync_source_path = sync_source_dir / repo["dir"] if sync_source_dir is not None else None
        if not sync_repo_to_source(
            checkout_path,
            sync_source_path,
            repo_name,
            status,
            sync_commit_changes=not args.no_rebuild_on_commit_change,
        ):
            continue
        if not repo_path.exists():
            status(f"Warning: {repo_path} missing, skipping.")
            continue
        deps_ok, deps_failure = ensure_deps_compiled(
            repo_path,
            repo_name,
            elixir_cache_key,
            status,
            args.deps_compile_timeout,
            rebuild_on_commit_change=not args.no_rebuild_on_commit_change,
        )
        if not deps_ok:
            if args.tc_table:
                tc_status = deps_failure or "dependency setup failed"
                status(f"Warning: {repo_name} dependency setup failed; adding failure to TC table.")
                repo_data.append(tc_status_row(repo_path, repo_name, tc_status))
            continue
        status(f"Processing {repo_name} in {repo_path}")

        compile_env = None
        if args.guard_exactness:
            compile_env, raw_dir = guard_exactness_compile_env(
                guard_root,
                guard_run_id,
                repo_name,
                repo_path,
            )
            guard_repo_records.append({
                "name": repo_name,
                "repo_path": repo_path,
                "raw_dir": raw_dir,
            })

        with open(perf_path, "a") as perf:
            perf.write(f"Compiling in {repo_path}\n")

        timed_out = False
        tc_status = None
        type_warning_counts = []
        type_warning_failure = None
        if args.serious_run:
            tc_samples = []
            comp_samples = []
            for warmup_idx in range(1, args.serious_warmups + 1):
                status(f"  Warmup {warmup_idx}/{args.serious_warmups}")
                returncode, _ = run_compile(
                    repo_path,
                    perf_path,
                    args.show_output,
                    run_label=f"-- {repo_name} warmup {warmup_idx}/{args.serious_warmups} --",
                    validate_compile_env=not args.no_validate_compile_env,
                    compile_timeout=args.compile_timeout,
                    extra_env=compile_env,
                )
                if returncode != 0:
                    if returncode == COMPILE_TIMEOUT_RETURNCODE and args.tc_table:
                        status(f"Warning: {repo_name} warmup {warmup_idx} timed out; adding timeout to TC table.")
                        timed_out = True
                        break
                    if args.tc_table:
                        tc_status = f"compile failed (exit {returncode})"
                        status(
                            f"Warning: {repo_name} warmup {warmup_idx} failed with "
                            f"exit code {returncode}; adding failure to TC table."
                        )
                        break
                    status(f"Error: {repo_name} warmup {warmup_idx} failed with exit code {returncode}.")
                    sys.exit(returncode or 1)

            if not timed_out and tc_status is None:
                for run_idx in range(1, args.serious_runs + 1):
                    status(f"  Measured run {run_idx}/{args.serious_runs}")
                    returncode, output = run_compile(
                        repo_path,
                        perf_path,
                        args.show_output,
                        run_label=f"-- {repo_name} measured run {run_idx}/{args.serious_runs} --",
                        validate_compile_env=not args.no_validate_compile_env,
                        compile_timeout=args.compile_timeout,
                        extra_env=compile_env,
                    )
                    if returncode != 0:
                        if returncode == COMPILE_TIMEOUT_RETURNCODE and args.tc_table:
                            status(f"Warning: {repo_name} measured run {run_idx} timed out; adding timeout to TC table.")
                            timed_out = True
                            break
                        if args.tc_table:
                            tc_status = f"compile failed (exit {returncode})"
                            status(
                                f"Warning: {repo_name} measured run {run_idx} failed with "
                                f"exit code {returncode}; adding failure to TC table."
                            )
                            break
                        status(f"Error: {repo_name} measured run {run_idx} failed with exit code {returncode}.")
                        sys.exit(returncode or 1)

                    tc_time, comp_time = extract_compile_metrics(output)
                    if tc_time is None or comp_time is None:
                        status(f"Error: failed to parse profiling output for {repo_name} measured run {run_idx}.")
                        sys.exit(1)
                    tc_samples.append(tc_time)
                    comp_samples.append(comp_time)
                    type_warning_failure = record_type_warning_count(
                        repo_path,
                        repo_name,
                        type_warning_counts,
                        type_warning_failure,
                    )
        else:
            returncode, output = run_compile(
                repo_path,
                perf_path,
                args.show_output,
                run_label=f"-- {repo_name} single run --",
                validate_compile_env=not args.no_validate_compile_env,
                compile_timeout=args.compile_timeout,
                extra_env=compile_env,
            )
            if returncode != 0:
                if returncode == COMPILE_TIMEOUT_RETURNCODE and args.tc_table:
                    status(f"Warning: {repo_name} timed out; adding timeout to TC table.")
                    timed_out = True
                elif args.tc_table:
                    tc_status = f"compile failed (exit {returncode})"
                    status(
                        f"Warning: compile failed for {repo_name} with exit code "
                        f"{returncode}; adding failure to TC table."
                    )
                else:
                    status(f"Warning: compile failed for {repo_name} with exit code {returncode}; skipping.")
                    with open(perf_path, "a") as perf:
                        perf.write("-------------------------\n")
                    continue
            if not timed_out and tc_status is None:
                tc_time, comp_time = extract_compile_metrics(output)
                if tc_time is None or comp_time is None:
                    status(f"Warning: failed to parse profiling output for {repo_name}; using 0.0 values.")
                    tc_time = tc_time if tc_time is not None else 0.0
                    comp_time = comp_time if comp_time is not None else 0.0
                type_warning_failure = record_type_warning_count(
                    repo_path,
                    repo_name,
                    type_warning_counts,
                    type_warning_failure,
                )

        with open(perf_path, "a") as perf:
            perf.write("-------------------------\n")

        loc = count_loc(repo_path)
        files = count_files(repo_path)
        modules = count_modules(repo_path)
        if tc_status:
            row = {
                "loc": loc,
                "name": repo_name,
                "files": files,
                "modules": modules,
                "tc_status": tc_status,
            }
        elif timed_out:
            row = {
                "loc": loc,
                "name": repo_name,
                "files": files,
                "modules": modules,
                "timed_out": True,
                "timeout_seconds": args.compile_timeout,
            }
        elif args.serious_run:
            tc_stats = summarize_samples(tc_samples)
            comp_stats = summarize_samples(comp_samples)
            row = {
                "loc": loc,
                "name": repo_name,
                "files": files,
                "modules": modules,
                "tc_mean": tc_stats["mean"],
                "tc_ci95": tc_stats["ci95"],
                "comp_mean": comp_stats["mean"],
                "comp_ci95": comp_stats["ci95"],
                "n": tc_stats["n"],
            }
        else:
            row = {
                "loc": loc,
                "name": repo_name,
                "files": files,
                "modules": modules,
                "tc_time": tc_time,
                "comp_time": comp_time,
            }

        if args.type_warnings:
            row.update(summarize_type_warning_counts(type_warning_counts, type_warning_failure))

        repo_data.append(row)
        status(f"  TC time: {format_tc_value(row, args.serious_run)}")
        if args.type_warnings:
            status(f"  Type warnings: {format_type_warnings_value(row)}")

    repo_data.sort(key=lambda r: r["loc"], reverse=True)

    if args.tc_table:
        result_path.write_text(format_tc_table(repo_data, args.serious_run, args.type_warnings))
    else:
        with open(result_path, "a") as f:
            for i, row in enumerate(repo_data, start=1):
                color = "\\rowcolor{violet1}" if i % 2 == 0 else ""
                if color:
                    f.write(color + "\n")
                if args.serious_run:
                    row_text = (
                        f"{row['name']} & {row['loc']:,} & {row['files']} & {row['modules']} & "
                        f"{row['tc_mean']:.3f} +- {row['tc_ci95']:.3f} s & "
                        f"{row['comp_mean']:.3f} +- {row['comp_ci95']:.3f} s"
                    )
                else:
                    row_text = (
                        f"{row['name']} & {row['loc']:,} & {row['files']} & {row['modules']} & "
                        f"{row['tc_time']:.3f} s & {row['comp_time']:.3f} s"
                    )
                if args.type_warnings:
                    row_text += f" & {format_type_warnings_value(row)}"
                f.write(f"{row_text} \\\\\n")

            f.write("\n\\hline\n\\end{tabular}\n\\end{center}\n")

    if args.guard_exactness:
        write_guard_exactness_outputs(
            guard_root,
            guard_repo_records,
            elixir_version,
            elixir_git,
            args,
            status,
        )

    if args.tc_table:
        print()
        print(result_path.read_text())
    else:
        print(f"\nCompilation complete. Results saved to {result_path}")
        print(result_path.read_text())


if __name__ == "__main__":
    main()
