# Project Versions

The warning-count runs used persistent `ept` repository buckets under:

```text
/Users/gldubc/Code/research/elixir/perf/
```

The table records the project checkout commits used by the experiment. The dirty entries are archived under `../project-patches/`; they are small compatibility changes to dependency locks or project options that allowed the selected projects to compile under the local development compiler. Postgrex and Flame were added by a focused rerun on 2026-06-01 using the same recorded commits as the other corpus experiments.

| Project | Directory | Repository | Commit | Tracked state |
|---|---|---|---|---|
| Blockscout | `blockscout` | `https://github.com/blockscout/blockscout.git` | `d9edfc30527a0e5d4ec86f923f20efcd8bfede01` | clean |
| Ash | `ash` | `https://github.com/ash-project/ash.git` | `5790310b740bfaf62ab6ceedc692bfc94c1bab60` | clean |
| Livebook | `livebook` | `https://github.com/livebook-dev/livebook.git` | `b1d98d2b68d4ee998a78f4214232d92b890a652d` | clean |
| HexPm | `hexpm` | `https://github.com/hexpm/hexpm.git` | `50587373a09fd55100961cb9c7501e501db472e5` | clean |
| Ecto | `ecto` | `https://github.com/elixir-ecto/ecto.git` | `cf3a5b7219a552c24aae24bf5eef7354c1184b8a` | clean |
| Credo | `credo` | `https://github.com/rrrene/credo.git` | `2d116684cd4b16b505031a8d84c6ae8ee48617bd` | clean |
| PhoenixLiveView | `phoenix_live_view` | `https://github.com/phoenixframework/phoenix_live_view.git` | `1fedd12dd000ceaf67da6ef26ca5d51dc8a64b54` | clean |
| Phoenix | `phoenix` | `https://github.com/phoenixframework/phoenix.git` | `d8f26700ea167a4e95d1d32314751ae1b5eb74f2` | dirty: `project-patches/phoenix-mix-lock.patch` |
| MixSBOM | `mix_sbom` | `https://github.com/erlef/mix_sbom.git` | `c72888d4e1d3f9a7693cc1faf952971216ac1f6a` | clean |
| Postgrex | `postgrex` | `https://github.com/elixir-ecto/postgrex.git` | `bd059dc01280f2932b6af5f36a5c8942e031ba5d` | clean |
| OpenApiSpex | `open_api_spex` | `https://github.com/open-api-spex/open_api_spex.git` | `f2c71bf320045b76c4bc2ea9a7a056c8d9092197` | clean |
| ExDoc | `ex_doc` | `https://github.com/elixir-lang/ex_doc.git` | `bc909685fd41f0e16f6714403bf520301ef3f28f` | clean |
| Nerves | `nerves` | `https://github.com/nerves-project/nerves.git` | `713da00682c9f70280ee78e00d994115cc9153eb` | dirty: `project-patches/nerves-elixir-requirement.patch` |
| Spitfire | `spitfire` | `https://github.com/elixir-tools/spitfire.git` | `47fad18a1bf7ca3ad5bca3b4d06a121e4ddceeb6` | dirty: `project-patches/spitfire-mix-lock.patch` |
| SQL | `sql` | `https://github.com/elixir-dbvisor/sql.git` | `bd316cd7b793e4d83b3e3545d506a8b00926dd32` | clean |
| Flame | `flame` | `https://github.com/phoenixframework/flame.git` | `27b94dafd874cd9747007205d25ee2d81349de07` | clean |
| AbsintheFederation | `absinthe_federation` | `https://github.com/DivvyPayHQ/absinthe_federation.git` | `d1735e37509157d0f10116d4f76286b09c86d3a9` | dirty: `project-patches/absinthe-federation-warnings-as-errors.patch` |
