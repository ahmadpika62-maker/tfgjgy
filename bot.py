import logging

import discord
from discord.ext import commands

from config import load_settings, token_fingerprint
from welcome import build_welcome_embed, member_snapshot


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
logger = logging.getLogger("roman_xp_welcome")


class WelcomeBot(commands.Bot):
    def __init__(self, welcome_channel_id: int) -> None:
        intents = discord.Intents.none()
        intents.guilds = True
        intents.members = True
        super().__init__(command_prefix=commands.when_mentioned, intents=intents)
        self.welcome_channel_id = welcome_channel_id
        self._welcomed_join_events: set[tuple[int, int]] = set()

    async def setup_hook(self) -> None:
        logger.info("Welcome join-event handler registered")

    async def on_ready(self) -> None:
        if self.user:
            logger.info("Connected as %s", self.user.name)

    async def on_member_join(self, member: discord.Member) -> None:
        event_key = (member.guild.id, member.id)
        if event_key in self._welcomed_join_events:
            logger.info("Skipped duplicate join event for display name %s", member.display_name)
            return
        self._welcomed_join_events.add(event_key)

        channel = member.guild.get_channel(self.welcome_channel_id)
        if channel is None:
            logger.error("Welcome channel %s was not found in guild %s", self.welcome_channel_id, member.guild.name)
            return
        if not isinstance(channel, discord.TextChannel):
            logger.error("Configured welcome channel is not a text channel")
            return

        try:
            await channel.send(
                embed=build_welcome_embed(member_snapshot(member)),
                allowed_mentions=discord.AllowedMentions.none(),
            )
            logger.info("Sent welcome message for display name %s", member.display_name)
        except discord.DiscordException:
            logger.exception("Could not send welcome message to the configured channel")


def create_bot() -> WelcomeBot:
    settings = load_settings()
    return WelcomeBot(settings.welcome_channel_id)


if __name__ == "__main__":
    settings = load_settings()
    logger.info("Discord token variable: PRESENT")
    logger.info("Token whitespace: %s", "NONE" if settings.token == settings.token.strip() else "TRIMMED")
    logger.info("Surrounding quotes: %s", "NONE" if not (len(settings.token) >= 2 and settings.token[0] == settings.token[-1] and settings.token[0] in {'\'', '"'}) else "REMOVED")
    logger.info('"Bot " prefix: %s', "NOT PRESENT" if not settings.token.lower().startswith("bot ") else "PRESENT")
    logger.info("Token fingerprint: %s", token_fingerprint(settings.token))

    try:
        create_bot().run(settings.token, log_handler=None)
    except discord.LoginFailure:
        logger.critical(
            "Discord authentication failed. Possible causes: wrong bot token, revoked/regenerated token, wrong credential type, malformed environment variable, or incorrect Railway secret."
        )
        raise
