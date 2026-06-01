# Excluded Static-Cleanup Examples

These commits were useful during manual review, but they were not counted in
the paper table because the commit metadata does not tie the cleanup to the
Elixir type system or to an Elixir warning in the way used by this experiment.

| Project | Commit | Deleted Elixir lines | Reason excluded |
| --- | --- | ---: | --- |
| Ash | `f33977d9e625d134119decfe6d5c764bbc5522b4` | 3 | Explicitly attributed to Dialyzer, not the Elixir type system. |
| Ash | `4017b72a5529adde923a2b64a271f960efb0d802` | 58 | Removes unused `require` statements. Useful cleanup, but not dead branch/clause evidence. |
| Ash | `79749c2685ea031ebb2de8cf60cc5edced6a8dd0` | 297 | Broad policy refactor with unrelated changes and Dialyzer notes. |
| Credo | `7437c92319514cf5ee1d00cdb56ffbcc40c4db14` | 16 | Compiler/test warning cleanup, but not dead branch/clause evidence. |
| Phoenix LiveView | `94a7cc55ce6e000a9a92741061497b95c422d18d` | 4 | Unreachable clause based on `IO.binwrite/2` API behavior, not type-system metadata. |
| Spitfire | `f937a7ab7baa275d3b5b66b25f09ce604a1d10f9` | 13 | Dialyzer setup/refactor commit; not Elixir type-system evidence. |
| Phoenix | `febe572cfb76b3179a38038fec19db556ad77aef` | 9 | Removes unused `require`s without type-system/dead-code metadata. |
| Phoenix | `a1916e0a0b5af8d166bbf78956b664856829d0bc` | 7 | Removes additional unused `require`s without type-system/dead-code metadata. |
| ExDoc | `71956e965f9d98e53a06c15f477cf038b476b87d` | 90 | Removes unused config fields; broader cleanup than dead-code warning evidence. |
| Nerves | `5523ba2d5d83754d44981bc53cd1d16e7eda33f7` | 284 | Deletes an unused module without type-system/warning metadata. |
| Livebook | `0435b4392ba67d0360448042b5ca2ef4d11052be` | 9 | Removes an unused environment variable without type-system/warning metadata. |
| Ash | `3979bf6c3b2051a83c07300487b36d78ba783257` | 19 | Generic "remove unused code" cleanup without type-system/warning metadata. |
