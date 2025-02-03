include Makefiles/rules.mk

# Targets
.PHONY: all build test clean

all: build

build:
	@$(BUILD_CMD)

test:
	@$(TEST_CMD) FILE=$(FILE)

run:
	@$(RUN_CMD) FILE=$(FILE)

clean:
	@$(CLEAN_CMD)
