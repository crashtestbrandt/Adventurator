.PHONY: dev test lint type run docker

uv:
	curl -LsSf https://astral.sh/uv/install.sh | sh

dev:
	uv venv || true
	. .venv/bin/activate && uv pip install -r requirements.txt
	. uv pip install -e .

run:
	. .venv/bin/activate && UVICORN_LOG_LEVEL=info uvicorn --app-dir src Adventorator.app:app --reload --host 0.0.0.0 --port 18000

tunnel:
	cloudflared tunnel --url http://127.0.0.1:18000

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

db-up:
	docker run --rm -d --name advdb -e POSTGRES_PASSWORD=adventorator \
		-e POSTGRES_USER=adventorator -e POSTGRES_DB=adventorator \
		-p 5432:5432 postgres:16

alembic-init:
	alembic init -t async migrations

alembic-rev:
	alembic revision --autogenerate -m "$(m)"

alembic-up:
	alembic upgrade head

alembic-down:
	alembic downgrade -1

