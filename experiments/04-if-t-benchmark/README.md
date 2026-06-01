# Experiment 04: If-T Benchmark

## What this measures

This experiment ports the thirteen core items of the If-T type-narrowing
benchmark to Elixir and runs them with the research compiler branch that supports
asserted function type forms.

The result checks whether each benchmark item accepts its positive program and
rejects its negative program. For Elixir, compiler type warnings count as
rejections because warnings are the implementation's type-failure signal.

## Paper result

The paper reports that the Elixir port passes 12 of the 13 core If-T items. The
only miss is `alias`.

The rerun archived here produced:

```text
(Benchmark         elixir)
(positive          O     )
(negative          O     )
(connectives       O     )
(nesting_body      O     )
(struct_fields     O     )
(tuple_elements    O     )
(tuple_length      O     )
(alias             x     )
(nesting_condition O     )
(merge_with_union  O     )
(predicate_2way    O     )
(predicate_1way    O     )
(predicate_checked O     )
```

The `alias` miss is a positive-side precision limitation: the checker does not
track that a saved Boolean test result implies a type refinement for the value
that was tested.

## Code versions

Benchmark:

```text
repository: git@github.com:gldubc/ifT-benchmark.git
branch: elixir-narrowing-benchmark
commit: e25b30a529d5196d8cf01e3fe6b1b5a9cd88b744
```

Compiler:

```text
repository: git@github.com:gldubc/elixir.git
branch: typespec-translation
commit: 3684a541ed2ce9f83cd74fd46a7bae69081f017b
```

The compiler worktree had no tracked modifications during the archived run.

## Reproduction

Cheap smoke check from this artifact repository:

```sh
make reproduce-experiment-04-smoke CONFIRM=0
```

This validates the committed result against the expected paper row.

To rerun the benchmark locally:

```sh
make reproduce-experiment-04-full CONFIRM=0 \
  IFT_BENCHMARK_ROOT=/Users/gldubc/Code/research/writing/active/core-elixir/if-t-benchmarks/ifT-benchmark \
  TYPESPEC_ELIXIR_BIN=/Users/gldubc/Code/research/elixir/worktrees/typespec-translation/bin/elixir
```

The direct command used for the archived run was:

```sh
PATH=/Users/gldubc/Code/research/elixir/worktrees/typespec-translation/bin:$PATH racket main.rkt elixir
```

## Files that matter

- `results/core-elixir-result.txt`: exact core Elixir benchmark output.
- `results/run-metadata.md`: command, compiler commit, and benchmark commit.
- `benchmark-patches/`: patch series for the benchmark branch used by the run.
- `tools/ift_benchmark_experiment.py`: Python smoke validator and local rerun
  driver.

## Intentionally not committed

The benchmark repository checkout, Elixir compiler checkout, compiler build
products, Mix build directories, dependencies, and generated HTML review page
are not committed here.

The benchmark source is represented by its Git commit and by the patch series in
`benchmark-patches/`.

## Smoke check

Run:

```sh
make reproduce-experiment-04-smoke CONFIRM=0
```

Expected output includes:

```text
if-t Elixir core validation passed: 12 O, alias x
```
