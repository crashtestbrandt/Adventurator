# config.py

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
import tomllib
from pathlib import Path

class Settings(BaseSettings):
    env: str = Field(default="dev")
    database_url: str = Field(default="sqlite+aiosqlite:///./adventorator.sqlite3")
    discord_public_key: str
    discord_bot_token: str | None = None
    features_llm: bool = False
    features_rules: bool = False
    features_combat: bool = False
    response_timeout_seconds: int = 3

    model_config = SettingsConfigDict(env_prefix="", case_sensitive=False, env_file=".env", extra="ignore")

def load_settings() -> Settings:
    cfg_path = Path("config.toml")
    data = {}
    if cfg_path.exists():
        with cfg_path.open("rb") as f:
            t = tomllib.load(f)
            data.update({
                "env": t.get("app", {}).get("env", "dev"),
                "features_llm": t.get("features", {}).get("llm", False),
                "features_rules": t.get("features", {}).get("rules", False),
                "features_combat": t.get("features", {}).get("combat", False),
                "response_timeout_seconds": t.get("discord", {}).get("response_timeout_seconds", 3),
            })
    return Settings(**data)  # .env overrides TOML
