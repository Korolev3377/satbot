import asyncio

import discord.ui
from discord import app_commands
from discord.app_commands import locale_str as _ls

IS_SYSTEM = "system"
USER_LOAD = "overload"
IS_USER_OVERLOADED = "overloaded"

FORMAT = "format"
EXTRAS = "extras"
TYPE = "type"
CMD = "cmd"
DICT = "dict"
USAGE = "usage"

EN = "en"
RU = "ru"
UK = "uk"

IS_DISABLED = "disabled"
IS_BROKEN = "broken"
IS_ADMIN_ONLY = "admin_only"
IS_OWNER_ONLY = "owner_only"

ID = "id"
NAME = "name"
WEALTH = "wealth"
SCORE = "score"
LANGUAGE = "language"
IS_VISIBLE = "is_visible"

ADD = "add"
SET = "set"
TRANSFER = "move"

# Замочег для базы данных.
LOCK = asyncio.Lock()


def create_group(group_name, group_desc, locale_dict):
    return app_commands.Group(
        name=_ls(
            group_name,
            extras={
                DICT: locale_dict.get(group_name),
                TYPE: CMD
            }
        ),
        description=_ls(
            group_desc,
            extras={
                DICT: locale_dict.get(group_desc),
                TYPE: CMD
            }
        )
    )


def namedesc(name_desc, locale_dict):
    return _ls(
        name_desc,
        extras={
            DICT: locale_dict.get(name_desc),
            TYPE: CMD
        }
    )
