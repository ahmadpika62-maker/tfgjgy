from dataclasses import dataclass
import hashlib
import os

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    token: str
    welcome_channel_id: int


def token_fingerprint(token: str) -> str:
    return hashlib.sha256((token or "").encode("utf-8")).hexdigest()[:16]


def sanitize_discord_bot_token(raw_value: str) -> str:
    token = (raw_value or "").strip()
    if not token:
        raise RuntimeError("DISCORD_BOT_TOKEN is missing")

    if len(token) >= 2 and token[0] == token[-1] and token[0] in {"'", '"'}:
        token = token[1:-1].strip()

    if not token:
        raise RuntimeError("DISCORD_BOT_TOKEN is missing")

    if token.lower().startswith("bot "):
        raise RuntimeError("DISCORD_BOT_TOKEN must be the raw Discord bot token, not a 'Bot ' prefixed value")

    return token


def load_settings() -> Settings:
    load_dotenv()

    token = sanitize_discord_bot_token(os.getenv("DISCORD_BOT_TOKEN", ""))
    channel_id = os.getenv("WELCOME_CHANNEL_ID", "").strip()

    if not channel_id:
        raise RuntimeError("WELCOME_CHANNEL_ID is required")

    try:
        parsed_channel_id = int(channel_id)
    except ValueError as exc:
        raise RuntimeError("WELCOME_CHANNEL_ID must be a numeric Discord channel ID") from exc

    if parsed_channel_id <= 0:
        raise RuntimeError("WELCOME_CHANNEL_ID must be positive")

    return Settings(token=token, welcome_channel_id=parsed_channel_id)
