import discord
from discord import app_commands
from discord.app_commands import locale_str as _ls

from translator.__init__ import T
from environment.variable import *

from .bf_cmd import brainfuck
from .ttt_cmd import tictactoe
from .gol_cmd import gameoflife

FUN_GROUP_NAME = "fungrp"
FUN_GROUP_DESC = "fungrp_d"

_locale = {FUN_GROUP_NAME: {EN: "game",
                            RU: "игра"},
           FUN_GROUP_DESC: {EN: "Funny commands",
                            RU: "Веселые команды"}
           }

_T = T(locale_dict=_locale)

fungrp = create_group(FUN_GROUP_NAME, FUN_GROUP_DESC, _locale)

fungrp.add_command(brainfuck)
fungrp.add_command(tictactoe)
fungrp.add_command(gameoflife)
