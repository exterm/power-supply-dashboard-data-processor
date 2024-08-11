.PHONY: run-dev-server

run-dev-server:
	@echo "Running development server..."
	@poetry run functions-framework --source=cloud-function/main.py --target=main --debug
