import discord

from discord import app_commands
from discord.app_commands import locale_str as _ls

from translator.main import T
from environment.variable import *

_locale = {
    "bonk_usr": {
        EN: "{_} horny!",
        RU: "{_} хорни!"
    },
    "bonk_name": {
        EN: "tangakk-horny",
        RU: "тангакк-хорни"
    },
    "bonk_desc": {
        EN: "command-description",
        RU: "описание-комманды"
    },
    'examplegrp_name': {
        EN: 'group-name',
        RU: 'название-группы'
    },
    'examplegrp_desc': {
        EN: 'group-description',
        RU: 'описание-группы'
    }
}

_T = T(locale_dict=_locale)


examplegrp = app_commands.Group(
    name=_ls(
        'examplegrp_name',
        extras={
            DICT: _locale.get('examplegrp_name'),
            TYPE: CMD
        }
    ),
    description=_ls(
        'examplegrp_desc',
        extras={
            DICT: _locale.get('examplegrp_desc'),
            TYPE: CMD
        }
    )
)


@examplegrp.command(
    name=_ls(
        'bonk_name',
        extras={
            DICT: _locale.get('bonk_name'),
            TYPE: CMD
        }
    ),
    description=_ls(
        'bonk_desc',
        extras={
            DICT: _locale.get('bonk_desc'),
            TYPE: CMD
        }
    )
)
async def bonk(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    _T.set_locale(locale=interaction.locale)
    _T.set_string(string=_ls("bonk_usr", extras={FORMAT: {'_': 'Tangakk'}}))
    await interaction.followup.send(_T.stranslate())
