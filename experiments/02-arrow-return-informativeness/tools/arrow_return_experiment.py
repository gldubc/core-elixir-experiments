#!/usr/bin/env python3
import argparse
import csv
import json
import os
import subprocess
import sys
from pathlib import Path


REPOSITORIES = [
    {"name": "HexPm", "dir": "hexpm", "url": "https://github.com/hexpm/hexpm.git"},
    {"name": "Phoenix", "dir": "phoenix", "url": "https://github.com/phoenixframework/phoenix.git"},
    {
        "name": "PhoenixLiveView",
        "dir": "phoenix_live_view",
        "url": "https://github.com/phoenixframework/phoenix_live_view.git",
    },
    {"name": "Livebook", "dir": "livebook", "url": "https://github.com/livebook-dev/livebook.git"},
    {"name": "Credo", "dir": "credo", "url": "https://github.com/rrrene/credo.git"},
    {"name": "ExDoc", "dir": "ex_doc", "url": "https://github.com/elixir-lang/ex_doc.git"},
    {"name": "Nerves", "dir": "nerves", "url": "https://github.com/nerves-project/nerves.git"},
    {"name": "Ecto", "dir": "ecto", "url": "https://github.com/elixir-ecto/ecto.git"},
    {"name": "Postgrex", "dir": "postgrex", "url": "https://github.com/elixir-ecto/postgrex.git"},
    {"name": "Flame", "dir": "flame", "url": "https://github.com/phoenixframework/flame.git"},
    {"name": "Ash", "dir": "ash", "url": "https://github.com/ash-project/ash.git"},
    {"name": "Spitfire", "dir": "spitfire", "url": "https://github.com/elixir-tools/spitfire.git"},
    {"name": "SQL", "dir": "sql", "url": "https://github.com/elixir-dbvisor/sql.git"},
    {
        "name": "OpenApiSpex",
        "dir": "open_api_spex",
        "url": "https://github.com/open-api-spex/open_api_spex.git",
    },
    {"name": "MixSBOM", "dir": "mix_sbom", "url": "https://github.com/erlef/mix_sbom.git"},
    {
        "name": "AbsintheFederation",
        "dir": "absinthe_federation",
        "url": "https://github.com/DivvyPayHQ/absinthe_federation.git",
    },
    {"name": "Blockscout", "dir": "blockscout", "url": "https://github.com/blockscout/blockscout.git"},
]

SUMMARY_FIELDS = [
    "Codebase",
    "LoC",
    "Function values",
    "Named",
    "Anonymous",
    "Arrows",
    "Informative returns",
    "Exact dynamic returns",
    "Informative %",
]

INTEGER_FIELDS = [
    "LoC",
    "Function values",
    "Named",
    "Anonymous",
    "Arrows",
    "Informative returns",
    "Exact dynamic returns",
]

EXPECTED_TOTAL = {
    "LoC": 517999,
    "Function values": 57258,
    "Named": 40608,
    "Anonymous": 16650,
    "Arrows": 69976,
    "Informative returns": 43158,
    "Exact dynamic returns": 26818,
    "Informative %": 61.68,
}

EXPECTED_CODEBASES = {
    "AbsintheFederation",
    "Ash",
    "Blockscout",
    "Credo",
    "Ecto",
    "ExDoc",
    "Flame",
    "HexPm",
    "Livebook",
    "MixSBOM",
    "Nerves",
    "OpenApiSpex",
    "Phoenix",
    "PhoenixLiveView",
    "Postgrex",
    "SQL",
    "Spitfire",
}


def require(condition, message):
    if not condition:
        raise SystemExit(f"validation failed: {message}")


def ratio_percent(informative, total):
    return round(informative / total * 100, 2) if total else 0.0


def parse_int(row, field):
    return int(row[field].replace(",", ""))


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


def read_summary(path):
    with Path(path).open(newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        require(reader.fieldnames == SUMMARY_FIELDS, f"unexpected summary fields in {path}")
        return list(reader)


def validate_summary(summary_path):
    rows = read_summary(summary_path)
    total_rows = [row for row in rows if row["Codebase"] == "TOTAL"]
    project_rows = [row for row in rows if row["Codebase"] != "TOTAL"]

    require(len(total_rows) == 1, "expected one TOTAL row")
    require(len(project_rows) == 17, "expected 17 project rows")
    require({row["Codebase"] for row in project_rows} == EXPECTED_CODEBASES, "project set mismatch")

    total = total_rows[0]
    sums = {field: sum(parse_int(row, field) for row in project_rows) for field in INTEGER_FIELDS}
    for field, value in sums.items():
        require(parse_int(total, field) == value, f"bad TOTAL {field}")
        require(value == EXPECTED_TOTAL[field], f"unexpected aggregate {field}")

    for row in project_rows + [total]:
        arrows = parse_int(row, "Arrows")
        informative = parse_int(row, "Informative returns")
        exact_dynamic = parse_int(row, "Exact dynamic returns")
        require(informative + exact_dynamic == arrows, f"arrow partition mismatch for {row['Codebase']}")
        expected_ratio = ratio_percent(informative, arrows)
        reported_ratio = float(row["Informative %"])
        require(
            abs(reported_ratio - expected_ratio) < 0.005,
            f"bad informative ratio for {row['Codebase']}",
        )

    require(abs(float(total["Informative %"]) - EXPECTED_TOTAL["Informative %"]) < 0.005, "bad total ratio")
    print(
        "arrow-return summary validation passed: "
        f"{parse_int(total, 'Arrows')} arrows, "
        f"{parse_int(total, 'Informative returns')} informative "
        f"({float(total['Informative %']):.2f}%)"
    )


def repo_name_for_file(file_name, repo_paths):
    path = Path(file_name)
    if not path.is_absolute():
        raise ValueError(f"could not map record to a known repository: {file_name}")

    resolved = path.resolve(strict=False)
    for name, repo_path in repo_paths.items():
        try:
            resolved.relative_to(repo_path)
            return name
        except ValueError:
            pass
    raise ValueError(f"could not map record to a known repository: {file_name}")


def aggregate_raw(raw_paths, repos_root):
    repos_root = Path(repos_root)
    repo_paths = {
        repo["name"]: (repos_root / repo["dir"]).resolve(strict=False)
        for repo in REPOSITORIES
    }
    rows = {
        repo["name"]: {
            "Codebase": repo["name"],
            "LoC": count_loc(repos_root / repo["dir"]),
            "Function values": 0,
            "Named": 0,
            "Anonymous": 0,
            "Arrows": 0,
            "Informative returns": 0,
            "Exact dynamic returns": 0,
        }
        for repo in REPOSITORIES
    }

    skipped_relative = 0
    for raw_path in raw_paths:
        with Path(raw_path).open(encoding="utf-8") as file:
            for line_number, line in enumerate(file, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                    name = repo_name_for_file(record["file"], repo_paths)
                except ValueError as exc:
                    if not Path(record.get("file", "")).is_absolute():
                        skipped_relative += 1
                        continue
                    raise SystemExit(f"{raw_path}:{line_number}: {exc}") from exc
                except (KeyError, json.JSONDecodeError) as exc:
                    raise SystemExit(f"{raw_path}:{line_number}: {exc}") from exc

                row = rows[name]
                row["Function values"] += 1
                if record.get("kind") == "anonymous":
                    row["Anonymous"] += 1
                else:
                    row["Named"] += 1
                row["Arrows"] += int(record["total_arrows"])
                row["Informative returns"] += int(record["informative_arrows"])
                row["Exact dynamic returns"] += int(record["exact_dynamic_arrows"])

    if skipped_relative:
        print(f"skipped {skipped_relative} records with relative file paths that do not name a project")

    project_rows = [row for row in rows.values() if row["Function values"] > 0]
    project_rows.sort(key=lambda row: (-row["LoC"], row["Codebase"]))

    total = {"Codebase": "TOTAL"}
    for field in INTEGER_FIELDS:
        total[field] = sum(row[field] for row in project_rows)
    return project_rows + [total]


def format_percent(row):
    return f"{ratio_percent(row['Informative returns'], row['Arrows']):.2f}"


def write_csv(rows, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=SUMMARY_FIELDS, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            output = dict(row)
            output["Informative %"] = format_percent(row)
            writer.writerow(output)


def fmt_int(value):
    return f"{value:,}"


def write_markdown(rows, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "| Codebase | LoC | Function values | Arrows | Informative returns | Exact dynamic returns | Informative % |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            "| "
            f"{row['Codebase']} | {fmt_int(row['LoC'])} | {fmt_int(row['Function values'])} | "
            f"{fmt_int(row['Arrows'])} | {fmt_int(row['Informative returns'])} | "
            f"{fmt_int(row['Exact dynamic returns'])} | {ratio_percent(row['Informative returns'], row['Arrows']):.1f}% |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def summarize(args):
    raw_paths = [Path(path) for path in args.raw_jsonl]
    if args.raw_dir:
        raw_paths.extend(sorted(Path(args.raw_dir).glob("*.jsonl")))
    require(raw_paths, "provide --raw-jsonl or --raw-dir")
    rows = aggregate_raw(raw_paths, args.repos_root)
    write_csv(rows, Path(args.output_dir) / "summary.csv")
    write_markdown(rows, Path(args.output_dir) / "summary.md")
    validate_summary(Path(args.output_dir) / "summary.csv")


def run_command(command, cwd, env, timeout, log_path):
    print("$", " ".join(command), f"(cwd={cwd})", flush=True)
    with log_path.open("w", encoding="utf-8") as log:
        process = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            stdout=log,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
    return process.returncode


def git(args, cwd=None):
    print("$ git", " ".join(args), flush=True)
    subprocess.run(["git", *args], cwd=cwd, check=True)


def checkout_projects(args):
    repos_root = Path(args.repos_root)
    repos_root.mkdir(parents=True, exist_ok=True)

    with Path(args.projects_csv).open(newline="", encoding="utf-8") as file:
        rows = list(csv.DictReader(file))

    for row in rows:
        repo_dir = repos_root / row["Repo dir"]
        if not (repo_dir / ".git").is_dir():
            git(["clone", row["Repository"], str(repo_dir)])
        git(["fetch", "--depth=1", "origin", row["Commit"]], cwd=repo_dir)
        git(["checkout", "--detach", row["Commit"]], cwd=repo_dir)
        git(["reset", "--hard", row["Commit"]], cwd=repo_dir)
        git(["clean", "-fdx"], cwd=repo_dir)


def selected_repositories(names):
    if not names:
        return REPOSITORIES
    selected = []
    by_name = {repo["name"]: repo for repo in REPOSITORIES}
    for name in names:
        require(name in by_name, f"unknown repository {name}")
        selected.append(by_name[name])
    return selected


def run_experiment(args):
    elixir_root = Path(args.elixir_root).resolve()
    repos_root = Path(args.repos_root).resolve()
    output_dir = Path(args.output_dir)
    raw_dir = output_dir / "raw"
    log_dir = output_dir / "logs"
    raw_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    mix = elixir_root / "bin" / "mix"
    require(mix.is_file(), f"missing mix executable: {mix}")

    env_base = os.environ.copy()
    env_base["PATH"] = f"{elixir_root / 'bin'}{os.pathsep}{env_base.get('PATH', '')}"

    for repo in selected_repositories(args.repo):
        repo_path = repos_root / repo["dir"]
        require((repo_path / "mix.exs").is_file(), f"missing mix.exs for {repo['name']}: {repo_path}")
        raw_path = raw_dir / f"{repo['dir']}.raw.jsonl"
        raw_path.unlink(missing_ok=True)

        env = dict(env_base)
        env["ELIXIR_TYPE_METRICS_ARROW_RETURN"] = str(raw_path)
        if args.deps_get:
            run_command([str(mix), "deps.get"], repo_path, env, args.compile_timeout, log_dir / f"{repo['dir']}-deps.log")
        status = run_command(
            [str(mix), "compile", "--force", "--no-validate-compile-env"],
            repo_path,
            env,
            args.compile_timeout,
            log_dir / f"{repo['dir']}.log",
        )
        if status != 0:
            print(f"{repo['name']} compile exited with status {status}; keeping any metrics emitted before exit")

    rows = aggregate_raw(sorted(raw_dir.glob("*.jsonl")), repos_root)
    write_csv(rows, output_dir / "summary.csv")
    write_markdown(rows, output_dir / "summary.md")
    print(f"wrote {output_dir / 'summary.csv'}")


def build_parser():
    parser = argparse.ArgumentParser(description="Run or validate the arrow-return informativeness experiment")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate the committed summary table")
    validate_parser.add_argument("--summary", required=True)
    validate_parser.set_defaults(func=lambda args: validate_summary(args.summary))

    summarize_parser = subparsers.add_parser("summarize", help="Aggregate raw JSONL metrics into summary tables")
    summarize_parser.add_argument("--raw-jsonl", action="append", default=[])
    summarize_parser.add_argument("--raw-dir")
    summarize_parser.add_argument("--repos-root", required=True)
    summarize_parser.add_argument("--output-dir", required=True)
    summarize_parser.set_defaults(func=summarize)

    run_parser = subparsers.add_parser("run", help="Compile project checkouts and collect raw metrics")
    run_parser.add_argument("--elixir-root", required=True)
    run_parser.add_argument("--repos-root", required=True)
    run_parser.add_argument("--output-dir", required=True)
    run_parser.add_argument("--repo", action="append", help="Run one codebase by display name; repeatable")
    run_parser.add_argument("--compile-timeout", type=int, default=60)
    run_parser.add_argument("--deps-get", action="store_true")
    run_parser.set_defaults(func=run_experiment)

    checkout_parser = subparsers.add_parser("checkout-projects", help="Clone project checkouts at archived commits")
    checkout_parser.add_argument("--projects-csv", required=True)
    checkout_parser.add_argument("--repos-root", required=True)
    checkout_parser.set_defaults(func=checkout_projects)
    return parser


def main(argv):
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main(sys.argv[1:])
