.PHONY: check lint type test format db-up db-new db-hist run

check: lint type test       ## Run all checks: lint → types → tests

lint:                       ## Run ruff linter
	ruff check .

type:                       ## Run mypy type checker
	mypy .

test:                       ## Run all tests
	pytest -v

format:                     ## Format code with ruff
	ruff format .

db-up:                      ## Apply all pending migrations
	alembic upgrade head

db-new:                     ## Create a new migration
	alembic revision --autogenerate -m "$(message)"

db-hist:                    ## Show migration history
	alembic history

run:                        ## Start the API server (development)
	uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
