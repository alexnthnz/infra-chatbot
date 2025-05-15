# Python interpreter
PYTHON = python3

# Backend directory
BACKEND = chatbot

# Service directories
SERVICES = handler

# Virtual environment directory
VENV = venv

# Deployment stage (dev, staging, prod)
STAGE ?= prod

# Map services to ECR repositories
SERVICE_ECR_MAP = handler:llmtoolflow-$(STAGE)-handler-ecr

# Function to get ECR repository for a service
get_ecr_repo = $(word 2,$(subst :, ,$(filter $1:%,$(SERVICE_ECR_MAP))))

# AWS region
AWS_REGION = ap-southeast-2

# AWS account ID
AWS_ACCOUNT_ID = $(shell aws sts get-caller-identity --query Account --output text)

# ECR repository URI prefix
ECR_REPO_PREFIX = $(AWS_ACCOUNT_ID).dkr.ecr.$(AWS_REGION).amazonaws.com

# Version variables
MAJOR ?= 0
MINOR ?= 0

# Validate AWS CLI configuration
validate-aws:
	@if ! aws sts get-caller-identity >/dev/null 2>&1; then echo "Error: AWS CLI not configured" >&2; exit 1; fi

compute-image-tag: validate-aws
	@if [ -z "$(SERVICE)" ]; then \
		echo "Error: SERVICE must be specified (e.g., make compute-image-tag SERVICE=handler)" >&2; \
		exit 1; \
	fi
	@if ! echo "$(SERVICES)" | grep -qw "$(SERVICE)"; then \
		echo "Error: SERVICE '$(SERVICE)' is not in SERVICES: $(SERVICES)" >&2; \
		exit 1; \
	fi
	@if [ ! -f scripts/compute_tag.sh ]; then echo "Error: scripts/compute_tag.sh not found" >&2; exit 1; fi
	@chmod +x scripts/compute_tag.sh
	$(eval REPO_NAME := $(call get_ecr_repo,$(SERVICE)))
	$(eval IMAGE_TAG := $(shell scripts/compute_tag.sh "$(REPO_NAME)" "$(AWS_REGION)" "$(MAJOR)" "$(MINOR)"))
	$(eval ECR_IMAGE_URI := $(ECR_REPO_PREFIX)/$(REPO_NAME):$(IMAGE_TAG))
	@echo "Computed ECR_IMAGE_URI: $(ECR_IMAGE_URI)"
	@echo "Computed IMAGE_TAG: $(IMAGE_TAG)"

# terraform.tfvars file location
TFVARS_FILE = deploy/infra/env/$(STAGE)/terraform.tfvars

# Default target
all: install test compute-image-tag build push-ecr update-tfvars

# Print variables for debugging
print-vars: compute-image-tag
	@echo "MAJOR: $(MAJOR)"
	@echo "MINOR: $(MINOR)"
	@echo "IMAGE_TAG: $(IMAGE_TAG)"
	@echo "ECR_IMAGE_URI: $(ECR_IMAGE_URI)"

# Update terraform.tfvars with the new ECR image URI
update-tfvars: compute-image-tag
	@echo "Updating terraform.tfvars with new ECR image URI: $(ECR_IMAGE_URI)"
	@if [ -f $(TFVARS_FILE) ]; then \
		if grep -q '^lambda_function_ecr_image_uri' $(TFVARS_FILE); then \
			sed -i.bak 's|^lambda_function_ecr_image_uri.*|lambda_function_ecr_image_uri = "$(ECR_IMAGE_URI)"|' $(TFVARS_FILE); \
		else \
			echo 'lambda_function_ecr_image_uri = "$(ECR_IMAGE_URI)"' >> $(TFVARS_FILE); \
		fi; \
	else \
		echo 'lambda_function_ecr_image_uri = "$(ECR_IMAGE_URI)"' > $(TFVARS_FILE); \
	fi

# Set up virtual environments for all services
venv:
	@if [ -z "$(SERVICE)" ]; then \
		echo "Error: SERVICE must be specified (e.g., make venv SERVICE=handler_1)" >&2; \
		exit 1; \
	fi
	@if ! echo "$(SERVICES)" | grep -qw "$(SERVICE)"; then \
		echo "Error: SERVICE '$(SERVICE)' is not in SERVICES: $(SERVICES)" >&2; \
		exit 1; \
	fi
	@$(PYTHON) -m venv $(BACKEND)/$(SERVICE)/$(VENV)
	@$(BACKEND)/$(SERVICE)/$(VENV)/bin/pip install --upgrade pip

# Install dependencies for all services
install: venv
	@if [ -z "$(SERVICE)" ]; then \
		echo "Error: SERVICE must be specified (e.g., make install SERVICE=handler_1)" >&2; \
		exit 1; \
	fi
	@if ! echo "$(SERVICES)" | grep -qw "$(SERVICE)"; then \
		echo "Error: SERVICE '$(SERVICE)' is not in SERVICES: $(SERVICES)" >&2; \
		exit 1; \
	fi
	@if [ ! -f $(BACKEND)/$(SERVICE)/requirements.txt ]; then echo "Error: requirements.txt not found for $(SERVICE)" >&2; exit 1; fi
	@$(BACKEND)/$(SERVICE)/$(VENV)/bin/pip install -r $(BACKEND)/$(SERVICE)/requirements.txt

# Run tests for all services
test: install
	@if [ -z "$(SERVICE)" ]; then \
		echo "Error: SERVICE must be specified (e.g., make test SERVICE=handler_1)" >&2; \
		exit 1; \
	fi
	@if ! echo "$(SERVICES)" | grep -qw "$(SERVICE)"; then \
		echo "Error: SERVICE '$(SERVICE)' is not in SERVICES: $(SERVICES)" >&2; \
		exit 1; \
	fi
	@test -d $(BACKEND)/$(SERVICE)/tests && $(BACKEND)/$(SERVICE)/$(VENV)/bin/pytest $(BACKEND)/$(SERVICE)/tests || echo "No tests for $(SERVICE)"

# Build Docker images for all services
build: compute-image-tag
	@if [ -z "$(SERVICE)" ]; then \
		echo "Error: SERVICE must be specified (e.g., make build SERVICE=handler_1)" >&2; \
		exit 1; \
	fi
	@if ! echo "$(SERVICES)" | grep -qw "$(SERVICE)"; then \
		echo "Error: SERVICE '$(SERVICE)' is not in SERVICES: $(SERVICES)" >&2; \
		exit 1; \
	fi
	@if [ -z "$(ECR_IMAGE_URI)" ]; then \
		echo "Error: ECR_IMAGE_URI is not set. Run compute-image-tag first." >&2; \
		exit 1; \
	fi
	@docker buildx build --platform linux/amd64 --provenance=false -t $(ECR_IMAGE_URI) $(BACKEND)/$(SERVICE)

# Push Docker images to ECR
push-ecr: build
	@if [ -z "$(SERVICE)" ]; then \
		echo "Error: SERVICE must be specified (e.g., make test SERVICE=handler_1)" >&2; \
		exit 1; \
	fi
	@if ! echo "$(SERVICES)" | grep -qw "$(SERVICE)"; then \
		echo "Error: SERVICE '$(SERVICE)' is not in SERVICES: $(SERVICES)" >&2; \
		exit 1; \
	fi
	@aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(ECR_REPO_PREFIX)
	@docker push $(ECR_REPO_PREFIX)/$(call get_ecr_repo,$(SERVICE)):$(IMAGE_TAG); 
	@docker rmi $(ECR_REPO_PREFIX)/$(call get_ecr_repo,$(SERVICE)):$(IMAGE_TAG) || true; 
	

# Set up ECR repositories for all services
setup-ecr: validate-aws
	@chmod +x scripts/setup_ecr.sh
	$(foreach service,$(SERVICES),scripts/setup_ecr.sh $(call get_ecr_repo,$(service)) $(AWS_REGION);)

# Drop ECR repositories for all services
drop-ecr: validate-aws
	@chmod +x scripts/drop_ecr.sh
	$(foreach service,$(SERVICES),scripts/drop_ecr.sh $(call get_ecr_repo,$(service)) $(AWS_REGION);)

# Clean up
clean:
	rm -rf $(foreach service,$(SERVICES),$(BACKEND)/$(service)/$(VENV) $(BACKEND)/$(service)/__pycache__ $(BACKEND)/$(service)/src/__pycache__ $(BACKEND)/$(service)/*.pyc $(BACKEND)/$(service)/src/*.pyc)
	rm -f .image_tag# Phony targets

help:
	@echo "Available targets:"
	@echo "  all                Run full pipeline (install, test, build, push, update tfvars)"
	@echo "  venv               Create virtual environment for a service"
	@echo "  install            Install dependencies for a service"
	@echo "  test               Run tests for a service"
	@echo "  build              Build Docker image for a service"
	@echo "  push-ecr           Push Docker image to ECR"
	@echo "  setup-ecr          Create ECR repositories"
	@echo "  drop-ecr           Delete ECR repositories"
	@echo "  clean              Remove virtual environments and cache files"
	@echo "  print-vars         Print computed variables"
	@echo "  update-tfvars      Update terraform.tfvars with ECR image URI"
	@echo "  compute-image-tag  Compute Docker image tag and ECR URI"
	@echo "Usage: make <target> SERVICE=<service> [STAGE=<stage>] [MAJOR=<major>] [MINOR=<minor>]"

# Phony targets
.PHONY: all venv install test build setup-ecr push-ecr drop-ecr clean print-vars update-tfvars compute-image-tag help
