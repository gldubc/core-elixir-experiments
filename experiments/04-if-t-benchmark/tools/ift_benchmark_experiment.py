#!/usr/bin/env python3
import argparse
import os
import pathlib
import subprocess
import sys


EXPECTED = {
    "positive": "O",
    "negative": "O",
    "connectives": "O",
    "nesting_body": "O",
    "struct_fields": "O",
    "tuple_elements": "O",
    "tuple_length": "O",
    "alias": "x",
    "nesting_condition": "O",
    "merge_with_union": "O",
    "predicate_2way": "O",
    "predicate_1way": "O",
    "predicate_checked": "O",
}


def parse_result(text):
    rows = {}
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("(") or not line.endswith(")"):
            continue
        parts = line[1:-1].split()
        if len(parts) != 2:
            continue
        name, value = parts
        if name == "Benchmark":
            continue
        rows[name] = value
    return rows


def validate_text(text):
    rows = parse_result(text)
    missing = sorted(set(EXPECTED) - set(rows))
    extra = sorted(set(rows) - set(EXPECTED))
    wrong = {key: (EXPECTED[key], rows[key]) for key in EXPECTED if rows.get(key) != EXPECTED[key]}

    if missing or extra or wrong:
        if missing:
            print(f"missing rows: {', '.join(missing)}", file=sys.stderr)
        if extra:
            print(f"extra rows: {', '.join(extra)}", file=sys.stderr)
        for key, (expected, actual) in wrong.items():
            print(f"{key}: expected {expected}, got {actual}", file=sys.stderr)
        return 1

    print("if-t Elixir core validation passed: 12 O, alias x")
    return 0


def validate(args):
    return validate_text(pathlib.Path(args.result).read_text())


def run(args):
    benchmark_root = pathlib.Path(args.benchmark_root)
    elixir_bin = pathlib.Path(args.elixir_bin)
    output = pathlib.Path(args.output) if args.output else None

    env = os.environ.copy()
    env["PATH"] = f"{elixir_bin.parent}{os.pathsep}{env.get('PATH', '')}"

    completed = subprocess.run(
        ["racket", "main.rkt", "elixir"],
        cwd=benchmark_root,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )

    print(completed.stdout, end="")
    if output:
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(completed.stdout)

    if completed.returncode != 0:
        print(f"benchmark command exited with {completed.returncode}", file=sys.stderr)
        return completed.returncode

    return validate_text(completed.stdout)


def main(argv):
    parser = argparse.ArgumentParser(description="Run or validate the archived Elixir If-T benchmark result")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument(
        "--result",
        default="experiments/04-if-t-benchmark/results/core-elixir-result.txt",
    )
    validate_parser.set_defaults(func=validate)

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--benchmark-root", required=True)
    run_parser.add_argument("--elixir-bin", required=True)
    run_parser.add_argument("--output")
    run_parser.set_defaults(func=run)

    args = parser.parse_args(argv)
    raise SystemExit(args.func(args))


if __name__ == "__main__":
    main(sys.argv[1:])
