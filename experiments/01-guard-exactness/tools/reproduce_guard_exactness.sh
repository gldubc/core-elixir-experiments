#!/usr/bin/env bash
set -euo pipefail

command="${1:-smoke}"
elixir_commit="095c1649c59651a959c57ed15628ea3aebc388d3"

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd -P)"
experiment_dir="$(cd "$script_dir/.." && pwd -P)"
repo_root="$(cd "$experiment_dir/../.." && pwd -P)"

patch="$experiment_dir/compiler-patches/guard-instrumentation.patch"
perf="$experiment_dir/tools/perf.py"
prepare_deps="$experiment_dir/tools/prepare_dependencies.py"

elixir_root="${ELIXIR_ROOT:-$repo_root/build/elixir-guard-exactness}"
run_id="${RUN_ID:-01-guard-exactness-$(date -u +%Y%m%d-%H%M%S)}"
run_dir="${RUN_DIR:-$repo_root/results/guard-exactness/$run_id}"
compile_timeout="${COMPILE_TIMEOUT:-60}"
system_mix="${SYSTEM_MIX:-mix}"
repos="${REPOS:-}"

case "$elixir_root" in
  /*) ;;
  *) elixir_root="$repo_root/$elixir_root" ;;
esac

case "$run_dir" in
  /*) ;;
  *) run_dir="$repo_root/$run_dir" ;;
esac

repo_args=()
if [[ -n "$repos" ]]; then
  for repo in $repos; do
    repo_args+=("-r" "$repo")
  done
fi

ensure_elixir() {
  if [[ ! -d "$elixir_root/.git" ]]; then
    mkdir -p "$(dirname "$elixir_root")"
    git clone https://github.com/elixir-lang/elixir.git "$elixir_root"
  fi

  if git -C "$elixir_root" apply --reverse --check "$patch" >/dev/null 2>&1; then
    echo "instrumentation patch already applied in $elixir_root"
    return
  fi

  if ! git -C "$elixir_root" diff --quiet || ! git -C "$elixir_root" diff --cached --quiet; then
    echo "refusing to patch dirty Elixir checkout: $elixir_root" >&2
    exit 1
  fi

  git -C "$elixir_root" fetch origin "$elixir_commit"
  git -C "$elixir_root" checkout --detach "$elixir_commit"
  git -C "$elixir_root" apply "$patch"
}

build_elixir() {
  make -C "$elixir_root"
}

prepare_dependencies() {
  python3 "$prepare_deps" \
    --elixir-root "$elixir_root" \
    --system-mix "$system_mix" \
    "${repo_args[@]}"
}

run_external_repos() {
  mkdir -p "$run_dir"
  python3 "$perf" \
    --elixir-root "$elixir_root" \
    --tc-table \
    --compile-timeout "$compile_timeout" \
    --guard-exactness \
    --guard-exactness-run-id "$run_id" \
    --guard-exactness-root "$run_dir" \
    --no-validate-compile-env \
    --no-rebuild-on-commit-change \
    "${repo_args[@]}"
}

run_stdlib() {
  mkdir -p "$run_dir/raw/ElixirStdlib"
  make -C "$elixir_root" clean
  ELIXIR_GUARD_EXACTNESS_DIR="$run_dir/raw/ElixirStdlib" \
  ELIXIR_GUARD_EXACTNESS_PROJECT="ElixirStdlib" \
  ELIXIR_GUARD_EXACTNESS_REPO_ROOT="$elixir_root" \
  ELIXIR_GUARD_EXACTNESS_RUN_ID="$run_id" \
    make -C "$elixir_root" compile
}

summarize() {
  python3 "$perf" \
    --elixir-root "$elixir_root" \
    --tc-table \
    --guard-exactness \
    --guard-exactness-run-id "$run_id" \
    --guard-exactness-root "$run_dir" \
    --guard-exactness-summarize-only
}

case "$command" in
  setup)
    ensure_elixir
    ;;
  build)
    build_elixir
    ;;
  prepare-deps)
    prepare_dependencies
    ;;
  external)
    run_external_repos
    ;;
  stdlib)
    run_stdlib
    ;;
  summarize)
    summarize
    ;;
  smoke)
    if [[ -z "$repos" ]]; then
      repos="ExDoc"
      repo_args=("-r" "ExDoc")
    fi
    ensure_elixir
    build_elixir
    prepare_dependencies
    run_external_repos
    summarize
    ;;
  full)
    ensure_elixir
    build_elixir
    prepare_dependencies
    run_external_repos
    run_stdlib
    summarize
    ;;
  *)
    echo "usage: $0 setup|build|prepare-deps|external|stdlib|summarize|smoke|full" >&2
    exit 2
    ;;
esac
