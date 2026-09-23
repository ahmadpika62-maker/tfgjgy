from dataclasses import dataclass
import os

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    token: str
    welcome_channel_id: int


def load_settings() -> Settings:
    load_dotenv()

    token = os.getenv("DISCORD_BOT_TOKEN", "").strip()
    channel_id = os.getenv("WELCOME_CHANNEL_ID", "").strip()

    if not token:
        raise RuntimeError("DISCORD_BOT_TOKEN is required")
    if not channel_id:
        raise RuntimeError("WELCOME_CHANNEL_ID is required")

    try:
        parsed_channel_id = int(channel_id)
    except ValueError as exc:
        raise RuntimeError("WELCOME_CHANNEL_ID must be a numeric Discord channel ID") from exc

    if parsed_channel_id <= 0:
        raise RuntimeError("WELCOME_CHANNEL_ID must be positive")

    return Settings(token=token, welcome_channel_id=parsed_channel_id)
