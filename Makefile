.PHONY: run-dev-server

run-dev-server:
	@echo "Running development server..."
	@poetry run functions-framework --target=main --debug
