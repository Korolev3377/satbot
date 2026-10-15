# ----- Python Standard Library ----- #
import logging

# ----- Discord Python Library ----- #
import discord

# ----- Local Modules ----- #
from .commands import get_command

Log = logging.getLogger(__name__)


class CommandTree(discord.app_commands.CommandTree):
    def __init__(self, global_commandlist, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.global_commandlist = global_commandlist
        self.clear_commands(guild=None)
        for g in self.client.guilds:
            self.clear_commands(guild=g)

        Log.debug(f"Add commands -> {self.global_commandlist}")
        for cmd_name in self.global_commandlist:
            if command := get_command(cmd_name):
                self.add_command(command, guild=None)
            else:
                Log.error(f"Fail to add command <{cmd_name}>")