from discord.ext.commands import when_mentioned_or
from discord import Intents


def CONFIG(): return


CONFIG.CMD_PREFIX = when_mentioned_or(">_", "!")
CONFIG.INTENTS = Intents.all()

default_cfg_data = {
    "cfg_data": {},
    "shop_data": {}
}
