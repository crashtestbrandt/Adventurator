.PHONY: dev test lint type run docker

dev:
	uv venv || true
	. .venv/bin/activate && uv pip install -r requirements.txt

run:
	. .venv/bin/activate && UVICORN_LOG_LEVEL=info uvicorn Adventurator.app:app --reload --port 8000

test:
	. .venv/bin/activate && pytest

lint:
	ruff check src tests

type:
	mypy src

format:
	ruff format src tests

clean:
	rm -rf .venv
