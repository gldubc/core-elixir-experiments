EXPERIMENT_DIR := experiments/01-guard-exactness
ELIXIR_COMMIT := 095c1649c59651a959c57ed15628ea3aebc388d3
BUILD_DIR ?= build
ELIXIR_ROOT ?= $(BUILD_DIR)/elixir-guard-exactness
RUN_ID ?= 01-guard-exactness-$(shell date -u +%Y%m%d-%H%M%S)
RUN_DIR ?= results/guard-exactness/$(RUN_ID)
COMPILE_TIMEOUT ?= 60
REPOS ?=
SYSTEM_MIX ?= mix

.PHONY: check check-artifact verify-patch setup-elixir build-elixir prepare-deps reproduce reproduce-smoke reproduce-full summarize package-raw

check: check-artifact verify-patch

check-artifact:
	python3 -m py_compile $(EXPERIMENT_DIR)/tools/perf.py
	python3 -m py_compile $(EXPERIMENT_DIR)/tools/validate_guard_exactness.py
	python3 -m py_compile $(EXPERIMENT_DIR)/tools/prepare_dependencies.py
	python3 $(EXPERIMENT_DIR)/tools/validate_guard_exactness.py \
		$(EXPERIMENT_DIR)/results

verify-patch:
	$(EXPERIMENT_DIR)/tools/verify_compiler_patch.sh

setup-elixir:
	ELIXIR_ROOT="$(ELIXIR_ROOT)" $(EXPERIMENT_DIR)/tools/reproduce_guard_exactness.sh setup

build-elixir:
	ELIXIR_ROOT="$(ELIXIR_ROOT)" $(EXPERIMENT_DIR)/tools/reproduce_guard_exactness.sh build

prepare-deps:
	ELIXIR_ROOT="$(ELIXIR_ROOT)" SYSTEM_MIX="$(SYSTEM_MIX)" REPOS="$(REPOS)" \
		$(EXPERIMENT_DIR)/tools/reproduce_guard_exactness.sh prepare-deps

reproduce: reproduce-full

reproduce-smoke:
	ELIXIR_ROOT="$(ELIXIR_ROOT)" RUN_ID="$(RUN_ID)" RUN_DIR="$(RUN_DIR)" \
		COMPILE_TIMEOUT="$(COMPILE_TIMEOUT)" SYSTEM_MIX="$(SYSTEM_MIX)" \
		REPOS="$(if $(REPOS),$(REPOS),ExDoc)" \
		$(EXPERIMENT_DIR)/tools/reproduce_guard_exactness.sh smoke

reproduce-full:
	ELIXIR_ROOT="$(ELIXIR_ROOT)" RUN_ID="$(RUN_ID)" RUN_DIR="$(RUN_DIR)" \
		COMPILE_TIMEOUT="$(COMPILE_TIMEOUT)" SYSTEM_MIX="$(SYSTEM_MIX)" \
		REPOS="$(REPOS)" \
		$(EXPERIMENT_DIR)/tools/reproduce_guard_exactness.sh full

summarize:
	ELIXIR_ROOT="$(ELIXIR_ROOT)" RUN_ID="$(RUN_ID)" RUN_DIR="$(RUN_DIR)" \
		$(EXPERIMENT_DIR)/tools/reproduce_guard_exactness.sh summarize

package-raw:
	scripts/package-raw-artifact.sh "$(RUN_DIR)" artifacts
