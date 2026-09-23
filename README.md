# ROMAN XP Welcome Bot

A small official Discord bot that listens for guild member joins and posts one welcome embed in the configured server channel. It never sends DMs and never mentions the member.

## Current server channel

The existing welcome channel was verified in the Discord server as `🌐・welcome-here`. Its current ID is included in `.env.example`; replace it if the channel changes.

## Setup

1. Install Python 3.11 or newer.
2. Create and activate a virtual environment:

   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. Install dependencies:

   ```powershell
   py -m pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env`.
5. Set `DISCORD_BOT_TOKEN` locally. Never paste it into chat or commit `.env`.
6. Confirm `WELCOME_CHANNEL_ID` points to the existing welcome text channel.

## Bot configuration

The bot requires the official Discord Bot API with the Server Members intent enabled for the bot application. It does not create an OAuth2 invite in this phase and does not change server permissions.

The bot needs permission to view and send messages in the configured welcome channel. No DM permission or user-token automation is used.

## Run

```powershell
py bot.py
```

Startup logs confirm that the bot connected and the join handler was registered. Runtime errors are logged locally without terminating the process for a failed welcome send.

## Local test mode

The embed builder is pure and can be tested without connecting to Discord:

```powershell
py -m pytest
```

This tests display-name-only content and optional avatar handling. It does not create fake Discord accounts or send messages.

## Join behavior

When Discord emits `on_member_join`, the bot:

1. Reads the member display name and public display avatar.
2. Resolves `WELCOME_CHANNEL_ID` inside the joining guild.
3. Sends one embed to that text channel.
4. Does not DM, mention, or include the numeric user ID.

Duplicate events are de-duplicated for the lifetime of the running process. A restart-safe persistent event store is intentionally not included in this first phase.
