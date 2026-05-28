# Experiment 01: Guard Exactness

This experiment measures how often the Elixir type checker computes exact
pattern/guard types at clause heads, generators, and `with` generators.

The compiler instrumentation is off by default. It emits JSONL only when
`ELIXIR_GUARD_EXACTNESS_DIR` is set.

## Contents

- `compiler-patches/guard-instrumentation.patch`: patch against Elixir commit
  `095c1649c59651a959c57ed15628ea3aebc388d3`.
- `tools/perf.py`: experiment snapshot of the `ept` perf backend with
  `--guard-exactness`.
- `tools/ept`: local user-facing wrapper snapshot. It forwards unknown flags to
  `perf.py`.
- `results/guard_exactness_summary.csv`: deduplicated project summaries.
- `results/projects.csv`: project commits, sizes, compile status, and counts.
- `results/paper_projects.csv`: the six projects used in the main paper table.
- `results/ept_corpus_table.csv`: full `ept` corpus table, excluding stdlib.
- `results/metadata.json`: sanitized run metadata and aggregate counts.
- `results/precise_guards_table.tex`: generated TeX table snippet.
- `results/SHA256SUMS.md`: checksums for committed artifacts and the large
  local per-site CSV.

The full raw JSONL directory was about 1.6 GB and is excluded from git. The
deduplicated per-site CSV was about 184 MB and is also excluded from git.

## Results

Main paper projects:

- Analyzed pairs: `59,973`
- Exact pairs: `38,645`
- Weighted exactness: `64.44%`

Full `ept` corpus, excluding the Elixir standard library:

- Analyzed pairs: `164,701`
- Exact pairs: `141,755`
- Weighted exactness: `86.07%`

All projects in this artifact, including the Elixir standard library:

- Analyzed pairs: `202,386`
- Exact pairs: `164,905`
- Weighted exactness: `81.48%`

## Reproduction Outline

Start from a clean Elixir checkout at the recorded commit:

```sh
git clone https://github.com/elixir-lang/elixir.git build/elixir
git -C build/elixir checkout 095c1649c59651a959c57ed15628ea3aebc388d3
git -C build/elixir apply ../../experiments/01-guard-exactness/compiler-patches/guard-instrumentation.patch
```

Build the instrumented compiler:

```sh
cd build/elixir
make clean
make
```

Run external repositories through `ept`/`perf.py`:

```sh
ELIXIR_PERF=$PWD/experiments/01-guard-exactness/tools/perf.py \
  experiments/01-guard-exactness/tools/ept \
  --guard-exactness \
  --guard-exactness-run-id 01-guard-exactness-20260527 \
  --compile-timeout 60 \
  --no-validate-compile-env \
  --no-rebuild-on-commit-change
```

Run the Elixir standard library separately with the same run id:

```sh
RUN_DIR=$PWD/results/guard-exactness/01-guard-exactness-20260527
ELIXIR_ROOT=$PWD/build/elixir

ELIXIR_GUARD_EXACTNESS_DIR=$RUN_DIR/raw/ElixirStdlib \
ELIXIR_GUARD_EXACTNESS_PROJECT=ElixirStdlib \
ELIXIR_GUARD_EXACTNESS_REPO_ROOT=$ELIXIR_ROOT \
ELIXIR_GUARD_EXACTNESS_RUN_ID=01-guard-exactness-20260527 \
  make -C "$ELIXIR_ROOT" compile
```

Regenerate summaries from raw JSONL:

```sh
python3 experiments/01-guard-exactness/tools/perf.py \
  --elixir-root build/elixir \
  --tc-table \
  --guard-exactness \
  --guard-exactness-run-id 01-guard-exactness-20260527 \
  --guard-exactness-summarize-only
```

Dependency note: the archived run prepared external project dependencies with
the system Mix where possible, then used the instrumented compiler only for the
analyzed project compile. This experiment does not change `perf.py` to enforce
that as a general policy.

## Validation

The archived run was checked as follows:

- all `11,960` JSONL files parsed;
- `649,102` raw JSONL rows parsed;
- zero JSON parse errors;
- retained summary rows exclude `deps/` and `_build/`;
- ExDoc repeated with identical deduplicated counts:
  `1,800` analyzed and `1,533` exact in both runs.

Run the local summary checks:

```sh
python3 experiments/01-guard-exactness/tools/validate_guard_exactness.py \
  experiments/01-guard-exactness/results
```
