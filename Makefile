.PHONY: check

check:
	python3 -m py_compile experiments/01-guard-exactness/tools/perf.py
	python3 -m py_compile experiments/01-guard-exactness/tools/validate_guard_exactness.py
	python3 experiments/01-guard-exactness/tools/validate_guard_exactness.py \
		experiments/01-guard-exactness/results
