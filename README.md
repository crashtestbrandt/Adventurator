# Adventurator

*Dungeon Master as a Service (DMaaS)*

A Discord-native Dungeon Master bot that runs tabletop RPG campaigns directly in chat. It blends deterministic game mechanics with AI-powered narration, letting players experience a text-based campaign without needing a human DM online 24/7.

---

- [Repo Structure](#repo-structure)
- [Development](#development)

---

## Prerequisites

- Bash-like environment
- Python > 3.10
- [uv](https://formulae.brew.sh/formula/uv)
- [cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)
- Docker

## Quickstart

```bash
cp .env.example .env  # <— Add secrets
make dev
make run
```

---

## Repo Structure

```
├── Dockerfile
├── LICENSE
├── Makefile
├── README.md
├── config.toml
├── pyproject.toml
├── requirements.txt
├── scripts
│   └── register_commands.py
├── src
│   └── Adventurator
│       ├── __init__.py
│       ├── app.py
│       ├── config.py
│       ├── crypto.py
│       ├── discord_schemas.py
│       ├── logging.py
│       ├── responder.py
│       └── rules
│           ├── __init__.py
│           ├── checks.py
│           └── dice.py
└── tests
    ├── data
    │   └── interaction_example.py
    ├── test_advantage.py
    ├── test_checks.py
    ├── test_crypto.py
    ├── test_dice.py
    └── test_interactions.py
    
```

---

## Development

**Guiding Principles**

* LLM augments, rules engine rules. All state changes go through deterministic code.
* Always ack in ≤3s. Immediately defer and finish work off-thread.
* Everything behind feature flags. Roll forward/Rollback without deploy.
* Shadow first. New subsystems run in observation mode before taking action.
* Write once, test twice. Unit+property tests for math; golden logs for flows.

 

