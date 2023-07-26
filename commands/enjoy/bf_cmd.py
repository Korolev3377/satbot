import discord
from discord import app_commands
from discord.app_commands import locale_str as _ls

from translator.main import T
from environment.variable import *

from .games.bf_game import Brainfuck

BRAINFUCK_NAME = 'bf_name'
BRAINFUCK_DESC = "bf_desc"
CODE = "code"
ENTER = "enter"

_locale = {
    BRAINFUCK_NAME: {
        EN: 'brainfuck',
        RU: 'брэйнфак'
    },
    BRAINFUCK_DESC: {
        EN: 'Brainfuck code reader',
        RU: 'Запустить брэйнфак-код'
    },
    CODE: {EN: "code",
           RU: "код"},
    ENTER: {EN: "input",
            RU: "ввод"}
}


@app_commands.command(
    name=namedesc(BRAINFUCK_NAME, _locale),
    description=namedesc(BRAINFUCK_DESC, _locale),
    extras={IS_BROKEN: False}
)
@app_commands.rename(code=namedesc(CODE, _locale), enter=namedesc(ENTER, _locale))
async def bf_cmd(interaction, code: str, *, enter: str = None):
    await interaction.response.defer(thinking=True)
    await interaction.followup.send("`"+Brainfuck().run(code, enter)[:1998]+"`")
