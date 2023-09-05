from commands.admin import admingrp
from .fun import fungrp
from .regular import facts, cults, rolldice
from .wealth import wealthgrp, wealthopagrp
from .shop import shopgrp

commands_to_declare = [facts, cults, rolldice, fungrp, admingrp, wealthgrp ,wealthopagrp]


def declare_commands(bot):
    for i in commands_to_declare:
        bot.tree.add_command(i, guilds=bot.guilds)
