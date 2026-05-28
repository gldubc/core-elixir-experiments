# Core Elixir Experiments

This repository stores reproduction artifacts for experiments used by the Core
Elixir paper. It is intentionally separate from the paper repository and from
the Elixir compiler checkout.

The repository is organized by numbered experiments:

- `experiments/01-guard-exactness`: guard-exactness instrumentation and corpus
  results.
- `experiments/02-arrow-return-informativeness`: inferred-arrow return
  informativeness instrumentation and selected open-source project results.

Each experiment directory contains its own README with the measurement, the
paper result, the code versions used, and reproduction commands. The repository
keeps the small artifacts needed to inspect and rerun the experiments: compiler
patches, drivers, summary tables, logs, and paper snippets.

Large raw outputs, dependency checkouts, compiler builds, and generated project
repositories are excluded from git. When such local-only files matter for a
result, the corresponding experiment README names them explicitly.

## Commands

```sh
# Show available targets and variables.
make help

# Lightweight consistency check for committed summaries plus patch apply check.
make check

# Reproduce a small run on ExDoc.
make reproduce-smoke

# Validate the archived arrow-return informativeness table.
make reproduce-experiment-02-smoke

# Reproduce the full guard-exactness run. This is intentionally expensive.
make reproduce-full

# Remove generated checkouts, raw run outputs, caches, and packaged artifacts.
make clean
```

Public targets ask for confirmation before doing work. Use `CONFIRM=0` for
scripted runs, for example:

```sh
make check CONFIRM=0
```
