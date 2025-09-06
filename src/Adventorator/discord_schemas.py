# discord_schemas.py

from pydantic import BaseModel
from typing import Any, Literal

class InteractionData(BaseModel):
    id: str | None = None
    name: str | None = None
    type: int | None = None
    options: list[dict[str, Any]] | None = None

class Interaction(BaseModel):
    id: str
    type: int
    token: str
    application_id: str
    data: InteractionData | None = None

class DeferResponse(BaseModel):
    type: Literal[5]  # DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE

class PongResponse(BaseModel):
    type: Literal[1]  # PONG for pings (type 1)
