from commands.admin import admingrp
from .fun import fungrp
from .regular import facts, cults, rolldice, facts_ignore, facts_count
from .wealth import wealthgrp, wealthopagrp
from .shop import shopgrp


def declare_commands(bot):
    commands_to_declare = []
    if bot.sys_var == 0:
        commands_to_declare = [admingrp, fungrp, facts, cults, rolldice, facts_ignore, facts_count]  # wealthgrp, wealthopagrp
    elif bot.sys_var == 1:
        commands_to_declare = [cults, rolldice, facts_ignore, facts_count]
    for i in commands_to_declare:
        bot.tree.add_command(i, guilds=bot.guilds)
