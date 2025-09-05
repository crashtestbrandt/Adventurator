# Adventurator

## Quickstart

```bash
cp .env.example .env  # put your actual DISCORD_PUBLIC_KEY
make run
```


## Repo Structure

```
Adeventurator/
├─ src/
│  └─ Adventurator/
│     ├─ __init__.py
│     ├─ config.py
│     ├─ logging.py
│     ├─ crypto.py           # Ed25519 signature verify
│     ├─ discord_schemas.py  # Pydantic models for interactions I/O
│     ├─ app.py              # FastAPI app, /interactions route
│     └─ responder.py        # defer+followup helpers
├─ tests/
│  ├─ test_crypto.py
│  ├─ test_interactions.py
│  └─ data/
│     └─ interaction_example.json
├─ .env.example
├─ config.toml
├─ pyproject.toml
├─ Makefile
├─ Dockerfile
└─ README.md
```

## Environment

```
brew install uv
uv venv
source .venv/bin/activate
uv pip install --upgrade pip
uv pip install -r requirements.txt
```