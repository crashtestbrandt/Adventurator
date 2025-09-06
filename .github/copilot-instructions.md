# Copilot Instructions for Adventorator

Purpose: Equip AI coding agents to be productive immediately in this repo. Keep edits small, match existing patterns, and verify with tests.

## Architecture: what matters
- Entry point: `src/Adventorator/app.py` (FastAPI). Exposes `POST /interactions` for Discord. Always verify `X-Signature-*` with `crypto.verify_ed25519`, then defer within 3s via `responder.respond_deferred()`.
- Command flow: `app._dispatch_command()` handles slash commands (`roll`, `check`, `sheet`, `ooc`). Use `responder.followup_message()` to send webhook follow-ups.
- Rules engine (deterministic, no I/O): `src/Adventorator/rules/`
  - `dice.DiceRNG.roll(expr, advantage=False, disadvantage=False)` parses `XdY+Z`; adv/dis only for single d20. Returns `DiceRoll(rolls, total, crit, ...)`.
  - `checks.compute_check(CheckInput, d20_rolls)` computes ability checks (mods, proficiency, adv/dis). Returns `CheckResult` with `success` if `dc` provided.
- Persistence: SQLAlchemy (async) in `db.py`, models in `models.py`, and thin repos in `repos.py`. Use `session_scope()` context manager; commit happens on exit.
- Schemas and typing: Pydantic v2 models in `schemas.py` and `discord_schemas.py`. Character sheets use alias `class -> class_name` with `populate_by_name=True`.
- Logging: `logging.setup_logging()` configures structured JSON logs via structlog.
- Phase 3 narrator (shadow mode): `llm.py` provides `LLMClient` (Ollama-style API). Enabled by `features.llm=true` in `config.toml`; settings from `[llm]` (api_url, model_name, default_system_prompt). The `ooc` command writes the player's message to transcripts, builds a prompt from recent history (`repos.get_recent_transcripts`), calls `LLMClient.generate_response`, follows up to Discord, then logs bot output back to transcripts. LLM never mutates state directly.

## Dev workflows
- Setup: `make dev` (uv venv + install), run: `make run` (uvicorn on :18000). Optional tunnel: `make tunnel` for Discord callbacks.
- Database: `alembic upgrade head` before features needing persistence. Helper targets: `make alembic-rev m="msg"`, `make alembic-up`, `make alembic-down`. Local Postgres: `make db-up` (or default SQLite via `DATABASE_URL`).
- Tests: `make test` runs pytest with coverage; async fixtures in `tests/conftest.py`. Keep rules pure and fast; seed RNGs in tests as shown in `tests/test_dice.py`.
- Slash command registration: `scripts/register_commands.py` (reads `.env` for `DISCORD_*`). Uses global (not guild) registration by default.
  - Includes `ooc` command; switch to guild route for faster iteration (commented in file). The script loads `.env` from repo root and fails fast with helpful errors.

## Discord + cloudflared setup
- Start the app locally, then create a public tunnel:
  - `make run` → service at http://127.0.0.1:18000
  - `make tunnel` → copy the https://<random>.trycloudflare.com URL
- In Discord Developer Portal (Your App → General/Installation):
  - Interactions Endpoint URL: `<tunnel-url>/interactions`
  - Copy your Public Key into `.env` as `DISCORD_PUBLIC_KEY`
  - Create a bot and copy its token into `.env` as `DISCORD_BOT_TOKEN`
  - Note your Application ID as `DISCORD_APP_ID`; optionally set `DISCORD_GUILD_ID` for guild-scoped work
- Register slash commands:
  - `scripts/register_commands.py` posts to `applications/{APP_ID}/commands` (global). Global commands can take up to an hour to appear.
  - For faster dev, switch to guild route (see commented line in the script), then set `DISCORD_GUILD_ID`.
- Invite the bot to your server with scopes `applications.commands` and `bot`.

## Conventions to follow
- Keep interaction handler under 3s: return `respond_deferred()` quickly, then do work in a background task and `followup_message()`.
- DB access through `repos.py` functions; avoid embedding SQL in handlers. Always run inside `async with session_scope()`.
- Discord payloads: use `discord_schemas.Interaction`. Options for subcommands live one level deeper; reuse helpers `_subcommand` and `_option` in `app.py`.
  - Guild/Channel/Member models exist; `_infer_ids_from_interaction` now reads `inter.guild/channel/member.user` where available.
- Dice/Checks: advantage/disadvantage only alters single d20 rolls. Include the picked die in messages, e.g., see `app.py` formatting for `roll`/`check`.
- Settings: `config.load_settings()` merges `config.toml` then `.env`. Prefer reading values via `Settings` instead of `os.environ` (except one-off scripts).
- Logging: prefer structlog `log = structlog.get_logger()`; log events, not strings. Keep modules import-light to avoid .env coupling in early imports.
  - LLM conventions: only run when `features_llm` is enabled; handle timeouts/empty responses gracefully (see `llm.py` return strings) and always write both player and bot messages to transcripts.

## Environment checklist (.env.example)
- Copy `.env.example` → `.env` and fill values before running:
  - `DISCORD_PUBLIC_KEY` — from Developer Portal → General Information
  - `DISCORD_BOT_TOKEN` — from Bot settings
  - `DISCORD_APP_ID` — Application ID
  - `DISCORD_GUILD_ID` — optional for guild-scoped registration
  - `DATABASE_URL` — default SQLite is fine for dev (`sqlite+aiosqlite:///./adventorator.sqlite3`)
  - `ENV` — `dev`

## Adding features safely (examples)
- New slash command:
  1) Extend `scripts/register_commands.py` with the command schema and re-run it.
  2) Handle it in `_dispatch_command()`; parse options with `_option()`/`_subcommand()`.
  3) Do logic (rules or repos) and `await followup_message(...)`.
- New model + migration:
  1) Add SQLAlchemy model in `models.py`.
  2) `alembic revision --autogenerate -m "add <model>"` then `alembic upgrade head`.
  3) Add repo helpers; write a thin test in `tests/` using the `db` fixture.
- LLM usage:
  1) Read defaults from `config.toml` `[llm]`. Toggle with `[features].llm=true`.
  2) Build prompts from transcripts (`repos.get_recent_transcripts`) and map author→role (player→user, bot→assistant).
  3) Call `await LLMClient.generate_response(messages)`; on None/empty, follow up with an ephemeral apology and skip mutations.

## External integrations
- Discord: Interactions signature check via NaCl; follow-ups via `POST /webhooks/{app_id}/{token}` (see `responder.py`).
- Databases: SQLite/local by default; Postgres recommended in prod. Async drivers are auto-normalized in `db._normalize_url()`.

## Files to study first
- `src/Adventorator/app.py`, `responder.py`, `discord_schemas.py`, `rules/dice.py`, `rules/checks.py`, `db.py`, `models.py`, `repos.py`, `schemas.py`, `llm.py`.
- Tests: `tests/test_dice.py`, `tests/test_checks.py`, `tests/test_repos.py`, `tests/test_interactions.py` for expected behavior and message formats.
  - See `tests/test_ollama_chat_nostream.py` for example Ollama response structure and prompt preparation (reference only).

Notes
- Do not log or commit real tokens. Use `.env.example` for templates if adding new env keys.
- Keep PRs small; prefer pure functions in `rules/` and async I/O isolated to `app.py`/`repos.py`.
