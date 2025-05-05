# Python interpreter
PYTHON = python3

# Backend directory
BACKEND = chatbot

# Service directories
SERVICES = handler 

# Virtual environment directory
VENV = venv

# Output directory for ZIP files
DIST = dist

# Deployment stage (dev, staging, prod)
STAGE ?= prod

SERVICE_BUCKET_MAP = handler:llmtoolflow-$(STAGE)-handler-artifact-bucket 

# Function to get bucket for a service
get_bucket = $(word 2,$(subst :, ,$(filter $1:%,$(SERVICE_BUCKET_MAP))))

# Default target
all: install test package

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

# Create ZIP files for all services
package: install $(DIST)
	$(foreach service,$(SERVICES), \
		mkdir -p $(DIST)/$(service); \
		cp -r $(BACKEND)/$(service)/* $(DIST)/$(service)/; \
		$(BACKEND)/$(service)/$(VENV)/bin/pip install -r $(BACKEND)/$(service)/requirements.txt -t $(DIST)/$(service)/; \
		$(BACKEND)/$(service)/$(VENV)/bin/pip install pydantic-core --platform manylinux2014_x86_64 -t $(DIST)/$(service)/ --implementation cp --python-version 3.13 --only-binary=:all: --upgrade pydantic; \
		rm -rf $(DIST)/$(service)/$(VENV); \
		cd $(DIST)/$(service) && zip -r ../$(service).zip . && cd ../../..; \
		rm -rf $(DIST)/$(service); \
	)

# Create dist directory
$(DIST):
	mkdir -p $(DIST)

# Set up S3 buckets for all services
setup-s3:
	@chmod +x scripts/setup_s3.sh
	$(foreach service,$(SERVICES),scripts/setup_s3.sh $(call get_bucket,$(service));)

# Upload ZIPs to S3
upload-s3: package
	$(foreach service,$(SERVICES),aws s3 cp $(DIST)/$(service).zip s3://$(call get_bucket,$(service))/$(service).zip;)

# Drop S3 buckets for all services
drop-s3:
	@chmod +x scripts/drop_s3.sh
	$(foreach service,$(SERVICES),scripts/drop_s3.sh $(call get_bucket,$(service));)# Clean up

clean:
	rm -rf $(DIST) $(foreach service,$(SERVICES),$(BACKEND)/$(service)/$(VENV) $(BACKEND)/$(service)/__pycache__ $(BACKEND)/$(service)/src/__pycache__ $(BACKEND)/$(service)/*.pyc $(BACKEND)/$(service)/src/*.pyc)# Phony targets

.PHONY: all venv install test package setup-s3 upload-s3 drop-s3 clean
