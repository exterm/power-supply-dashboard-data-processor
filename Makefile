SHELL := /bin/bash

.PHONY: run-dev-server
run-dev-server:
	@echo "Running development server..."
	@set -a; source .local-secrets; set +a; poetry run functions-framework --source=cloud-function/main.py --target=main --debug

.PHONY: test
test:
	@echo "Running tests..."
	@set -a; source .local-secrets; set +a; poetry run pytest cloud-function/utils/*.py
