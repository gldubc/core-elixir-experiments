#!/usr/bin/env python3
import csv
import json
import sys
from pathlib import Path


PAPER_PROJECTS = {"ElixirStdlib", "Phoenix", "Ecto", "PhoenixLiveView", "Postgrex", "Flame"}


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def require(condition, message):
    if not condition:
        raise SystemExit(f"validation failed: {message}")


def ratio_percent(exact, analyzed):
    return round(exact / analyzed * 100, 2)


def main(argv):
    if len(argv) != 2:
        raise SystemExit("usage: validate_guard_exactness.py RESULTS_DIR")

    results_dir = Path(argv[1])
    summary = read_csv(results_dir / "guard_exactness_summary.csv")
    projects = read_csv(results_dir / "projects.csv")
    ept = read_csv(results_dir / "ept_corpus_table.csv")
    paper = read_csv(results_dir / "paper_projects.csv")
    metadata = json.loads((results_dir / "metadata.json").read_text(encoding="utf-8"))

    require(len(summary) == 18, "expected 18 projects in guard_exactness_summary.csv")
    require(len(projects) == 18, "expected 18 projects in projects.csv")
    require(len(ept) == 17, "expected 17 projects in ept corpus table")
    require({row["project"] for row in paper} == PAPER_PROJECTS, "paper project set mismatch")

    by_project = {row["project"]: row for row in projects}
    require(all(int(row["analyzed_pairs"]) > 0 for row in projects), "all projects must have rows")
    require(by_project["SQL"]["compile_status"] == "timeout after 60s", "SQL timeout status missing")

    for row in projects:
        analyzed = int(row["analyzed_pairs"])
        exact = int(row["exact_pairs"])
        reported = float(row["exactness_percent"])
        require(reported == ratio_percent(exact, analyzed), f"bad exactness percent for {row['project']}")

    ept_analyzed = sum(int(row["analyzed_pairs"]) for row in ept)
    ept_exact = sum(int(row["exact_pairs"]) for row in ept)
    paper_analyzed = sum(int(row["analyzed_pairs"]) for row in paper)
    paper_exact = sum(int(row["exact_pairs"]) for row in paper)
    all_analyzed = sum(int(row["analyzed_pairs"]) for row in projects)
    all_exact = sum(int(row["exact_pairs"]) for row in projects)

    aggregate = metadata["aggregate"]
    require(aggregate["ept_corpus_without_stdlib"]["analyzed_pairs"] == ept_analyzed, "bad ept analyzed aggregate")
    require(aggregate["ept_corpus_without_stdlib"]["exact_pairs"] == ept_exact, "bad ept exact aggregate")
    require(aggregate["paper_projects"]["analyzed_pairs"] == paper_analyzed, "bad paper analyzed aggregate")
    require(aggregate["paper_projects"]["exact_pairs"] == paper_exact, "bad paper exact aggregate")
    require(aggregate["all_projects_including_stdlib"]["analyzed_pairs"] == all_analyzed, "bad all analyzed aggregate")
    require(aggregate["all_projects_including_stdlib"]["exact_pairs"] == all_exact, "bad all exact aggregate")

    print("guard exactness summary validation passed")


if __name__ == "__main__":
    main(sys.argv)
