.PHONY: dev test lint type run docker

uv:
	curl -LsSf https://astral.sh/uv/install.sh | sh

dev:
	uv venv || true
	. .venv/bin/activate && uv pip install -r requirements.txt

run:
	. .venv/bin/activate && UVICORN_LOG_LEVEL=info uvicorn --app-dir src Adventurator.app:app --reload --host 0.0.0.0 --port 18000

tunnel:
	cloudflared tunnel --url http://127.0.0.1:8000

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
