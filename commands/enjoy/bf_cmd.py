import discord
from discord import app_commands
from discord.app_commands import locale_str as _ls

from translator.main import T
from environment.variable import *

from .games.bf_game import Brainfuck

BRAINFUCK_NAME = 'bf_name'
BRAINFUCK_DESC = "bf_desc"

_locale = {
    BRAINFUCK_NAME: {
        EN: 'brainfuck',
        RU: 'брайнфак'
    },
    BRAINFUCK_DESC: {
        EN: 'Emulate bf code.',
        RU: 'Эмулирует бф код.'
    }
}


@app_commands.command(
    name=namedesc(BRAINFUCK_NAME, _locale),
    description=namedesc(BRAINFUCK_DESC, _locale),
    extras={IS_BROKEN: False}
)
async def bf_cmd(interaction, code: str, *, enter: str = None):
    await interaction.response.defer(thinking=True)
    await interaction.followup.send("`"+Brainfuck().run(code, enter)[:1998]+"`")
