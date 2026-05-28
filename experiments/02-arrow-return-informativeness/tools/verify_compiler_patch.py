#!/usr/bin/env python3
import os
import subprocess
import sys
import time
from pathlib import Path


ELIXIR_COMMIT = "23a431223bbbc156eb224c6aa55b68479393d3e5"
SCRIPT_DIR = Path(__file__).resolve().parent
EXPERIMENT_DIR = SCRIPT_DIR.parent
REPO_ROOT = EXPERIMENT_DIR.parents[1]
PATCH = EXPERIMENT_DIR / "compiler-patches" / "arrow-return-informativeness.patch"
CHECK_ROOT = REPO_ROOT / "build" / "patch-check-elixir-arrow-return"
LOCK_PATH = REPO_ROOT / "build" / "patch-check-elixir-arrow-return.lock"


def run(cmd, cwd=None):
    print("$", " ".join(str(part) for part in cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


class FileLock:
    def __init__(self, path):
        self.path = path
        self.fd = None

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        while True:
            try:
                self.fd = os.open(self.path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                os.write(self.fd, str(os.getpid()).encode())
                return self
            except FileExistsError:
                time.sleep(0.2)

    def __exit__(self, _exc_type, _exc, _tb):
        if self.fd is not None:
            os.close(self.fd)
        try:
            self.path.unlink()
        except FileNotFoundError:
            pass


def main():
    with FileLock(LOCK_PATH):
        if not (CHECK_ROOT / ".git").is_dir():
            if CHECK_ROOT.exists():
                raise SystemExit(f"{CHECK_ROOT} exists but is not a git repository")
            CHECK_ROOT.parent.mkdir(parents=True, exist_ok=True)
            run(
                [
                    "git",
                    "clone",
                    "--filter=blob:none",
                    "--no-checkout",
                    "https://github.com/elixir-lang/elixir.git",
                    str(CHECK_ROOT),
                ]
            )

        run(["git", "fetch", "--depth=1", "origin", ELIXIR_COMMIT], cwd=CHECK_ROOT)
        run(["git", "checkout", "--detach", ELIXIR_COMMIT], cwd=CHECK_ROOT)
        run(["git", "reset", "--hard", ELIXIR_COMMIT], cwd=CHECK_ROOT)
        run(["git", "clean", "-fdx"], cwd=CHECK_ROOT)
        run(["git", "apply", "--check", str(PATCH)], cwd=CHECK_ROOT)
    print(f"compiler patch applies to {ELIXIR_COMMIT}")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
