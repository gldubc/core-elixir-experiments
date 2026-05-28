#!/usr/bin/env python3
import subprocess
import sys
from pathlib import Path


ELIXIR_COMMIT = "095c1649c59651a959c57ed15628ea3aebc388d3"
SCRIPT_DIR = Path(__file__).resolve().parent
EXPERIMENT_DIR = SCRIPT_DIR.parent
REPO_ROOT = EXPERIMENT_DIR.parents[1]
PATCH = EXPERIMENT_DIR / "compiler-patches" / "guard-instrumentation.patch"
CHECK_ROOT = REPO_ROOT / "build" / "patch-check-elixir"


def run(cmd, cwd=None):
    print("$", " ".join(str(part) for part in cmd), flush=True)
    subprocess.run(cmd, cwd=cwd, check=True)


def main():
    if not (CHECK_ROOT / ".git").is_dir():
        if CHECK_ROOT.exists():
            raise SystemExit(f"{CHECK_ROOT} exists but is not a git repository")
        CHECK_ROOT.parent.mkdir(parents=True, exist_ok=True)
        run([
            "git",
            "clone",
            "--filter=blob:none",
            "--no-checkout",
            "https://github.com/elixir-lang/elixir.git",
            str(CHECK_ROOT),
        ])

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
