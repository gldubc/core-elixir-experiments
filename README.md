# Core Elixir Experiments

This repository stores reproduction artifacts for experiments used by the Core
Elixir paper. It is intentionally separate from the paper repository and from
the Elixir compiler checkout.

The repository is organized by numbered experiments:

- `experiments/01-guard-exactness`: guard-exactness instrumentation and corpus
  results.

Large raw outputs are not committed to git. Each experiment should commit the
code needed to reproduce the run, exact commit metadata, summary tables, and
checksums or packaging instructions for large raw data.

## Repository Policy

- Keep experiment names stable and numbered.
- Commit scripts, patches, summaries, metadata, and paper table snippets.
- Do not commit per-process raw JSONL dumps or other large generated artifacts.
- Put large raw archives in GitHub Releases or a long-term artifact archive.
- Record exact upstream commits and command lines in each experiment directory.

## Quick Check

```sh
make check
```
