from dataclasses import dataclass

import discord


@dataclass(frozen=True)
class WelcomeMember:
    display_name: str
    avatar_url: str | None = None


def member_snapshot(member: discord.Member) -> WelcomeMember:
    avatar_url = str(member.display_avatar.url) if member.display_avatar else None
    return WelcomeMember(display_name=member.display_name, avatar_url=avatar_url)


def build_welcome_embed(member: WelcomeMember) -> discord.Embed:
    embed = discord.Embed(
        title="✨ 𝗪𝗘𝗟𝗖𝗢𝗠𝗘 ✨",
        description=(
            "Welcome to ROMAN XP!\n\n"
            f"Welcome, {member.display_name} 👋\n\n"
            "We are happy to have you here. Explore the server and use the support section when you need help."
        ),
        colour=discord.Colour.blurple(),
    )
    embed.set_footer(text="ROMAN XP")
    if member.avatar_url:
        embed.set_thumbnail(url=member.avatar_url)
    return embed
