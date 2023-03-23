from discord import app_commands
from discord.app_commands import locale_str as _ls

from .games.bf_game import Brainfuck

bf_lc = {
    'bf_name': {
        'en': 'brainfuck',
        'ru': 'брайнфак'
    },
    "bf_desc": {
        'en': 'Emulate bf code.',
        'ru': 'Эмулирует бф код.'
    }
}


@app_commands.command(
    name=_ls(
        'bf_name',
        extras={
            'dict': bf_lc.get('bf_name'),
            'type': 'cmd'
        }
    ),
    description=_ls(
        'bf_desc',
        extras={
            'dict': bf_lc.get('bf_desc'),
            'type': 'cmd'
        }
    ),
    extras={"broken": True}
)
async def bf_cmd(interaction, code: str, *, enter: str = None):
    await interaction.followup.send("`", Brainfuck().run(code, input), "`")
