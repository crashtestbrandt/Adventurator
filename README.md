# Adventorator

*Dungeon Master as a Service (DMaaS)*

A Discord-native Dungeon Master bot that runs tabletop RPG campaigns directly in chat. It blends deterministic game mechanics with AI-powered narration, letting players experience a text-based campaign without needing a human DM online 24/7.

![](/docs/images/usage-slash-check.jpeg)

---

* [Overview](#overview)
* [Prerequisites](#prerequisites) & [Quickstart](#quickstart)
* [Repo Structure](#repo-structure)
* [Contributing](./CONTRIBUTING.md)

---

## Overview

**✨ Features (MVP and beyond)**

* Discord-first gameplay
* Slash commands (/roll, /check, /sheet, /act) and interactive components (buttons, modals).
* Combat threads with initiative order, per-turn locks, and timeouts.
* Ephemeral prompts for individual player actions.
* Deterministic rules engine
* Full SRD 5e dice system (advantage/disadvantage, crits, modifiers).
* Ability checks, saving throws, AC, HP, conditions.
* Initiative and turn management with audit logging.
* Campaign persistence
* JSON-schema character sheets stored in Postgres (or SQLite for dev).
* Adventure content as structured "nodes" (locations, NPCs, encounters).
* Automatic transcripts and neutral session summaries.
* AI-assisted narration (behind feature flag)
* LLM proposes DCs and narrates outcomes; Rules Service enforces mechanics.
* Retrieval-augmented memory: previous sessions, adventure nodes, campaign facts.
* Configurable tone, verbosity, and house rules.
* Developer experience
* Python 3.10+, FastAPI interactions endpoint, Redis for locks/queues.
* Pydantic models, property-based tests for dice & checks.
* Structured JSON logs, reproducible seeds, feature flags for every subsystem.

**🏗 Architecture**

* Discord Interactions API → FastAPI app → defer in <3s → enqueue background job.
* Rules Service (pure Python functions) → resolves rolls, DCs, initiative, mutations.
* Database → campaign state, character sheets, transcripts.
* Optional LLM → narrates and proposes rulings, never mutates state directly.
* Workers → long-running tasks: narration, summarization, content ingestion.
 
**Diagram: High-Level Architecture**

```mermaid
flowchart TD
  %% === External ===
  U[Player on Discord]:::ext
  DP[Discord Platform<br/>App Commands and Interactions]:::ext
  WH[Discord Webhooks API<br/>Follow-up Messages]:::ext

  %% === Network Edge ===
  CF[cloudflared Tunnel<br/>TLS - trusted CA]:::edge

  %% === App ===
  subgraph APP[Adventorator Service - FastAPI]
    A[Interactions Endpoint<br/>path: /interactions]
    SIG[Ed25519 Verify<br/>X-Signature-* headers]
    DISP[Command Dispatcher]
    RESP[Responder<br/>defer and follow-up]
    RULES[Rules Engine - Phase 1<br/>Dice, Checks, Adv/Dis]
    CTX[Context Resolver - Phase 2<br/>Campaign, Player, Scene]
    TRANS[Transcript Logger - Phase 2]
  end

  %% === Data ===
  subgraph DATA[Data Layer]
    DB[(Postgres or SQLite<br/>campaigns, players, characters, scenes, transcripts)]:::data
    MIG[Alembic Migrations]:::ops
  end

  %% === Tooling ===
  REG[scripts/register_commands.py<br/>Guild command registration]:::ops
  LOG[Structured Logs<br/>structlog and orjson]:::ops
  TEST[Tests<br/>pytest and hypothesis]:::ops

  %% === Flows ===
  U -->|Slash command| DP
  DP -->|POST /interactions<br/>signed| CF
  CF --> A

  A --> SIG
  SIG -->|valid| DISP
  A -.->|invalid| RESP

  %% Phase 0: immediate defer
  DISP --> RESP

  %% Phase 1: deterministic mechanics
  DISP --> RULES
  RULES --> RESP

  %% Phase 2: persistence and context
  DISP --> CTX
  CTX --> DB
  RESP -->|write bot output| TRANS
  TRANS --> DB

  %% Follow-up delivery
  RESP -->|POST follow-up| WH
  WH --> DP --> U

  %% Tooling edges
  REG --> DP
  MIG --> DB
  TEST -.-> RULES
  TEST -.-> A
  LOG -.-> APP

  %% Styles
  classDef ext  fill:#eef7ff,stroke:#4e89ff,stroke-width:1px,color:#0d2b6b
  classDef edge fill:#efeaff,stroke:#8b5cf6,stroke-width:1px,color:#2b1b6b
  classDef data fill:#fff7e6,stroke:#f59e0b,stroke-width:1px,color:#7c3e00
  classDef ops  fill:#eefaf0,stroke:#10b981,stroke-width:1px,color:#065f46 
```

**Diagram: Interaction Lifecycle (Phase 0-2)**

```mermaid
sequenceDiagram
  autonumber
  participant User as Player (Discord)
  participant Discord as Discord Platform
  participant CF as cloudflared Tunnel
  participant API as Adventorator /interactions
  participant SIG as Ed25519 Verify
  participant DISP as Dispatcher
  participant RULES as Rules Engine
  participant CTX as Context Resolver
  participant DB as Database
  participant WH as Discord Webhooks

  User->>Discord: /roll expr:2d6+3
  Discord->>CF: POST /interactions (signed)
  CF->>API: Forward request
  API->>SIG: Verify signature
  SIG-->>API: OK (or 401 if bad)

  API-->>Discord: Defer (type=5) ≤3s

  API->>DISP: route command ("roll")
  DISP->>RULES: parse & roll (deterministic)
  RULES-->>DISP: result (rolls, total)

  %% Phase 2 logging & context (optional for Phase 0/1)
  DISP->>CTX: resolve campaign/player/scene
  CTX->>DB: upsert/get rows
  DISP->>DB: write transcript (player input)
  DISP->>DB: write transcript (bot output meta)

  DISP->>WH: POST follow-up message (narration + mechanics)
  WH-->>Discord: deliver message
  Discord-->>User: Show result
```

**🔒 Design philosophy**

* AI narrates, rules engine rules. No silent HP drops or fudged rolls.
* Human-in-the-loop. GM override commands (/gm) and rewind via event sourcing.
* Defensive defaults. Feature flags, degraded modes (rules-only if LLM/vector DB down).
* Reproducible. Seeded RNG, append-only logs, golden transcripts for regression tests.

**🚧 Status**

* [X] Phase 0: Verified interactions endpoint, 3s deferral, logging.
* [X] Phase 1: Deterministic dice + checks, /roll and /check commands.
* [ ] Phase 2: Persistence (campaigns, characters, transcripts).
* [ ] Phase 3: Shadow LLM narrator, proposal-only.
* [ ] Phase 4+: Combat system, content ingestion, GM controls, premium polish.

**🔜 Roadmap**

* Add /sheet CRUD with strict JSON schema.
* Initiative + combat encounters with Redis turn locks.
* Adventure ingestion pipeline for SRD or custom campaigns.
* Optional Embedded App for lightweight maps/handouts in voice channels.

---

## Prerequisites

- Bash-like environment
- Docker
- Python > 3.10
- [uv](https://docs.astral.sh/uv/getting-started/installation/)

    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

- [cloudflared](https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/)

    ```bash
    # Linux
    wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-arm
    sudo cp ./cloudflared-linux-arm /usr/local/bin/cloudflared
    sudo chmod +x /usr/local/bin/cloudflared
    cloudflared -v

    # MacOS
    brew install cloudflared
    ```

## Quickstart

```bash
cp .env.example .env    # <-- Add secrets
make dev                # Install Python requirements
make run                # Start local dev server on 18000
```

### Optional: Anonymous Cloudflare tunnel:

```bash
make tunnel
```

In the output, you should see something like:

    ```
    2025-09-05T18:57:54Z INF |  Your quick Tunnel has been created! Visit it at (it may take some time to be reachable):  |
    2025-09-05T18:57:54Z INF |  https://rooms-mechanics-tires-mats.trycloudflare.com  
    ---

Discord can now reach your dev server using that URL + `/interactions`.

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
│   └── Adventorator
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