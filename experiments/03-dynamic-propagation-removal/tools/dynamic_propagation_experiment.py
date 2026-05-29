#!/usr/bin/env python3
import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path


PROJECTS = [
    {
        "name": "Blockscout",
        "dir": "blockscout",
        "url": "https://github.com/blockscout/blockscout.git",
        "commit": "d9edfc30527a0e5d4ec86f923f20efcd8bfede01",
    },
    {
        "name": "Ash",
        "dir": "ash",
        "url": "https://github.com/ash-project/ash.git",
        "commit": "5790310b740bfaf62ab6ceedc692bfc94c1bab60",
    },
    {
        "name": "Livebook",
        "dir": "livebook",
        "url": "https://github.com/livebook-dev/livebook.git",
        "commit": "b1d98d2b68d4ee998a78f4214232d92b890a652d",
    },
    {
        "name": "HexPm",
        "dir": "hexpm",
        "url": "https://github.com/hexpm/hexpm.git",
        "commit": "50587373a09fd55100961cb9c7501e501db472e5",
    },
    {
        "name": "Ecto",
        "dir": "ecto",
        "url": "https://github.com/elixir-ecto/ecto.git",
        "commit": "cf3a5b7219a552c24aae24bf5eef7354c1184b8a",
    },
    {
        "name": "Credo",
        "dir": "credo",
        "url": "https://github.com/rrrene/credo.git",
        "commit": "2d116684cd4b16b505031a8d84c6ae8ee48617bd",
    },
    {
        "name": "PhoenixLiveView",
        "dir": "phoenix_live_view",
        "url": "https://github.com/phoenixframework/phoenix_live_view.git",
        "commit": "1fedd12dd000ceaf67da6ef26ca5d51dc8a64b54",
    },
    {
        "name": "Phoenix",
        "dir": "phoenix",
        "url": "https://github.com/phoenixframework/phoenix.git",
        "commit": "d8f26700ea167a4e95d1d32314751ae1b5eb74f2",
        "patch": "phoenix-mix-lock.patch",
    },
    {
        "name": "MixSBOM",
        "dir": "mix_sbom",
        "url": "https://github.com/erlef/mix_sbom.git",
        "commit": "c72888d4e1d3f9a7693cc1faf952971216ac1f6a",
    },
    {
        "name": "OpenApiSpex",
        "dir": "open_api_spex",
        "url": "https://github.com/open-api-spex/open_api_spex.git",
        "commit": "f2c71bf320045b76c4bc2ea9a7a056c8d9092197",
    },
    {
        "name": "ExDoc",
        "dir": "ex_doc",
        "url": "https://github.com/elixir-lang/ex_doc.git",
        "commit": "bc909685fd41f0e16f6714403bf520301ef3f28f",
    },
    {
        "name": "Nerves",
        "dir": "nerves",
        "url": "https://github.com/nerves-project/nerves.git",
        "commit": "713da00682c9f70280ee78e00d994115cc9153eb",
        "patch": "nerves-elixir-requirement.patch",
    },
    {
        "name": "Spitfire",
        "dir": "spitfire",
        "url": "https://github.com/elixir-tools/spitfire.git",
        "commit": "47fad18a1bf7ca3ad5bca3b4d06a121e4ddceeb6",
        "patch": "spitfire-mix-lock.patch",
    },
    {
        "name": "SQL",
        "dir": "sql",
        "url": "https://github.com/elixir-dbvisor/sql.git",
        "commit": "bd316cd7b793e4d83b3e3545d506a8b00926dd32",
    },
    {
        "name": "AbsintheFederation",
        "dir": "absinthe_federation",
        "url": "https://github.com/DivvyPayHQ/absinthe_federation.git",
        "commit": "d1735e37509157d0f10116d4f76286b09c86d3a9",
        "patch": "absinthe-federation-warnings-as-errors.patch",
    },
]

EXPECTED_PROJECTS = {
    "AbsintheFederation",
    "Ash",
    "Blockscout",
    "Credo",
    "Ecto",
    "ExDoc",
    "HexPm",
    "Livebook",
    "MixSBOM",
    "Nerves",
    "OpenApiSpex",
    "Phoenix",
    "PhoenixLiveView",
    "SQL",
    "Spitfire",
}

EXPECTED_TOTALS = {
    "Refine": 94,
    "No-dynamic cached deps": 145,
    "Cached - Refine": 51,
}


def run(cmd, cwd=None):
    print("$", " ".join(str(part) for part in cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def require(condition, message):
    if not condition:
        raise SystemExit(f"validation failed: {message}")


def parse_int(text):
    text = text.strip()
    sign = -1 if text.startswith("-") else 1
    text = text.lstrip("+-").replace(",", "")
    return sign * int(text)


def parse_markdown_table(path):
    rows = []
    header = None
    for raw_line in Path(path).read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not (line.startswith("|") and line.endswith("|")):
            continue
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        if all(set(cell) <= {"-", ":"} for cell in cells):
            continue
        if header is None:
            header = cells
        else:
            require(len(cells) == len(header), f"bad table row in {path}: {raw_line}")
            rows.append(dict(zip(header, cells)))
    require(header is not None, f"no markdown table found in {path}")
    return rows


def warning_counts(path):
    records = json.loads(Path(path).read_text(encoding="utf-8"))
    counts = Counter(record["repo"] for record in records)
    return records, counts


def validate(args):
    comparison_rows = parse_markdown_table(args.comparison)
    require(len(comparison_rows) == 15, "expected 15 comparison rows")
    require({row["Codebase"] for row in comparison_rows} == EXPECTED_PROJECTS, "project set mismatch")

    refine_total = 0
    cached_total = 0
    delta_total = 0
    cached_counts = {}
    refine_counts = {}

    for row in comparison_rows:
        project = row["Codebase"]
        refine = parse_int(row["Refine"])
        rebuilt = parse_int(row["No-dynamic rebuilt deps"])
        cached = parse_int(row["No-dynamic cached deps"])
        delta_refine = parse_int(row["Cached - Refine"])
        delta_rebuilt = parse_int(row["Cached - Rebuilt"])
        extracted = parse_int(row["Extracted warning blocks"])

        require(row["Status"] == "ok", f"{project} status is not ok")
        require(cached == rebuilt, f"{project} cached count differs from rebuilt count")
        require(delta_rebuilt == 0, f"{project} cached-vs-rebuilt delta is not zero")
        require(delta_refine == cached - refine, f"{project} cached-refine delta mismatch")
        require(extracted == cached, f"{project} extracted warning count mismatch")

        refine_total += refine
        cached_total += cached
        delta_total += delta_refine
        refine_counts[project] = refine
        cached_counts[project] = cached

    require(refine_total == EXPECTED_TOTALS["Refine"], "bad Refine total")
    require(cached_total == EXPECTED_TOTALS["No-dynamic cached deps"], "bad no-dynamic total")
    require(delta_total == EXPECTED_TOTALS["Cached - Refine"], "bad delta total")

    refine_records, refine_warning_counts = warning_counts(args.refine_warnings)
    nodynamic_records, nodynamic_warning_counts = warning_counts(args.no_dynamic_warnings)

    require(len(refine_records) == refine_total, "Refine warning JSON total mismatch")
    require(len(nodynamic_records) == cached_total, "no-dynamic warning JSON total mismatch")

    for project in EXPECTED_PROJECTS:
        require(
            refine_warning_counts.get(project, 0) == refine_counts[project],
            f"{project} Refine warning JSON count mismatch",
        )
        require(
            nodynamic_warning_counts.get(project, 0) == cached_counts[project],
            f"{project} no-dynamic warning JSON count mismatch",
        )

    print(
        "dynamic-propagation removal validation passed: "
        f"{refine_total} -> {cached_total} type warnings ({delta_total:+d})"
    )


def clear_sentinels(args):
    root = Path(args.repos_root)
    removed = 0
    for sentinel in root.glob("*/_build/.perf-deps-compiled"):
        sentinel.unlink()
        removed += 1
        print(f"removed {sentinel}")
    print(f"removed {removed} dependency sentinel(s)")


def patch_already_applied(repo_path, patch_path):
    result = subprocess.run(
        ["git", "apply", "--reverse", "--check", str(patch_path)],
        cwd=repo_path,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.returncode == 0


def checkout_projects(args):
    experiment_dir = Path(__file__).resolve().parents[1]
    patch_root = experiment_dir / "project-patches"
    repos_root = Path(args.repos_root)
    repos_root.mkdir(parents=True, exist_ok=True)

    for project in PROJECTS:
        repo_path = repos_root / project["dir"]
        if not (repo_path / ".git").is_dir():
            if repo_path.exists():
                raise SystemExit(f"{repo_path} exists but is not a git repository")
            run(["git", "clone", "--no-checkout", project["url"], str(repo_path)])

        run(["git", "fetch", "--depth=1", "origin", project["commit"]], cwd=repo_path)
        run(["git", "checkout", "--detach", project["commit"]], cwd=repo_path)
        run(["git", "reset", "--hard", project["commit"]], cwd=repo_path)
        run(["git", "clean", "-fdx"], cwd=repo_path)

        patch_name = project.get("patch")
        if args.apply_project_patches and patch_name:
            patch_path = patch_root / patch_name
            if patch_already_applied(repo_path, patch_path):
                print(f"{project['name']}: project patch already applied")
            else:
                run(["git", "apply", str(patch_path)], cwd=repo_path)

    print(f"checked out {len(PROJECTS)} project repositories under {repos_root}")


def main():
    experiment_dir = Path(__file__).resolve().parents[1]
    results = experiment_dir / "results"

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument(
        "--comparison",
        default=results / "no-dynamic-vs-refine-comparison-20260527.md",
        type=Path,
    )
    validate_parser.add_argument(
        "--refine-warnings",
        default=results / "refine-warnings-20260527.json",
        type=Path,
    )
    validate_parser.add_argument(
        "--no-dynamic-warnings",
        default=results / "no-dynamic-cached-deps-warnings-20260527.json",
        type=Path,
    )
    validate_parser.set_defaults(func=validate)

    clear_parser = subparsers.add_parser("clear-sentinels")
    clear_parser.add_argument(
        "--repos-root",
        default=experiment_dir / "tools" / "repos",
        type=Path,
        help="Repository bucket containing project checkouts.",
    )
    clear_parser.set_defaults(func=clear_sentinels)

    checkout_parser = subparsers.add_parser("checkout-projects")
    checkout_parser.add_argument(
        "--repos-root",
        default=experiment_dir / "tools" / "repos",
        type=Path,
        help="Repository bucket for the recorded project checkouts.",
    )
    checkout_parser.add_argument(
        "--apply-project-patches",
        action="store_true",
        help="Apply the archived project compatibility patches after checkout.",
    )
    checkout_parser.set_defaults(func=checkout_projects)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
