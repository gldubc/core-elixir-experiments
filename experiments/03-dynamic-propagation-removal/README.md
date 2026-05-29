# Experiment 03: Dynamic-Propagation Removal

## What this measures

This experiment measures how many project type warnings appear when the checker
does not propagate dynamic return information through strong calls.

The full checker keeps gradual return information in dynamic/gradual mode:
when any argument to a strong operation is gradual, the operation returns
`dynamic(t)` instead of plain `t`. The removal variant applies
`compiler-patches/dynamic-propagation-removal.patch`, which changes
`Module.Types.Apply.return/3` to return `t` directly.

The unit is a rendered Elixir type warning for the selected project itself.
Dependency warnings are not counted. The `ept` snapshot in `tools/perf.py`
counts compiler diagnostics whose severity is `:warning` and whose details
include `:typing_traces`, recursing through umbrella child apps but not through
dependencies.

## Paper result

The paper uses this experiment to show that dynamic propagation is not just an
implementation convenience. On the selected 15-project corpus, removing dynamic
propagation changes the project warning total from:

```text
94 warnings with the full checker
145 warnings with dynamic propagation removed
+51 additional warnings
```

The table inserted in the paper is archived as `results/paper-table.tex`.

## Code versions

Full checker baseline:

```text
Elixir branch: refine-static-predicate-types
Elixir commit: 095c1649c59651a959c57ed15628ea3aebc388d3
Commit subject: Refine static predicate branches
```

Removal variant:

```text
Base commit: 095c1649c59651a959c57ed15628ea3aebc388d3
Patch: compiler-patches/dynamic-propagation-removal.patch
Local branch now containing the same patch:
  no-dynamic-strong-return-wrapping
  8e07dc6187b7b3a8ba82e06ed6bf666eeb5987f4
```

During the archived run, the removal variant was compiled as the baseline commit
plus local working-tree changes. That matters because `tools/perf.py` keys the
dependency sentinel by the Git commit, not by dirty state. The experiment
therefore ran the removal variant twice: once after forcing dependency sentinel
invalidation and once with cached dependency sentinels. The project warning
counts were identical.

Project commits and local compatibility patches are recorded in
`results/projects.md`.

## Reproduction

From the artifact repository root, run the cheap smoke check:

```bash
make reproduce-experiment-03-smoke CONFIRM=0
```

To verify that the removal patch still applies to the recorded compiler base:

```bash
make verify-dynamic-propagation-patch CONFIRM=0
```

To rebuild the two compilers:

```bash
ARTIFACT=/Users/gldubc/Code/research/core-elixir-experiments

git clone https://github.com/elixir-lang/elixir.git "$ARTIFACT/build/elixir-refine"
cd "$ARTIFACT/build/elixir-refine"
git checkout --detach 095c1649c59651a959c57ed15628ea3aebc388d3
make

git clone https://github.com/elixir-lang/elixir.git "$ARTIFACT/build/elixir-no-dynamic"
cd "$ARTIFACT/build/elixir-no-dynamic"
git checkout --detach 095c1649c59651a959c57ed15628ea3aebc388d3
git apply "$ARTIFACT/experiments/03-dynamic-propagation-removal/compiler-patches/dynamic-propagation-removal.patch"
make
```

To recreate the project bucket and apply the archived project compatibility
patches where needed:

```bash
cd "$ARTIFACT"
REPO_ARGS="\
  --repo Blockscout --repo Ash --repo Livebook --repo HexPm --repo Ecto \
  --repo Credo --repo PhoenixLiveView --repo Phoenix --repo MixSBOM \
  --repo OpenApiSpex --repo ExDoc --repo Nerves --repo Spitfire \
  --repo SQL --repo AbsintheFederation"

python3 experiments/03-dynamic-propagation-removal/tools/dynamic_propagation_experiment.py \
  checkout-projects \
  --repos-root experiments/03-dynamic-propagation-removal/tools/repos \
  --apply-project-patches
```

To rerun the measurement:

```bash
cd "$ARTIFACT"

python3 experiments/03-dynamic-propagation-removal/tools/perf.py \
  --elixir-root build/elixir-refine \
  --repo-bucket main \
  --tc-table --type-warnings \
  --compile-timeout 120 --deps-compile-timeout 600 \
  $REPO_ARGS \
  -o build/dynamic-propagation-refine.md

python3 experiments/03-dynamic-propagation-removal/tools/dynamic_propagation_experiment.py \
  clear-sentinels \
  --repos-root experiments/03-dynamic-propagation-removal/tools/repos

python3 experiments/03-dynamic-propagation-removal/tools/perf.py \
  --elixir-root build/elixir-no-dynamic \
  --repo-bucket main \
  --tc-table --type-warnings \
  --compile-timeout 120 --deps-compile-timeout 600 \
  $REPO_ARGS \
  -o build/dynamic-propagation-no-dynamic-rebuilt-deps.md

python3 experiments/03-dynamic-propagation-removal/tools/perf.py \
  --elixir-root build/elixir-no-dynamic \
  --repo-bucket main \
  --tc-table --type-warnings \
  --compile-timeout 120 --deps-compile-timeout 600 \
  --no-rebuild-on-commit-change \
  $REPO_ARGS \
  -o build/dynamic-propagation-no-dynamic-cached-deps.md
```

The final comparison should match
`results/no-dynamic-vs-refine-comparison-20260527.md`.

## Files that matter

- `compiler-patches/dynamic-propagation-removal.patch`: compiler change used
  for the removal variant.
- `project-patches/*.patch`: small project compatibility patches present in the
  archived repository bucket.
- `tools/perf.py`: `ept` snapshot with the `--type-warnings` counter.
- `tools/dynamic_propagation_experiment.py`: project checkout helper, summary
  validator, and dependency sentinel cleaner.
- `tools/verify_compiler_patch.py`: patch-application check against the recorded
  compiler commit.
- `results/no-dynamic-vs-refine-comparison-20260527.md`: final comparison table.
- `results/*type-warning-table-20260527.md`: input warning-count tables.
- `results/refine-warnings-20260527.json`: extracted baseline warning blocks.
- `results/no-dynamic-cached-deps-warnings-20260527.json`: extracted removal
  warning blocks.
- `results/no-dynamic-cached-deps-warnings-20260527.md`: readable warning-block
  log for the removal variant.
- `results/type-warning-counting-audit-20260527.html`: local report explaining
  how type warnings were counted and cross-checked.
- `results/small-project-warning-audit-20260527.html`: local report reviewing
  the small-project warning candidates and likely false positives.
- `results/paper-table.tex`: table inserted in the Core Elixir paper.

## Intentionally not committed

The complete raw compiler logs were local-only:

```text
type-warning-audit-refine-20260527.log
type-warning-no-dynamic-cached-deps-20260527.log
type-warning-no-dynamic-rebuilt-deps-20260527.partial-untrusted.log
```

They are not committed because the extracted warning blocks and validation
tables are much smaller and contain the warning data used for the paper.
Generated Elixir builds, project checkouts, dependency directories, `_build`
directories, and fresh rerun outputs belong under `build/` or under the
experiment `tools/repos*` buckets and are ignored by git.

## Smoke check

Run:

```bash
make reproduce-experiment-03-smoke CONFIRM=0
```

Expected output includes:

```text
dynamic-propagation removal validation passed: 94 -> 145 type warnings (+51)
```
