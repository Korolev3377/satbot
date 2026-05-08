# ----- Python Standard Library ----- #
import logging

# ----- Discord Python Library ----- #
import discord

# ----- Local Modules ----- #
from .commands import get_command

Log = logging.getLogger(__name__)


class CommandTree(discord.app_commands.CommandTree):
    def __init__(self, commandlist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.clear_commands(guild=None)

        Log.debug(f"Add commands -> {commandlist}")
        for cmd_name in commandlist:
            if command := get_command(cmd_name):
                self.add_command(command, guild=None)
            else:
                Log.error(f"Fail to add command <{cmd_name}>")