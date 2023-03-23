from discord import app_commands
from discord.app_commands import locale_str as _ls

from .bf_cmd import bf_cmd
from .ttt_cmd import tictactoe_cmd
from .gol_cmd import gol_cmd

grp_lc = {
    'enjoy_name': {
        'en': 'game',
        'ru': 'игра'
    },
    'enjoy_desc': {
        'en': 'Enjoy stuff.',
        'ru': 'Развлекательное развлечение.'
    }
}

enjoy_grp = app_commands.Group(
    name=_ls(
        'enjoy_name',
        extras={
            'dict': grp_lc.get('enjoy_name'),
            'type': 'cmd'
        }
    ),
    description=_ls(
        'enjoy_desc',
        extras={
            'dict': grp_lc.get('enjoy_desc'),
            'type': 'cmd'
        }
    )
)

enjoy_grp.add_command(bf_cmd)
enjoy_grp.add_command(tictactoe_cmd)
enjoy_grp.add_command(gol_cmd)
