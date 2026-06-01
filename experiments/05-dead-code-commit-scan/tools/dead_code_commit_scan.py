#!/usr/bin/env python3
import argparse
import csv
import subprocess
from collections import Counter, defaultdict
from pathlib import Path


START_DATE = "2024-05-01 00:00:00"

REMOVED_CODE_TERMS = [
    "dead code",
    "unused",
    "unused clause",
    "unused clauses",
    "unused branch",
    "unused branches",
    "unreachable",
    "non-reachable",
    "redundant",
    "useless",
    "unneeded",
    "unnecessary",
]

TYPE_COMPILER_TERMS = [
    "type system",
    "typesystem",
    "type-system",
    "type checker",
    "typechecker",
    "type-checker",
    "type warning",
    "type warnings",
    "compiler",
    "warning",
    "warnings",
    "elixir 1.17",
    "elixir 1.18",
    "elixir 1.19",
    "elixir 1.20",
    "latest elixir",
    "is never used",
    "will never match",
    "can never succeed",
    "will always evaluate",
]

EXPECTED_TOTALS = {
    "Direct": {"commits": 9, "lines": 91},
    "Warning-linked": {"commits": 5, "lines": 88},
    "ALL": {"commits": 14, "lines": 179},
}


def require(condition, message):
    if not condition:
        raise SystemExit(f"validation failed: {message}")


def run_git(repo, args, check=True):
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        check=False,
    )
    if check and result.returncode != 0:
        raise SystemExit(
            f"git command failed in {repo}: git {' '.join(args)}\n{result.stderr.strip()}"
        )
    return result


def read_csv(path):
    with Path(path).open(newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


def write_tsv(path, fieldnames, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def experiment_dir():
    return Path(__file__).resolve().parents[1]


def default_results_dir():
    return experiment_dir() / "results"


def int_field(row, key):
    return int(row[key].replace(",", ""))


def validate(args):
    results_dir = Path(args.results_dir)
    repositories = read_csv(results_dir / "repositories.csv")
    accepted = read_csv(results_dir / "accepted_commits.csv")
    summary = read_csv(results_dir / "project_summary.csv")

    require(len(repositories) == 17, "expected 17 repositories")
    scanned = sum(int_field(row, "non_merge_commits_since_2024_05_01") for row in repositories)
    require(scanned == 7151, f"expected 7,151 scanned commits, got {scanned}")

    bucket_counts = Counter(row["bucket"] for row in accepted)
    bucket_lines = Counter()
    project_totals = defaultdict(lambda: Counter())
    for row in accepted:
        bucket = row["bucket"]
        lines = int_field(row, "deleted_lines")
        bucket_lines[bucket] += lines
        project = row["project"]
        if bucket == "Direct":
            project_totals[project]["direct_commits"] += 1
            project_totals[project]["direct_lines"] += lines
        elif bucket == "Warning-linked":
            project_totals[project]["warning_linked_commits"] += 1
            project_totals[project]["warning_linked_lines"] += lines
        else:
            raise SystemExit(f"unknown bucket: {bucket}")
        project_totals[project]["total_commits"] += 1
        project_totals[project]["total_lines"] += lines

    for bucket, expected in EXPECTED_TOTALS.items():
        if bucket == "ALL":
            commits = len(accepted)
            lines = sum(int_field(row, "deleted_lines") for row in accepted)
        else:
            commits = bucket_counts[bucket]
            lines = bucket_lines[bucket]
        require(commits == expected["commits"], f"bad {bucket} commit count")
        require(lines == expected["lines"], f"bad {bucket} deleted-line count")

    for row in summary:
        project = row["project"]
        expected = Counter(
            {
                "direct_commits": int_field(row, "direct_commits"),
                "direct_lines": int_field(row, "direct_lines"),
                "warning_linked_commits": int_field(row, "warning_linked_commits"),
                "warning_linked_lines": int_field(row, "warning_linked_lines"),
                "total_commits": int_field(row, "total_commits"),
                "total_lines": int_field(row, "total_lines"),
            }
        )
        if project == "TOTAL":
            actual = Counter(
                {
                    "direct_commits": bucket_counts["Direct"],
                    "direct_lines": bucket_lines["Direct"],
                    "warning_linked_commits": bucket_counts["Warning-linked"],
                    "warning_linked_lines": bucket_lines["Warning-linked"],
                    "total_commits": len(accepted),
                    "total_lines": sum(int_field(item, "deleted_lines") for item in accepted),
                }
            )
        else:
            actual = project_totals[project]
        require(actual == expected, f"project summary mismatch for {project}")

    print(
        "dead-code commit scan validation passed: "
        "14 commits, 179 deleted lines "
        "(9 direct/91, 5 warning-linked/88)"
    )


def term_hits(text, terms):
    lowered = text.lower()
    return [term for term in terms if term in lowered]


def find_repo_dir(row, roots):
    for root in roots:
        candidate = Path(root) / row["repo_dir"]
        if (candidate / ".git").is_dir():
            return candidate
    return None


def ensure_repo(row, roots, clone_missing):
    repo = find_repo_dir(row, roots)
    if repo is not None:
        return repo

    if not clone_missing:
        raise SystemExit(
            f"missing checkout for {row['project']} ({row['repo_dir']}); "
            "pass --clone-missing or add another --repos-root"
        )

    root = Path(roots[0])
    root.mkdir(parents=True, exist_ok=True)
    repo = root / row["repo_dir"]
    print(f"cloning {row['repo_url']} -> {repo}")
    subprocess.run(["git", "clone", row["repo_url"], str(repo)], check=True)
    return repo


def commit_records(repo, rev):
    fmt = "%H%x1f%ad%x1f%s%x1f%b%x1e"
    result = run_git(
        repo,
        [
            "log",
            f"--since={START_DATE}",
            "--no-merges",
            "--date=short",
            f"--format={fmt}",
            rev,
        ],
    )
    for raw in result.stdout.split("\x1e"):
        raw = raw.strip("\n")
        if not raw:
            continue
        parts = raw.split("\x1f", 3)
        if len(parts) != 4:
            raise SystemExit(f"could not parse git log record in {repo}: {raw!r}")
        commit, date, subject, body = parts
        yield {"commit": commit, "date": date, "subject": subject, "body": body}


def elixir_numstat_deletions(repo, commit):
    result = run_git(
        repo,
        [
            "show",
            "--numstat",
            "--format=",
            commit,
            "--",
            "*.ex",
            "*.exs",
            "*.heex",
            "*.eex",
        ],
    )
    deletions = 0
    for line in result.stdout.splitlines():
        fields = line.split("\t")
        if len(fields) < 3 or fields[1] == "-":
            continue
        deletions += int(fields[1])
    return deletions


def full_subject(repo, commit):
    return run_git(repo, ["show", "--quiet", "--format=%s", commit]).stdout.strip()


def scan(args):
    results_dir = Path(args.results_dir)
    repositories = read_csv(results_dir / "repositories.csv")
    accepted = read_csv(results_dir / "accepted_commits.csv")
    roots = [Path(root) for root in args.repos_root]
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    candidate_rows = []
    accepted_rows = []
    scanned_total = 0

    repos_by_dir = {}
    for row in repositories:
        repo = ensure_repo(row, roots, args.clone_missing)
        repos_by_dir[row["repo_dir"]] = repo
        records = list(commit_records(repo, row["scan_commit"]))
        scanned_total += len(records)

        for record in records:
            text = f"{record['subject']}\n{record['body']}"
            removed = term_hits(text, REMOVED_CODE_TERMS)
            typed = term_hits(text, TYPE_COMPILER_TERMS)
            if not (removed or typed):
                continue
            if removed and typed:
                candidate_kind = "removed-code-and-type"
            elif removed:
                candidate_kind = "removed-code-only"
            else:
                candidate_kind = "type-or-warning-only"
            candidate_rows.append(
                {
                    "project": row["project"],
                    "commit": record["commit"],
                    "date": record["date"],
                    "candidate_kind": candidate_kind,
                    "removed_code_terms": ";".join(removed),
                    "type_compiler_terms": ";".join(typed),
                    "subject": record["subject"],
                }
            )

    candidate_commits = {row["commit"] for row in candidate_rows}
    for row in accepted:
        repo = repos_by_dir.get(row["repo_dir"]) or ensure_repo(row, roots, args.clone_missing)
        subject = full_subject(repo, row["commit"])
        counted = int_field(row, "deleted_lines")
        numstat = elixir_numstat_deletions(repo, row["commit"])
        if row["count_mode"] == "elixir_numstat":
            status = "ok" if numstat == counted else "count-mismatch"
        elif row["count_mode"] == "manual_hunks":
            status = "ok" if numstat >= counted else "manual-count-too-large"
        else:
            status = f"unknown-count-mode:{row['count_mode']}"
        accepted_rows.append(
            {
                "project": row["project"],
                "commit": row["commit"],
                "bucket": row["bucket"],
                "count_mode": row["count_mode"],
                "counted_deleted_lines": counted,
                "elixir_numstat_deletions": numstat,
                "in_keyword_candidates": "yes" if row["commit"] in candidate_commits else "no",
                "status": status,
                "subject": subject,
            }
        )

    write_tsv(
        output_dir / "keyword-candidates.tsv",
        [
            "project",
            "commit",
            "date",
            "candidate_kind",
            "removed_code_terms",
            "type_compiler_terms",
            "subject",
        ],
        candidate_rows,
    )
    write_tsv(
        output_dir / "accepted-verification.tsv",
        [
            "project",
            "commit",
            "bucket",
            "count_mode",
            "counted_deleted_lines",
            "elixir_numstat_deletions",
            "in_keyword_candidates",
            "status",
            "subject",
        ],
        accepted_rows,
    )

    bad = [row for row in accepted_rows if row["status"] != "ok"]
    missing = [row for row in accepted_rows if row["in_keyword_candidates"] != "yes"]
    summary = [
        f"scanned_commits\t{scanned_total}",
        f"keyword_candidates\t{len(candidate_rows)}",
        f"accepted_commits\t{len(accepted_rows)}",
        f"accepted_count_problems\t{len(bad)}",
        f"accepted_not_in_keyword_candidates\t{len(missing)}",
    ]
    (output_dir / "scan-summary.tsv").write_text("\n".join(summary) + "\n", encoding="utf-8")

    if bad:
        details = ", ".join(f"{row['project']} {row['commit'][:7]}" for row in bad)
        raise SystemExit(f"accepted count verification failed for: {details}")

    print(
        f"dead-code keyword scan wrote {len(candidate_rows)} candidates "
        f"and verified {len(accepted_rows)} accepted commits under {output_dir}"
    )
    if missing:
        print(
            "note: accepted commits not in broad keyword candidates: "
            + ", ".join(f"{row['project']} {row['commit'][:7]}" for row in missing)
        )


def main():
    parser = argparse.ArgumentParser(description="Dead-code commit-scan artifact driver")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="validate committed result tables")
    validate_parser.add_argument("--results-dir", default=default_results_dir())
    validate_parser.set_defaults(func=validate)

    scan_parser = subparsers.add_parser("scan", help="rerun the keyword scan against git checkouts")
    scan_parser.add_argument("--results-dir", default=default_results_dir())
    scan_parser.add_argument("--repos-root", action="append", required=True)
    scan_parser.add_argument("--output-dir", required=True)
    scan_parser.add_argument("--clone-missing", action="store_true")
    scan_parser.set_defaults(func=scan)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
