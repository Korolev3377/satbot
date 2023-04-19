from .example.main import examplegrp


# from .test.main import test_grp
# from .enjoy.main import enjoy_grp


def declare_cmds(bot):
    bot.tree.add_command(examplegrp)
    # bot.tree.add_command(enjoy_grp)

    # Help(BOT)
    # Test(BOT)
    # FunGroup(BOT)
    # Other(BOT)
    # Nickblue_cmds(BOT)
