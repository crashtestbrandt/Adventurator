# responder.py

from fastapi import Response
import httpx
from Adventorator.discord_schemas import DeferResponse, PongResponse
from Adventorator.config import load_settings
import orjson

_settings = load_settings()

def orjson_response(data: dict) -> Response:
    return Response(content=orjson.dumps(data), media_type="application/json")

def respond_pong() -> Response:
    return orjson_response(PongResponse(type=1).model_dump())

def respond_deferred() -> Response:
    return orjson_response(DeferResponse(type=5).model_dump())

async def followup_message(application_id: str, token: str, content: str, ephemeral: bool=False):
    url = f"https://discord.com/api/v10/webhooks/{application_id}/{token}"
    flags = 64 if ephemeral else 0  # 64 = EPHEMERAL
    payload = {"content": content, "flags": flags}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.post(url, content=orjson.dumps(payload), headers={"Content-Type":"application/json"})
        r.raise_for_status()
