import discord
from discord import app_commands
from discord.app_commands import locale_str as _ls

from translator.main import T
from environment.variable import *

from .bf_cmd import bf_cmd
from .ttt_cmd import ttt_cmd
from .gol_cmd import gol_cmd

ENJOY_GROUP_NAME = "enjoygrp_name"
ENJOY_GROUP_DESC = "enjoygrp_desc"

_locale = {ENJOY_GROUP_NAME: {EN: "game",
                              RU: "игра"},
           ENJOY_GROUP_DESC: {EN: "Games commands groups.",
                              RU: "Группа комманд игр."}
           }

_T = T(locale_dict=_locale)

enjoy_grp = create_group(ENJOY_GROUP_NAME, ENJOY_GROUP_DESC, _locale)

enjoy_grp.add_command(bf_cmd)
enjoy_grp.add_command(ttt_cmd)
enjoy_grp.add_command(gol_cmd)
