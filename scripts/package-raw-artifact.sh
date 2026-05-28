#!/usr/bin/env bash
set -euo pipefail

if (($# != 2)); then
  echo "usage: package-raw-artifact.sh RUN_DIR OUT_DIR" >&2
  exit 2
fi

run_dir="$(cd "$1" && pwd -P)"
out_dir="$2"
mkdir -p "$out_dir"
out_dir="$(cd "$out_dir" && pwd -P)"

run_name="$(basename "$run_dir")"
archive="$out_dir/${run_name}-raw.tar.zst"

tar --zstd -cf "$archive" -C "$run_dir" raw guard_exactness_rows.csv
shasum -a 256 "$archive" > "$archive.sha256"

echo "$archive"
