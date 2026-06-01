# Experiment 05: Dead-Code Commit Scan

## What this measures

This experiment measures public commits in selected Elixir projects where dead
code was removed after type-system or compiler-warning evidence.

The scan is intentionally commit-metadata based. It searches commit messages and
bodies for removed-code words such as `dead code`, `unused`, `unused clause`,
`unreachable`, `redundant`, and `useless`, together with type/compiler words
such as `type system`, `typesystem`, `type checker`, `compiler`, `warning`, and
release names such as `Elixir 1.18`. Candidate diffs were then manually
inspected, and only warning-related deleted Elixir source lines were counted.

## Paper result

The paper reports:

```text
17 repositories scanned
7,151 non-merge commits after 2024-05-01
14 accepted dead-code commits
179 counted deleted Elixir source lines

Direct evidence:         9 commits, 91 lines
Warning-linked evidence: 5 commits, 88 lines
```

`Direct` means the commit metadata explicitly names the type system, type
checker, compiler, or a relevant Elixir release. `Warning-linked` means the
metadata names an Elixir warning, unused-clause warning, or dead-code cleanup,
but not the type-system pass itself.

Broader static-cleanup commits, such as unused `require`s, unused config fields,
or deleted unused modules, are listed separately in
`results/excluded_static_cleanup.md` and are not counted in the paper number.

## Code and repository versions

The scan uses the repository set recorded in `results/repositories.csv`. Each
row records the repository URL, the default-branch commit that was scanned, and
the number of non-merge commits after `2024-05-01`.

No compiler patch was used for this experiment. The evidence is the upstream
Git history plus manual diff inspection. The original local checkouts were under:

```text
/Users/gldubc/Code/research/elixir/perf/repos
/Users/gldubc/Code/research/elixir/perf/repos-s2-guard-instrumentation
```

`postgrex` and `flame` came from the second bucket during the archived scan.

## Reproduction

Cheap smoke check from the artifact repository root:

```sh
make reproduce-experiment-05-smoke CONFIRM=0
```

This validates the committed tables and checks that the paper totals still add
up to `14` commits and `179` deleted lines.

To rerun the keyword scan against the same local repo buckets:

```sh
python3 experiments/05-dead-code-commit-scan/tools/dead_code_commit_scan.py \
  scan \
  --results-dir experiments/05-dead-code-commit-scan/results \
  --repos-root /Users/gldubc/Code/research/elixir/perf/repos \
  --repos-root /Users/gldubc/Code/research/elixir/perf/repos-s2-guard-instrumentation \
  --output-dir build/dead-code-commit-scan
```

To rerun from fresh clones instead:

```sh
make reproduce-experiment-05-full CONFIRM=0
```

This clones missing repositories into `build/dead-code-commit-scan-repos`,
scans the recorded default-branch commits, and writes local candidate tables to
`build/dead-code-commit-scan/`.

## Files that matter

- `tools/dead_code_commit_scan.py`: Python validator and keyword-scan driver.
- `results/repositories.csv`: repository URLs, scanned commits, and commit
  counts.
- `results/accepted_commits.csv`: accepted commits, evidence bucket, counted
  lines, and counting mode.
- `results/project_summary.csv`: per-project totals used by the paper table.
- `results/excluded_static_cleanup.md`: useful reviewed commits that were not
  counted.

## Intentionally not committed

Generated project checkouts, dependency directories, and fresh scan outputs are
not committed. They belong under `build/`.

The full rerun writes:

```text
build/dead-code-commit-scan/keyword-candidates.tsv
build/dead-code-commit-scan/accepted-verification.tsv
build/dead-code-commit-scan/scan-summary.tsv
```

Those files are reproducible from the committed script and tables, so they are
not stored in git.

## Smoke check

Run:

```sh
make reproduce-experiment-05-smoke CONFIRM=0
```

Expected output includes:

```text
dead-code commit scan validation passed: 14 commits, 179 deleted lines (9 direct/91, 5 warning-linked/88)
```
