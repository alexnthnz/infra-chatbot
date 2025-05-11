# Python interpreter
PYTHON = python3

# Backend directory
BACKEND = chatbot

# Service directories
SERVICES = handler_1

# Virtual environment directory
VENV = venv

# Deployment stage (dev, staging, prod)
STAGE ?= prod

# Map services to ECR repositories
SERVICE_ECR_MAP = handler_1:llmtoolflow-$(STAGE)-handler-ecr

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

# Compute the image tag once and store it
compute-image-tag:
	@chmod +x scripts/compute_tag.sh
	@scripts/compute_tag.sh $(call get_ecr_repo,handler_1) $(AWS_REGION) $(MAJOR) $(MINOR)
	@. ./.image_tag && echo "Computed IMAGE_TAG: $$IMAGE_TAG"
	$(eval IMAGE_TAG := $(shell . ./.image_tag && echo $$IMAGE_TAG))
	$(eval ECR_IMAGE_URI := $(ECR_REPO_PREFIX)/$(call get_ecr_repo,handler_1):$(IMAGE_TAG))

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

# Print IMAGE_TAG for use in Terraform
print-IMAGE_TAG: compute-image-tag
	@echo $(IMAGE_TAG)

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
venv: $(SERVICES:%=$(BACKEND)/%/venv)

$(BACKEND)/%/venv:
	$(PYTHON) -m venv $(BACKEND)/$*/$(VENV)
	$(BACKEND)/$*/$(VENV)/bin/pip install --upgrade pip

# Install dependencies for all services
install: venv
	$(foreach service,$(SERVICES),$(BACKEND)/$(service)/$(VENV)/bin/pip install -r $(BACKEND)/$(service)/requirements.txt;)

# Run tests for all services
test: install
	$(foreach service,$(SERVICES),test -d $(BACKEND)/$(service)/tests && $(BACKEND)/$(service)/$(VENV)/bin/pytest $(BACKEND)/$(service)/tests || echo "No tests for $(service)";)

# Build Docker images for all services
build: compute-image-tag
	$(foreach service,$(SERVICES), \
		docker buildx build --platform linux/amd64 --provenance=false -t $(ECR_REPO_PREFIX)/$(call get_ecr_repo,$(service)):$(IMAGE_TAG) $(BACKEND)/$(service); \
	)

# Push Docker images to ECR
push-ecr: build
	@aws ecr get-login-password --region $(AWS_REGION) | docker login --username AWS --password-stdin $(ECR_REPO_PREFIX)
	$(foreach service,$(SERVICES), \
		docker push $(ECR_REPO_PREFIX)/$(call get_ecr_repo,$(service)):$(IMAGE_TAG); \
		docker rmi $(ECR_REPO_PREFIX)/$(call get_ecr_repo,$(service)):$(IMAGE_TAG) || true; \
	)

# Set up ECR repositories for all services
setup-ecr:
	@chmod +x scripts/setup_ecr.sh
	$(foreach service,$(SERVICES),scripts/setup_ecr.sh $(call get_ecr_repo,$(service)) $(AWS_REGION);)

# Drop ECR repositories for all services
drop-ecr:
	@chmod +x scripts/drop_ecr.sh
	$(foreach service,$(SERVICES),scripts/drop_ecr.sh $(call get_ecr_repo,$(service)) $(AWS_REGION);)

# Clean up
clean:
	rm -rf $(foreach service,$(SERVICES),$(BACKEND)/$(service)/$(VENV) $(BACKEND)/$(service)/__pycache__ $(BACKEND)/$(service)/src/__pycache__ $(BACKEND)/$(service)/*.pyc $(BACKEND)/$(service)/src/*.pyc)
	rm -f .image_tag# Phony targets

# Phony targets
.PHONY: all venv install test build setup-ecr push-ecr drop-ecr clean print-vars print-IMAGE_TAG update-tfvars compute-image-tag
