#!/usr/bin/env python3
import argparse
import csv
import datetime
import importlib.util
import re
import subprocess
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
EXPERIMENT_DIR = SCRIPT_DIR.parent
PROJECTS_CSV = EXPERIMENT_DIR / "results" / "projects.csv"
PERF_PY = SCRIPT_DIR / "perf.py"


def run(cmd, cwd=None):
    print("$", " ".join(str(part) for part in cmd), flush=True)
    return subprocess.run(cmd, cwd=cwd)


def repo_slug(elixir_root):
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", Path(elixir_root).resolve().name).strip("-")
    return slug or "worktree"


def load_projects():
    with PROJECTS_CSV.open(newline="", encoding="utf-8") as file:
        return {
            row["project"]: row
            for row in csv.DictReader(file)
            if row["project"] != "ElixirStdlib"
        }


def selected_projects(projects, selected):
    if not selected:
        return list(projects.values())

    missing = sorted(set(selected) - set(projects))
    if missing:
        raise SystemExit(f"unknown repos: {', '.join(missing)}")

    return [projects[name] for name in selected]


def ensure_checkout(row, repos_dir):
    checkout = repos_dir / row["repo_dir"]
    if not (checkout / ".git").is_dir():
        checkout.parent.mkdir(parents=True, exist_ok=True)
        if checkout.exists():
            raise SystemExit(f"{checkout} exists but is not a git repository")
        result = run(["git", "clone", row["repo_url"], str(checkout)])
        if result.returncode != 0:
            raise SystemExit(result.returncode)

    result = run(["git", "fetch", "origin", row["commit"]], cwd=checkout)
    if result.returncode != 0:
        result = run(["git", "fetch", "--all", "--prune"], cwd=checkout)
        if result.returncode != 0:
            raise SystemExit(result.returncode)

    result = run(["git", "checkout", "--detach", row["commit"]], cwd=checkout)
    if result.returncode != 0:
        raise SystemExit(result.returncode)

    return checkout


def mix_project_path(checkout, row):
    # The archived corpus used project roots directly. Keep this function
    # separate so future experiments can add umbrella subdirectories here.
    return checkout


def prepare_project(row, repos_dir, system_mix):
    checkout = ensure_checkout(row, repos_dir)
    project_path = mix_project_path(checkout, row)

    result = run([system_mix, "deps.get"], cwd=project_path)
    if result.returncode != 0:
        raise SystemExit(result.returncode)

    spec = importlib.util.spec_from_file_location("_guard_exactness_perf", PERF_PY)
    perf = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(perf)
    if not perf.patch_known_dependency_issues(project_path, row["project"], print):
        raise SystemExit("dependency compatibility patch failed")

    result = run([system_mix, "deps.compile", "--force"], cwd=project_path)
    if result.returncode != 0:
        raise SystemExit(result.returncode)

    sentinel = project_path / "_build" / ".perf-deps-compiled"
    sentinel.parent.mkdir(parents=True, exist_ok=True)
    sentinel.write_text(f"system-deps:{system_mix}:{row['commit']}\n", encoding="utf-8")
    print(f"prepared {row['project']} dependencies with {system_mix}")


def main(argv):
    parser = argparse.ArgumentParser(description="Prepare guard-exactness corpus dependencies with system Mix")
    parser.add_argument("--elixir-root", required=True)
    parser.add_argument("--system-mix", default="mix")
    parser.add_argument("--repos-dir")
    parser.add_argument("-r", "--repo", action="append", default=[])
    args = parser.parse_args(argv)

    repos_dir = Path(args.repos_dir) if args.repos_dir else SCRIPT_DIR / f"repos-{repo_slug(args.elixir_root)}"
    projects = load_projects()

    for row in selected_projects(projects, args.repo):
        prepare_project(row, repos_dir, args.system_mix)

    repos_dir.mkdir(parents=True, exist_ok=True)
    (repos_dir / ".perf-last-clean-month").write_text(
        datetime.date.today().strftime("%Y-%m") + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main(sys.argv[1:])
