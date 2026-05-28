#!/usr/bin/env bash
set -euo pipefail

commit="095c1649c59651a959c57ed15628ea3aebc388d3"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
experiment_dir="$(cd "$script_dir/.." && pwd -P)"
repo_root="$(cd "$experiment_dir/../.." && pwd -P)"
patch="$experiment_dir/compiler-patches/guard-instrumentation.patch"
check_root="$repo_root/build/patch-check-elixir"

if [[ ! -d "$check_root/.git" ]]; then
  rm -rf "$check_root"
  mkdir -p "$(dirname "$check_root")"
  git clone --filter=blob:none --no-checkout https://github.com/elixir-lang/elixir.git "$check_root"
fi

git -C "$check_root" fetch --depth=1 origin "$commit"
git -C "$check_root" checkout --detach "$commit" >/dev/null
git -C "$check_root" reset --hard "$commit" >/dev/null
git -C "$check_root" clean -fdx >/dev/null
git -C "$check_root" apply --check "$patch"

echo "compiler patch applies to $commit"
