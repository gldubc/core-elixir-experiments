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
- `tools/reproduce_guard_exactness.py`: setup, dependency preparation,
  collection, stdlib collection, and summarization driver.
- `tools/prepare_dependencies.py`: prepares external repo dependencies with the
  system `mix` before instrumented project compilation.
- `tools/verify_compiler_patch.py`: checks that the compiler patch applies to
  the recorded Elixir commit.
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

## Make Targets

From the repository root:

```sh
make help
```

This prints the available targets and the common variables for selecting repos,
run ids, timeouts, and tool paths.

```sh
make check
```

This verifies the committed summaries and checks that the compiler patch applies
to the recorded Elixir commit. On the first run it creates
`build/patch-check-elixir`. It does not run the corpus.

```sh
make reproduce-smoke
```

This clones/builds the instrumented compiler, prepares ExDoc dependencies with
the system `mix`, runs ExDoc with guard-exactness instrumentation, and summarizes
the run.

```sh
make reproduce-full
```

This runs the full external `ept` corpus plus a forced Elixir standard-library
compile under the same run id. It is expensive and writes raw JSONL under
`results/guard-exactness/<run-id>/raw/`.

```sh
make clean
```

This removes generated Elixir checkouts, reproduction run outputs, repo buckets,
Python caches, and packaged raw artifacts. It does not remove committed summary
files under `experiments/01-guard-exactness/results/`.

Useful knobs:

```sh
make reproduce-smoke REPOS="ExDoc Credo"
make reproduce-full RUN_ID=01-guard-exactness-rerun COMPILE_TIMEOUT=60
make prepare-deps REPOS="Phoenix Ecto" SYSTEM_MIX=/opt/homebrew/bin/mix
```

## Reproduction Steps

The Make targets delegate to `tools/reproduce_guard_exactness.py`. The full run
does this:

1. clone Elixir into `build/elixir-guard-exactness`;
2. check out `095c1649c59651a959c57ed15628ea3aebc388d3`;
3. apply `compiler-patches/guard-instrumentation.patch`;
4. build the instrumented compiler;
5. clone the recorded external repo commits into the perf bucket;
6. prepare external repo dependencies with the system `mix`;
7. run external repos through the experiment `perf.py` with `--guard-exactness`;
8. force a standard-library compile with the same guard-exactness environment;
9. regenerate CSV, TeX, and metadata summaries from raw JSONL.

The external repo command is equivalent to:

```sh
python3 experiments/01-guard-exactness/tools/perf.py \
  --elixir-root build/elixir-guard-exactness \
  --tc-table \
  --guard-exactness \
  --guard-exactness-run-id 01-guard-exactness-20260527 \
  --guard-exactness-root results/guard-exactness/01-guard-exactness-20260527 \
  --compile-timeout 60 \
  --no-validate-compile-env \
  --no-rebuild-on-commit-change
```

The dependency preparation is intentionally outside `perf.py`: this artifact
prepares dependencies with the system Mix and writes the existing perf sentinel
so `perf.py` does not rebuild dependencies with the instrumented compiler.

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
