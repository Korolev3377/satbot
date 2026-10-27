# ----- Python Standard Library ----- #
import logging
import os
import asyncio
import sys

# ----- Discord Python Library ----- #
import discord

# ----- Local Modules ----- #
from bot.cli import Cli
from bot.commandtree import CommandTree

Log = logging.getLogger(__name__)

if token_path := os.environ.get("SATBOT_TOKEN_PATH"):
    with open(os.path.join(token_path), 'r') as f:
        TOKEN = f.read().strip()
else:
    Log.critical("Discord token not found")
    exit(1)


if __name__ == '__main__':
    kwargs = dict(arg.split('=') for arg in sys.argv[1:] if '=' in arg)
    loglevel_numeric = getattr(logging, "INFO")
    if loglevel := kwargs.get("--log"):
        if loglevel.upper() in ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"]:
            loglevel_numeric = getattr(logging, loglevel.upper())
    logging.basicConfig(filename='log', level=loglevel_numeric, format="%(asctime)s [ %(levelname)-8s ] %(name)s:\n%(message)s\n")

    discordLogger = logging.getLogger('discord')
    discordLogger.setLevel(logging.INFO)
    discordGatewayLogger = logging.getLogger('discord.gateway')
    discordGatewayLogger.setLevel(logging.WARN)

    Log.info("Programm started")
    client = Cli(intents=discord.Intents.all())
    client.add_tree(CommandTree(client=client, global_commandlist=["bot_settings_cmd"]))
    try:
        client.run(TOKEN, reconnect=True)
    except KeyboardInterrupt:
        Log.info("Programm closed with KeyboardInterrupt")