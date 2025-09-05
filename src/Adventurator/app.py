# app.py

from fastapi import FastAPI, Request, HTTPException
from Adventurator.logging import setup_logging
from Adventurator.config import load_settings
from Adventurator.crypto import verify_ed25519
from Adventurator.discord_schemas import Interaction
from Adventurator.responder import respond_pong, respond_deferred
import structlog
import asyncio

log = structlog.get_logger()
settings = load_settings()
setup_logging()
app = FastAPI(title="Adventurator")

DISCORD_SIG_HEADER = "X-Signature-Ed25519"
DISCORD_TS_HEADER = "X-Signature-Timestamp"

@app.post("/interactions")
async def interactions(request: Request):
    raw = await request.body()
    sig = request.headers.get(DISCORD_SIG_HEADER)
    ts  = request.headers.get(DISCORD_TS_HEADER)
    if not sig or not ts:
        raise HTTPException(status_code=401, detail="missing signature headers")

    if not verify_ed25519(settings.discord_public_key, ts, raw, sig):
        raise HTTPException(status_code=401, detail="bad signature")

    inter = Interaction.model_validate_json(raw)

    # Ping = 1
    if inter.type == 1:
        return respond_pong()

    # Anything else: immediately DEFER (type 5) to satisfy the 3s budget.
    # In the background you would enqueue work; here we just simulate.
    asyncio.create_task(_background_followup_stub(inter))
    return respond_deferred()

async def _background_followup_stub(inter: Interaction):
    # TODO: implement webhook follow-up using interaction token
    # For Phase 0 we just log it; Phase 1 will send a follow-up message.
    log.info("deferred_work", interaction_id=inter.id, name=inter.data.name if inter.data else None)
