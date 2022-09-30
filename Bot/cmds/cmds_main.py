from Bot.cmds.help import Help
from Bot.cmds.test import Test
from Bot.cmds.fun import FunGroup
from Bot.cmds.other import Other

def register_all_commands(BOT):
    Help(BOT)
    Test(BOT)
    FunGroup(BOT)
    Other(BOT)
