#!/usr/bin/env python3
import argparse
import sys


YES_VALUES = {"1", "true", "yes", "y", "on"}
NO_VALUES = {"0", "false", "no", "n", "off"}


def enabled(value):
    normalized = str(value).strip().lower()
    if normalized in YES_VALUES:
        return True
    if normalized in NO_VALUES:
        return False
    raise SystemExit(f"invalid confirmation setting: {value!r}")


def main(argv):
    parser = argparse.ArgumentParser(description="Ask for confirmation before running a make target")
    parser.add_argument("--enabled", default="1")
    parser.add_argument("message")
    args = parser.parse_args(argv)

    if not enabled(args.enabled):
        return

    print(f"{args.message} Confirm [y/n].", end=" ", flush=True)
    answer = sys.stdin.readline()
    if not sys.stdin.isatty():
        print()
    if answer.strip().lower() not in {"y", "yes"}:
        raise SystemExit("aborted")


if __name__ == "__main__":
    main(sys.argv[1:])
