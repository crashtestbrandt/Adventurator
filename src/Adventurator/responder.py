# responder.py

from fastapi import Response
from Adventurator.discord_schemas import DeferResponse, PongResponse
import orjson

def orjson_response(data: dict) -> Response:
    return Response(content=orjson.dumps(data), media_type="application/json")

def respond_pong() -> Response:
    return orjson_response(PongResponse(type=1).model_dump())

def respond_deferred() -> Response:
    return orjson_response(DeferResponse(type=5).model_dump())
