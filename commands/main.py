from .test.main import test_grp
from .enjoy.main import enjoy_grp


def declare_cmds(bot):
    bot.tree.add_command(test_grp)
    bot.tree.add_command(enjoy_grp)

    # Help(BOT)
    # Test(BOT)
    # FunGroup(BOT)
    # Other(BOT)
    # Nickblue_cmds(BOT)
