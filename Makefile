EXPERIMENT_DIR := experiments/01-guard-exactness
ARROW_EXPERIMENT_DIR := experiments/02-arrow-return-informativeness
DYNAMIC_EXPERIMENT_DIR := experiments/03-dynamic-propagation-removal
IFT_EXPERIMENT_DIR := experiments/04-if-t-benchmark
ELIXIR_COMMIT := 095c1649c59651a959c57ed15628ea3aebc388d3
PYTHON ?= python3
BUILD_DIR ?= build
ELIXIR_ROOT ?= $(BUILD_DIR)/elixir-guard-exactness
IFT_BENCHMARK_ROOT ?= /Users/gldubc/Code/research/writing/active/core-elixir/if-t-benchmarks/ifT-benchmark
TYPESPEC_ELIXIR_BIN ?= /Users/gldubc/Code/research/elixir/worktrees/typespec-translation/bin/elixir
IFT_OUTPUT ?= $(BUILD_DIR)/ift-benchmark-core-rerun.txt
RUN_ID ?=
RUN_DIR ?=
COMPILE_TIMEOUT ?= 60
REPOS ?=
SYSTEM_MIX ?= mix
CONFIRM ?= 1
REPO_ARGS = $(foreach repo,$(REPOS),--repo $(repo))
SMOKE_REPO_ARGS = $(foreach repo,$(if $(REPOS),$(REPOS),ExDoc),--repo $(repo))
RUN_ID_ARG = $(if $(RUN_ID),--run-id $(RUN_ID),)
RUN_DIR_ARG = $(if $(RUN_DIR),--run-dir $(RUN_DIR),)
SMOKE_SCOPE = $(if $(REPOS),$(REPOS),ExDoc)
EXTERNAL_SCOPE = $(if $(REPOS),$(REPOS),all external repos)
confirm = @$(PYTHON) scripts/confirm.py --enabled "$(CONFIRM)" "$(1)"

.DEFAULT_GOAL := help

.PHONY: help clean check check-artifact verify-patch check-arrow-return verify-arrow-return-patch reproduce-experiment-02-smoke check-dynamic-propagation verify-dynamic-propagation-patch reproduce-experiment-03-smoke check-ift-benchmark reproduce-experiment-04-smoke reproduce-experiment-04-full setup-elixir build-elixir prepare-deps reproduce reproduce-smoke reproduce-full summarize package-raw

help:
	@printf '%s\n' 'Core Elixir experiment artifact targets:'
	@printf '%s\n' ''
	@printf '%s\n' '  make check                            Validate committed summaries and compiler patches.'
	@printf '%s\n' '  make reproduce-smoke                  Reproduce a small ExDoc guard-exactness run.'
	@printf '%s\n' '  make reproduce-full                   Reproduce the full guard-exactness run.'
	@printf '%s\n' '  make reproduce-experiment-02-smoke    Validate the arrow-return summary table.'
	@printf '%s\n' '  make verify-arrow-return-patch        Check the arrow-return compiler patch applies.'
	@printf '%s\n' '  make reproduce-experiment-03-smoke    Validate the dynamic-propagation warning table.'
	@printf '%s\n' '  make verify-dynamic-propagation-patch Check the dynamic-propagation compiler patch applies.'
	@printf '%s\n' '  make reproduce-experiment-04-smoke    Validate the If-T Elixir benchmark row.'
	@printf '%s\n' '  make reproduce-experiment-04-full     Rerun the If-T Elixir benchmark locally.'
	@printf '%s\n' '  make prepare-deps                     Prepare external repo dependencies with system Mix.'
	@printf '%s\n' '  make summarize                        Regenerate summaries from RUN_DIR raw JSONL.'
	@printf '%s\n' '  make package-raw                      Package RUN_DIR raw JSONL and per-site CSV.'
	@printf '%s\n' '  make clean                            Remove generated build, result, cache, and artifact state.'
	@printf '%s\n' ''
	@printf '%s\n' 'Useful variables:'
	@printf '%s\n' '  REPOS="ExDoc Credo"'
	@printf '%s\n' '  RUN_ID=01-guard-exactness-rerun'
	@printf '%s\n' '  RUN_DIR=results/guard-exactness/<run-id>'
	@printf '%s\n' '  COMPILE_TIMEOUT=60'
	@printf '%s\n' '  SYSTEM_MIX=/path/to/mix'
	@printf '%s\n' '  ELIXIR_ROOT=build/elixir-guard-exactness'
	@printf '%s\n' '  IFT_BENCHMARK_ROOT=/path/to/ifT-benchmark'
	@printf '%s\n' '  TYPESPEC_ELIXIR_BIN=/path/to/typespec-translation/bin/elixir'
	@printf '%s\n' '  CONFIRM=0'

clean:
	$(call confirm,Removing generated build checkouts and run outputs and packaged artifacts and Python caches and repo buckets.)
	rm -rf "$(BUILD_DIR)" results artifacts
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find "$(EXPERIMENT_DIR)/tools" -maxdepth 1 -type d -name 'repos-*' -exec rm -rf {} +
	find "$(DYNAMIC_EXPERIMENT_DIR)/tools" -maxdepth 1 -type d \( -name 'repos' -o -name 'repos-*' \) -exec rm -rf {} +

check:
	$(call confirm,Validating committed summaries and verifying the compiler patches.)
	@$(MAKE) --no-print-directory check-artifact verify-patch check-arrow-return verify-arrow-return-patch check-dynamic-propagation verify-dynamic-propagation-patch check-ift-benchmark CONFIRM=0

check-artifact:
	$(call confirm,Validating committed guard-exactness summary artifacts.)
	$(PYTHON) -m py_compile $(EXPERIMENT_DIR)/tools/perf.py
	$(PYTHON) -m py_compile $(EXPERIMENT_DIR)/tools/validate_guard_exactness.py
	$(PYTHON) -m py_compile $(EXPERIMENT_DIR)/tools/prepare_dependencies.py
	$(PYTHON) -m py_compile $(EXPERIMENT_DIR)/tools/reproduce_guard_exactness.py
	$(PYTHON) -m py_compile $(EXPERIMENT_DIR)/tools/verify_compiler_patch.py
	$(PYTHON) -m py_compile scripts/package_raw_artifact.py
	$(PYTHON) -m py_compile scripts/confirm.py
	$(PYTHON) $(EXPERIMENT_DIR)/tools/validate_guard_exactness.py \
		$(EXPERIMENT_DIR)/results

verify-patch:
	$(call confirm,Checking that the compiler patch applies to the recorded Elixir commit.)
	$(PYTHON) $(EXPERIMENT_DIR)/tools/verify_compiler_patch.py

check-arrow-return:
	$(call confirm,Validating committed arrow-return informativeness summary artifacts.)
	$(PYTHON) -m py_compile $(ARROW_EXPERIMENT_DIR)/tools/arrow_return_experiment.py
	$(PYTHON) -m py_compile $(ARROW_EXPERIMENT_DIR)/tools/verify_compiler_patch.py
	$(PYTHON) $(ARROW_EXPERIMENT_DIR)/tools/arrow_return_experiment.py \
		validate \
		--summary $(ARROW_EXPERIMENT_DIR)/results/summary.csv

verify-arrow-return-patch:
	$(call confirm,Checking that the arrow-return compiler patch applies to the recorded Elixir commit.)
	$(PYTHON) $(ARROW_EXPERIMENT_DIR)/tools/verify_compiler_patch.py

reproduce-experiment-02-smoke:
	$(call confirm,Validating the archived arrow-return informativeness summary table.)
	$(PYTHON) $(ARROW_EXPERIMENT_DIR)/tools/arrow_return_experiment.py \
		validate \
		--summary $(ARROW_EXPERIMENT_DIR)/results/summary.csv

check-dynamic-propagation:
	$(call confirm,Validating committed dynamic-propagation removal summary artifacts.)
	$(PYTHON) -m py_compile $(DYNAMIC_EXPERIMENT_DIR)/tools/dynamic_propagation_experiment.py
	$(PYTHON) -m py_compile $(DYNAMIC_EXPERIMENT_DIR)/tools/verify_compiler_patch.py
	$(PYTHON) -m py_compile $(DYNAMIC_EXPERIMENT_DIR)/tools/perf.py
	$(PYTHON) $(DYNAMIC_EXPERIMENT_DIR)/tools/dynamic_propagation_experiment.py validate

verify-dynamic-propagation-patch:
	$(call confirm,Checking that the dynamic-propagation removal compiler patch applies.)
	$(PYTHON) $(DYNAMIC_EXPERIMENT_DIR)/tools/verify_compiler_patch.py

reproduce-experiment-03-smoke:
	$(call confirm,Validating the archived dynamic-propagation removal warning table.)
	$(PYTHON) $(DYNAMIC_EXPERIMENT_DIR)/tools/dynamic_propagation_experiment.py validate

check-ift-benchmark:
	$(call confirm,Validating committed If-T Elixir benchmark artifacts.)
	$(PYTHON) -m py_compile $(IFT_EXPERIMENT_DIR)/tools/ift_benchmark_experiment.py
	$(PYTHON) $(IFT_EXPERIMENT_DIR)/tools/ift_benchmark_experiment.py validate \
		--result $(IFT_EXPERIMENT_DIR)/results/core-elixir-result.txt

reproduce-experiment-04-smoke:
	$(call confirm,Validating the archived If-T Elixir benchmark row.)
	$(PYTHON) $(IFT_EXPERIMENT_DIR)/tools/ift_benchmark_experiment.py validate \
		--result $(IFT_EXPERIMENT_DIR)/results/core-elixir-result.txt

reproduce-experiment-04-full:
	$(call confirm,Rerunning the If-T Elixir core benchmark with $(TYPESPEC_ELIXIR_BIN).)
	$(PYTHON) $(IFT_EXPERIMENT_DIR)/tools/ift_benchmark_experiment.py run \
		--benchmark-root "$(IFT_BENCHMARK_ROOT)" \
		--elixir-bin "$(TYPESPEC_ELIXIR_BIN)" \
		--output "$(IFT_OUTPUT)"

setup-elixir:
	$(call confirm,Cloning or patching the instrumented Elixir checkout at $(ELIXIR_ROOT).)
	$(PYTHON) $(EXPERIMENT_DIR)/tools/reproduce_guard_exactness.py setup \
		--elixir-root "$(ELIXIR_ROOT)"

build-elixir:
	$(call confirm,Building the instrumented Elixir checkout at $(ELIXIR_ROOT).)
	$(PYTHON) $(EXPERIMENT_DIR)/tools/reproduce_guard_exactness.py build \
		--elixir-root "$(ELIXIR_ROOT)"

prepare-deps:
	$(call confirm,Preparing dependencies for $(EXTERNAL_SCOPE) with $(SYSTEM_MIX).)
	$(PYTHON) $(EXPERIMENT_DIR)/tools/reproduce_guard_exactness.py prepare-deps \
		--elixir-root "$(ELIXIR_ROOT)" \
		--system-mix "$(SYSTEM_MIX)" \
		$(REPO_ARGS)

reproduce: reproduce-full

reproduce-smoke:
	$(call confirm,Doing the guard-exactness experiment only for $(SMOKE_SCOPE).)
	$(PYTHON) $(EXPERIMENT_DIR)/tools/reproduce_guard_exactness.py smoke \
		--elixir-root "$(ELIXIR_ROOT)" $(RUN_ID_ARG) $(RUN_DIR_ARG) \
		--compile-timeout "$(COMPILE_TIMEOUT)" \
		--system-mix "$(SYSTEM_MIX)" $(SMOKE_REPO_ARGS)

reproduce-full:
	$(call confirm,Doing the guard-exactness experiment for $(EXTERNAL_SCOPE) plus the Elixir standard library.)
	$(PYTHON) $(EXPERIMENT_DIR)/tools/reproduce_guard_exactness.py full \
		--elixir-root "$(ELIXIR_ROOT)" $(RUN_ID_ARG) $(RUN_DIR_ARG) \
		--compile-timeout "$(COMPILE_TIMEOUT)" \
		--system-mix "$(SYSTEM_MIX)" $(REPO_ARGS)

summarize:
	$(call confirm,Regenerating guard-exactness summaries from the selected run directory.)
	$(PYTHON) $(EXPERIMENT_DIR)/tools/reproduce_guard_exactness.py summarize \
		--elixir-root "$(ELIXIR_ROOT)" $(RUN_ID_ARG) $(RUN_DIR_ARG)

package-raw:
	$(if $(RUN_DIR),,$(error RUN_DIR is required for package-raw))
	$(call confirm,Packaging raw JSONL and per-site CSV from $(RUN_DIR).)
	$(PYTHON) scripts/package_raw_artifact.py "$(RUN_DIR)" artifacts
