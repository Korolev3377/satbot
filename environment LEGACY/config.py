from discord.ext.commands import when_mentioned_or
from discord import Intents


def CONFIG(): return  # Костыль, но да пофиг.


CONFIG.CMD_PREFIX = when_mentioned_or(">_", "!")
CONFIG.INTENTS = Intents.all()

CONFIG.DEFAULT_CFG = {
  "wealth_name": {
    "en": "coins",
    "ru": "монета"
  },
  "commands_to_declare": {
    # Regular Commands
    "facts": False,
    "facts_ignore": False,
    "facts_count": False,
    "cults": False,
    "rolldice": False,
    # Fun Commands Group
    "fungrp": False,
    # Wealth Commands
    "wealthgrp": False,
    "wealthopagrp": False
  },
  "fact_word_react": False,
  "server_member_join_leave": {
    "enable": False,
    "on_join": "{user_name} {user_mention} {user_id} :inbox_tray:",
    "on_leave": "{user_name} {user_mention} {user_id} :outbox_tray:",
    "channel_id": ""
  }
}
