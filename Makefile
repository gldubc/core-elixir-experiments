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
REPO_ARGS = $(foreach repo,$(REPOS),--repo $(repo))
SMOKE_REPO_ARGS = $(foreach repo,$(if $(REPOS),$(REPOS),ExDoc),--repo $(repo))
RUN_ID_ARG = $(if $(RUN_ID),--run-id $(RUN_ID),)
RUN_DIR_ARG = $(if $(RUN_DIR),--run-dir $(RUN_DIR),)

.PHONY: check check-artifact verify-patch setup-elixir build-elixir prepare-deps reproduce reproduce-smoke reproduce-full summarize package-raw

check: check-artifact verify-patch

check-artifact:
	$(PYTHON) -m py_compile $(EXPERIMENT_DIR)/tools/perf.py
	$(PYTHON) -m py_compile $(EXPERIMENT_DIR)/tools/validate_guard_exactness.py
	$(PYTHON) -m py_compile $(EXPERIMENT_DIR)/tools/prepare_dependencies.py
	$(PYTHON) -m py_compile $(EXPERIMENT_DIR)/tools/reproduce_guard_exactness.py
	$(PYTHON) -m py_compile $(EXPERIMENT_DIR)/tools/verify_compiler_patch.py
	$(PYTHON) -m py_compile scripts/package_raw_artifact.py
	$(PYTHON) $(EXPERIMENT_DIR)/tools/validate_guard_exactness.py \
		$(EXPERIMENT_DIR)/results

verify-patch:
	$(PYTHON) $(EXPERIMENT_DIR)/tools/verify_compiler_patch.py

setup-elixir:
	$(PYTHON) $(EXPERIMENT_DIR)/tools/reproduce_guard_exactness.py setup \
		--elixir-root "$(ELIXIR_ROOT)"

build-elixir:
	$(PYTHON) $(EXPERIMENT_DIR)/tools/reproduce_guard_exactness.py build \
		--elixir-root "$(ELIXIR_ROOT)"

prepare-deps:
	$(PYTHON) $(EXPERIMENT_DIR)/tools/reproduce_guard_exactness.py prepare-deps \
		--elixir-root "$(ELIXIR_ROOT)" \
		--system-mix "$(SYSTEM_MIX)" \
		$(REPO_ARGS)

reproduce: reproduce-full

reproduce-smoke:
	$(PYTHON) $(EXPERIMENT_DIR)/tools/reproduce_guard_exactness.py smoke \
		--elixir-root "$(ELIXIR_ROOT)" $(RUN_ID_ARG) $(RUN_DIR_ARG) \
		--compile-timeout "$(COMPILE_TIMEOUT)" \
		--system-mix "$(SYSTEM_MIX)" $(SMOKE_REPO_ARGS)

reproduce-full:
	$(PYTHON) $(EXPERIMENT_DIR)/tools/reproduce_guard_exactness.py full \
		--elixir-root "$(ELIXIR_ROOT)" $(RUN_ID_ARG) $(RUN_DIR_ARG) \
		--compile-timeout "$(COMPILE_TIMEOUT)" \
		--system-mix "$(SYSTEM_MIX)" $(REPO_ARGS)

summarize:
	$(PYTHON) $(EXPERIMENT_DIR)/tools/reproduce_guard_exactness.py summarize \
		--elixir-root "$(ELIXIR_ROOT)" $(RUN_ID_ARG) $(RUN_DIR_ARG)

package-raw:
	$(if $(RUN_DIR),,$(error RUN_DIR is required for package-raw))
	$(PYTHON) scripts/package_raw_artifact.py "$(RUN_DIR)" artifacts
