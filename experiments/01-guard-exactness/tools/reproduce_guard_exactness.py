#!/usr/bin/env python3
import argparse
import datetime
import os
import subprocess
import sys
from pathlib import Path


ELIXIR_COMMIT = "095c1649c59651a959c57ed15628ea3aebc388d3"
SCRIPT_DIR = Path(__file__).resolve().parent
EXPERIMENT_DIR = SCRIPT_DIR.parent
REPO_ROOT = EXPERIMENT_DIR.parents[1]
PATCH = EXPERIMENT_DIR / "compiler-patches" / "guard-instrumentation.patch"
PERF = SCRIPT_DIR / "perf.py"
PREPARE_DEPS = SCRIPT_DIR / "prepare_dependencies.py"


def run(cmd, cwd=None, env=None):
    print("$", " ".join(str(part) for part in cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, env=env, check=True)


def capture_ok(cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def absolute_path(path):
    path = Path(path).expanduser()
    if path.is_absolute():
        return path
    return REPO_ROOT / path


def repo_args(repos):
    args = []
    for repo in repos:
        args.extend(["-r", repo])
    return args


class Reproducer:
    def __init__(self, args):
        self.elixir_root = absolute_path(args.elixir_root)
        self.run_id = args.run_id
        self.run_dir = absolute_path(args.run_dir)
        self.compile_timeout = args.compile_timeout
        self.system_mix = args.system_mix
        self.repos = list(args.repo or [])

    def ensure_elixir(self):
        if not (self.elixir_root / ".git").is_dir():
            if self.elixir_root.exists():
                raise SystemExit(f"{self.elixir_root} exists but is not a git repository")
            self.elixir_root.parent.mkdir(parents=True, exist_ok=True)
            run(["git", "clone", "https://github.com/elixir-lang/elixir.git", str(self.elixir_root)])

        if capture_ok(["git", "apply", "--reverse", "--check", str(PATCH)], cwd=self.elixir_root):
            print(f"instrumentation patch already applied in {self.elixir_root}")
            return

        if not capture_ok(["git", "diff", "--quiet"], cwd=self.elixir_root):
            raise SystemExit(f"refusing to patch dirty Elixir checkout: {self.elixir_root}")
        if not capture_ok(["git", "diff", "--cached", "--quiet"], cwd=self.elixir_root):
            raise SystemExit(f"refusing to patch dirty Elixir checkout: {self.elixir_root}")

        run(["git", "fetch", "origin", ELIXIR_COMMIT], cwd=self.elixir_root)
        run(["git", "checkout", "--detach", ELIXIR_COMMIT], cwd=self.elixir_root)
        run(["git", "apply", str(PATCH)], cwd=self.elixir_root)

    def build_elixir(self):
        run(["make", "-C", str(self.elixir_root)])

    def prepare_dependencies(self):
        run([
            sys.executable,
            str(PREPARE_DEPS),
            "--elixir-root",
            str(self.elixir_root),
            "--system-mix",
            self.system_mix,
            *repo_args(self.repos),
        ])

    def run_external_repos(self):
        self.run_dir.mkdir(parents=True, exist_ok=True)
        run([
            sys.executable,
            str(PERF),
            "--elixir-root",
            str(self.elixir_root),
            "--tc-table",
            "--compile-timeout",
            str(self.compile_timeout),
            "--guard-exactness",
            "--guard-exactness-run-id",
            self.run_id,
            "--guard-exactness-root",
            str(self.run_dir),
            "--no-validate-compile-env",
            "--no-rebuild-on-commit-change",
            *repo_args(self.repos),
        ])

    def run_stdlib(self):
        (self.run_dir / "raw" / "ElixirStdlib").mkdir(parents=True, exist_ok=True)
        run(["make", "-C", str(self.elixir_root), "clean"])
        env = os.environ.copy()
        env.update({
            "ELIXIR_GUARD_EXACTNESS_DIR": str(self.run_dir / "raw" / "ElixirStdlib"),
            "ELIXIR_GUARD_EXACTNESS_PROJECT": "ElixirStdlib",
            "ELIXIR_GUARD_EXACTNESS_REPO_ROOT": str(self.elixir_root),
            "ELIXIR_GUARD_EXACTNESS_RUN_ID": self.run_id,
        })
        run(["make", "-C", str(self.elixir_root), "compile"], env=env)

    def summarize(self):
        run([
            sys.executable,
            str(PERF),
            "--elixir-root",
            str(self.elixir_root),
            "--tc-table",
            "--guard-exactness",
            "--guard-exactness-run-id",
            self.run_id,
            "--guard-exactness-root",
            str(self.run_dir),
            "--guard-exactness-summarize-only",
        ])

    def smoke(self):
        if not self.repos:
            self.repos = ["ExDoc"]
        self.ensure_elixir()
        self.build_elixir()
        self.prepare_dependencies()
        self.run_external_repos()
        self.summarize()

    def full(self):
        self.ensure_elixir()
        self.build_elixir()
        self.prepare_dependencies()
        self.run_external_repos()
        self.run_stdlib()
        self.summarize()


def parse_args(argv):
    parser = argparse.ArgumentParser(description="Reproduce guard-exactness collection")
    parser.add_argument(
        "command",
        choices=["setup", "build", "prepare-deps", "external", "stdlib", "summarize", "smoke", "full"],
        nargs="?",
        default="smoke",
    )
    parser.add_argument("--elixir-root", default="build/elixir-guard-exactness")
    parser.add_argument("--run-id")
    parser.add_argument("--run-dir", default=None)
    parser.add_argument("--compile-timeout", default="60")
    parser.add_argument("--system-mix", default="mix")
    parser.add_argument("-r", "--repo", action="append", default=[])
    args = parser.parse_args(argv)
    if args.run_id is None:
        timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d-%H%M%S")
        args.run_id = f"01-guard-exactness-{timestamp}"
    if args.run_dir is None:
        args.run_dir = f"results/guard-exactness/{args.run_id}"
    return args


def main(argv):
    args = parse_args(argv)
    repro = Reproducer(args)
    command = args.command
    if command == "setup":
        repro.ensure_elixir()
    elif command == "build":
        repro.build_elixir()
    elif command == "prepare-deps":
        repro.prepare_dependencies()
    elif command == "external":
        repro.run_external_repos()
    elif command == "stdlib":
        repro.run_stdlib()
    elif command == "summarize":
        repro.summarize()
    elif command == "smoke":
        repro.smoke()
    elif command == "full":
        repro.full()


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
