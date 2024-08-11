SHELL := /bin/bash

.PHONY: run-dev-server
run-dev-server:
	@echo "Running development server..."
	pwd
	@set -a; source .local-secrets; set +a; poetry run functions-framework --source=cloud-function/main.py --target=main --debug
