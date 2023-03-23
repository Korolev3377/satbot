from discord.ext.commands import when_mentioned_or
from discord import Intents
from abc import ABC


class Cfg(ABC):
    CMD_PREFIX = when_mentioned_or(">_", "!")
    INTENTS = Intents.all()
