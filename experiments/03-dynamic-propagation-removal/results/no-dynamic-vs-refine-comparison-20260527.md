# Type Warning Comparison: no-dynamic vs Refine

Generated on 2026-05-27; extended on 2026-06-01 with Postgrex and Flame.

## Inputs

- Refine table: `results/refine-type-warning-table-20260527.md`
- No-dynamic rebuilt-deps table: `results/no-dynamic-rebuilt-deps-type-warning-table-20260527.md`
- No-dynamic cached-deps table: `results/no-dynamic-cached-deps-type-warning-table-20260527.md`
- Focused Postgrex/Flame extension tables: `results/postgrex-flame-*-type-warning-table-20260601.md`
- Extracted cached-deps warning blocks: `results/no-dynamic-cached-deps-warnings-20260527.json` and `.md`

The original no-dynamic run used branch `no-dynamic-strong-return-wrapping` at commit `095c1649c59651a959c57ed15628ea3aebc388d3`, with local working-tree changes compiled into `bin/elixir`. The Postgrex/Flame extension used the committed branch `no-dynamic-strong-return-wrapping` at `8e07dc6187b7b3a8ba82e06ed6bf666eeb5987f4`.

## Result

- Refine total: 94 type warnings
- No-dynamic rebuilt-deps total: 158 type warnings
- No-dynamic cached-deps total: 158 type warnings
- No-dynamic cached minus Refine: +64 type warnings
- Cached-deps minus rebuilt-deps: +0 type warnings
- Extracted cached warning blocks: 158

The cached-deps pass produced exactly the same type-warning counts as the forced dependency rebuild pass, including the Postgrex/Flame extension. This confirms empirically that the dependency sentinel state did not affect the measured project warning counts for this run. The reason is also visible in the harness: dependency compilation happens before measurement, while every measured project run uses `mix compile --force --no-deps-check`, and the `--type-warnings` counter reads the selected project diagnostics, recursing only through umbrella child apps.

## Table

| Codebase | Refine | No-dynamic rebuilt deps | No-dynamic cached deps | Cached - Refine | Cached - Rebuilt | Extracted warning blocks | Status |
|---|---:|---:|---:|---:|---:|---:|---|
| Blockscout | 37 | 50 | 50 | +13 | +0 | 50 | ok |
| Ash | 33 | 45 | 45 | +12 | +0 | 45 | ok |
| Livebook | 4 | 6 | 6 | +2 | +0 | 6 | ok |
| HexPm | 12 | 12 | 12 | +0 | +0 | 12 | ok |
| Ecto | 0 | 0 | 0 | +0 | +0 | 0 | ok |
| Credo | 0 | 6 | 6 | +6 | +0 | 6 | ok |
| PhoenixLiveView | 0 | 1 | 1 | +1 | +0 | 1 | ok |
| Phoenix | 0 | 0 | 0 | +0 | +0 | 0 | ok |
| MixSBOM | 2 | 2 | 2 | +0 | +0 | 2 | ok |
| Postgrex | 0 | 12 | 12 | +12 | +0 | 12 | ok |
| OpenApiSpex | 2 | 7 | 7 | +5 | +0 | 7 | ok |
| ExDoc | 1 | 2 | 2 | +1 | +0 | 2 | ok |
| Nerves | 0 | 0 | 0 | +0 | +0 | 0 | ok |
| Spitfire | 1 | 2 | 2 | +1 | +0 | 2 | ok |
| SQL | 1 | 11 | 11 | +10 | +0 | 11 | ok |
| Flame | 0 | 1 | 1 | +1 | +0 | 1 | ok |
| AbsintheFederation | 1 | 1 | 1 | +0 | +0 | 1 | ok |

## Small Warning Projects

These no-dynamic projects have 1-7 warnings and are likely good candidates for a detailed local warning UI:

- Livebook: 6 warnings (+2 vs Refine)
- Credo: 6 warnings (+6 vs Refine)
- PhoenixLiveView: 1 warning (+1 vs Refine)
- MixSBOM: 2 warnings (+0 vs Refine)
- OpenApiSpex: 7 warnings (+5 vs Refine)
- ExDoc: 2 warnings (+1 vs Refine)
- Spitfire: 2 warnings (+1 vs Refine)
- Flame: 1 warning (+1 vs Refine)
- AbsintheFederation: 1 warning (+0 vs Refine)
