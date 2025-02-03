include Makefiles/docker.mk
include Makefiles/rules.mk

# Define the path to the Dockerfile
DOCKER_FILE_PATH := dockerfiles/Dockerfile.debug

DOCKER_BUILD_CMD := $(DOCKER_HOST) image build -t $(DOCKER_IMG_NAME) -f $(DOCKER_FILE_PATH) $(DOCKER_BUILD_CONTEXT)
DOCKER_RUN_CMD := $(DOCKER_HOST) container run $(DOCKER_ARG) $(DOCKER_IMG_NAME)

# Define the default target
.PHONY: all build test clean

# Target: all
all: build

# Target: build_img
# Description: Builds the Docker image using the specified Dockerfile
.PHONY: build_img
build_img:
	@$(DOCKER_BUILD_CMD)

# Build code
build: build_img
	@$(DOCKER_RUN_CMD) $(BUILD_CMD)

# Test code
test: build_img
	@$(DOCKER_RUN_CMD) $(TEST_CMD) FILE=$(FILE)

# Run code
run: build_img
	@$(DOCKER_RUN_CMD) $(RUN_CMD) FILE=$(FILE)

# Clean
clean: build_img
	@$(DOCKER_RUN_CMD) $(CLEAN_CMD)
