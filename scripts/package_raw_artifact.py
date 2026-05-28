#!/usr/bin/env python3
import argparse
import hashlib
import subprocess
import sys
from pathlib import Path


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv):
    parser = argparse.ArgumentParser(description="Package large guard-exactness raw artifacts")
    parser.add_argument("run_dir")
    parser.add_argument("out_dir")
    args = parser.parse_args(argv)

    run_dir = Path(args.run_dir).expanduser().resolve()
    out_dir = Path(args.out_dir).expanduser().resolve()
    raw_dir = run_dir / "raw"
    rows = run_dir / "guard_exactness_rows.csv"
    if not raw_dir.is_dir():
        raise SystemExit(f"missing raw directory: {raw_dir}")
    if not rows.is_file():
        raise SystemExit(f"missing rows CSV: {rows}")

    out_dir.mkdir(parents=True, exist_ok=True)
    archive = out_dir / f"{run_dir.name}-raw.tar.zst"
    subprocess.run([
        "tar",
        "--zstd",
        "-cf",
        str(archive),
        "-C",
        str(run_dir),
        "raw",
        "guard_exactness_rows.csv",
    ], check=True)

    checksum = archive.with_suffix(archive.suffix + ".sha256")
    checksum.write_text(f"{sha256(archive)}  {archive.name}\n", encoding="utf-8")
    print(archive)


if __name__ == "__main__":
    try:
        main(sys.argv[1:])
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
