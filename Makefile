EXPERIMENT_DIR := experiments/01-guard-exactness
ELIXIR_COMMIT := 095c1649c59651a959c57ed15628ea3aebc388d3
PYTHON ?= python3
BUILD_DIR ?= build
ELIXIR_ROOT ?= $(BUILD_DIR)/elixir-guard-exactness
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

.PHONY: help clean check check-artifact verify-patch setup-elixir build-elixir prepare-deps reproduce reproduce-smoke reproduce-full summarize package-raw

help:
	@printf '%s\n' 'Core Elixir experiment artifact targets:'
	@printf '%s\n' ''
	@printf '%s\n' '  make check             Validate committed summaries and compiler patch.'
	@printf '%s\n' '  make reproduce-smoke   Reproduce a small ExDoc guard-exactness run.'
	@printf '%s\n' '  make reproduce-full    Reproduce the full corpus plus stdlib.'
	@printf '%s\n' '  make prepare-deps      Prepare external repo dependencies with system Mix.'
	@printf '%s\n' '  make summarize         Regenerate summaries from RUN_DIR raw JSONL.'
	@printf '%s\n' '  make package-raw       Package RUN_DIR raw JSONL and per-site CSV.'
	@printf '%s\n' '  make clean             Remove generated build, result, cache, and artifact state.'
	@printf '%s\n' ''
	@printf '%s\n' 'Useful variables:'
	@printf '%s\n' '  REPOS="ExDoc Credo"'
	@printf '%s\n' '  RUN_ID=01-guard-exactness-rerun'
	@printf '%s\n' '  RUN_DIR=results/guard-exactness/<run-id>'
	@printf '%s\n' '  COMPILE_TIMEOUT=60'
	@printf '%s\n' '  SYSTEM_MIX=/path/to/mix'
	@printf '%s\n' '  ELIXIR_ROOT=build/elixir-guard-exactness'
	@printf '%s\n' '  CONFIRM=0'

clean:
	$(call confirm,Removing generated build checkouts and run outputs and packaged artifacts and Python caches and repo buckets.)
	rm -rf "$(BUILD_DIR)" results artifacts
	find . -type d -name __pycache__ -prune -exec rm -rf {} +
	find "$(EXPERIMENT_DIR)/tools" -maxdepth 1 -type d -name 'repos-*' -exec rm -rf {} +

check:
	$(call confirm,Validating committed summaries and verifying the compiler patch.)
	@$(MAKE) --no-print-directory check-artifact verify-patch CONFIRM=0

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
