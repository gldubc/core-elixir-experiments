# Experiment 02: Arrow-Return Informativeness

## What this measures

This experiment measures how often the Elixir type checker infers function arrows
whose return type is more informative than exactly `dynamic()`.

The unit is an inferred arrow, not a source function declaration: one function
value may contribute several arrows.  An arrow scores:

- `0` if its return type is exactly `dynamic()`;
- `1` otherwise, including gradual return types such as `dynamic(integer())`.

The reported metric is:

```text
informative-return ratio = informative arrows / all inferred arrows
```

The aggregation keeps metric records whose `file` field identifies one of the
recorded project checkouts.  The raw stream also contained compiler-generated
template records with relative file paths; these were not attributable to a
project checkout in the original aggregation and are skipped by the reproduction
driver.

## Paper result

The paper uses this experiment to test whether inference usually collapses to
plain `dynamic()` or whether it retains useful static return information.

Across 17 selected open-source Elixir projects, the instrumented type checker
reported:

```text
57,258 function values
69,976 inferred arrows
43,158 informative returns
26,818 exact dynamic returns
61.68% informative-return ratio
```

The main text uses the aggregate result and a short table excerpt.  The full
per-project table is in `results/summary.csv` and `results/summary.md`; the
LaTeX snippets used for the paper are in `results/paper-main-excerpt.tex` and
`results/paper-appendix-table.tex`.

## Code versions

Compiler base:

```text
Elixir commit: 23a431223bbbc156eb224c6aa55b68479393d3e5
Elixir commit subject: Optimize Registry exact key matching
Instrumentation patch: compiler-patches/arrow-return-informativeness.patch
```

Project versions are recorded in `results/projects.csv`.  Each row gives the
project checkout directory, repository URL, exact commit, branch state, and
clean/dirty state used for the archived run.

The local compiler worktree that produced the patch was:

```text
/Users/gldubc/Code/research/elixir/worktrees/s10-arrow-return-informativeness
```

## Reproduction

From the artifact repository root:

```bash
make reproduce-experiment-02-smoke CONFIRM=0
```

This validates the committed summary table and is the cheap smoke check.

To verify that the compiler patch still applies to the recorded Elixir commit:

```bash
make verify-arrow-return-patch CONFIRM=0
```

To recreate the project checkouts and run the experiment locally:

```bash
ARTIFACT=/Users/gldubc/Code/research/core-elixir-experiments

python3 "$ARTIFACT/experiments/02-arrow-return-informativeness/tools/arrow_return_experiment.py" \
  checkout-projects \
  --projects-csv "$ARTIFACT/experiments/02-arrow-return-informativeness/results/projects.csv" \
  --repos-root "$ARTIFACT/build/arrow-return-projects"

git clone https://github.com/elixir-lang/elixir.git "$ARTIFACT/build/elixir-arrow-return"
cd "$ARTIFACT/build/elixir-arrow-return"
git checkout --detach 23a431223bbbc156eb224c6aa55b68479393d3e5
git apply "$ARTIFACT/experiments/02-arrow-return-informativeness/compiler-patches/arrow-return-informativeness.patch"
make
make test_stdlib TEST_FILES=module/types/metrics_test.exs
make test_stdlib TEST_FILES=module/types/infer_test.exs
make test_stdlib TEST_FILES=module/types/expr_test.exs

cd "$ARTIFACT"
python3 experiments/02-arrow-return-informativeness/tools/arrow_return_experiment.py \
  run \
  --elixir-root build/elixir-arrow-return \
  --repos-root build/arrow-return-projects \
  --output-dir build/arrow-return-run \
  --compile-timeout 60

python3 experiments/02-arrow-return-informativeness/tools/arrow_return_experiment.py \
  validate \
  --summary build/arrow-return-run/summary.csv
```

If dependencies are missing from fresh project checkouts, add `--deps-get` to
the `run` command.  That makes the run slower and creates local dependency
directories under `build/arrow-return-projects`.

## Files that matter

- `compiler-patches/arrow-return-informativeness.patch`: compiler
  instrumentation used for the measurement.
- `tools/arrow_return_experiment.py`: Python driver for checkout, collection,
  aggregation, and summary validation.
- `tools/verify_compiler_patch.py`: Python patch-application check against the
  recorded Elixir commit.
- `results/summary.csv`: committed numeric result.
- `results/summary.md`: Markdown rendering of the numeric result.
- `results/projects.csv`: exact project commits used by the archived run.
- `results/type-checking-table.txt`: type-checking timing log from the
  all-project run.
- `results/blockscout-type-checking-table.txt`: separate Blockscout timing log;
  the all-project timing log records a Blockscout compile failure, while the
  separate run emitted the Blockscout metrics included in the final summary.
- `results/paper-main-excerpt.tex` and `results/paper-appendix-table.tex`:
  snippets corresponding to the result added to the paper.

## Intentionally not committed

The raw metric streams are large and local-only:

```text
raw.jsonl
blockscout.raw.jsonl
combined.raw.jsonl
```

They are not committed.  Generated project checkouts, dependency directories,
Elixir build outputs, and fresh reproduction outputs belong under `build/`,
which is ignored by git.

## Smoke check

Run:

```bash
make reproduce-experiment-02-smoke CONFIRM=0
```

Expected output includes:

```text
arrow-return summary validation passed: 69976 arrows, 43158 informative (61.68%)
```
