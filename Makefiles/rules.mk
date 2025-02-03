include cfg/.env

# Targets
.PHONY: all test clean

NPROC := $(shell nproc)

FILE ?=

BUILD_TOOL_CMD := make -j$(NPROC) -C $(TOP_DIR)
BUILD_CMD := $(BUILD_TOOL_CMD) build
TEST_CMD := $(BUILD_TOOL_CMD) test FILE=$(FILE)
RUN_CMD := $(BUILD_TOOL_CMD) run FILE=$(FILE)
CLEAN_CMD := $(BUILD_TOOL_CMD) clean
