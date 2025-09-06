# discord_schemas.py

from pydantic import BaseModel
from typing import Any, Literal, Optional

class User(BaseModel):
    id: str
    username: str
    discriminator: Optional[str] = None
    avatar: Optional[str] = None
    global_name: Optional[str] = None

class Member(BaseModel):
    user: User
    nick: Optional[str] = None
    roles: list[str] = []
    joined_at: Optional[str] = None
    permissions: Optional[str] = None

class Channel(BaseModel):
    id: str
    guild_id: Optional[str] = None
    name: Optional[str] = None
    type: Optional[int] = None

class Guild(BaseModel):
    id: str
    locale: Optional[str] = None
    features: list[str] = []

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
    guild_id: Optional[str] = None
    channel_id: Optional[str] = None
    member: Optional[Member] = None
    guild: Optional[Guild] = None
    channel: Optional[Channel] = None

class DeferResponse(BaseModel):
    type: Literal[5]  # DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE

class PongResponse(BaseModel):
    type: Literal[1]  # PONG for pings (type 1)
