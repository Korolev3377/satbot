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
IS_DM_ALLOWED = "allow_dm"

ID = "id"
NAME = "name"
WEALTH = "wealth"
SCORE = "score"
LANGUAGE = "language"
IS_VISIBLE = "is_visible"

# Замочег для базы данных.
LOCK = asyncio.Lock()

WEALTH_NAME = {"en": ("hex", "hex"),
               "kto_chto": ("хекс", "хексы"),
               "kogo_chego": ("хекса", "хексов"),
               "komu_chemu": ("хексу", "хексами"),
               "kogo_chto": ("хекс", "хексы"),
               "kem_chem": ("хексом", "хексами"),
               "okom_ochom": ("хексе", "хексах")}


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


_ = "_"

# ADMINS

ADMIN_GRP_NAME = "admin_grp_name"
ADMIN_GRP_DESC = "admin_grp_desc"
BOTSAY_CMD_NAME = "botsay_cmd_name"
BOTSAY_CMD_DESC = "botsay_cmd_desc"
MSG = "msg"
CHNL = "chnl"
MODAL_TEXT_LABEL = "modal_text_label"
MODAL_TITLE = "modal_title"
DELETE = "delete"
EDIT = "edit"

# ECONOMIC


BALANCE_CHANGED = "balance_changed"
USER_2 = "user2"
TARGET = "target"
VALUE = "value"
TRANSFER_ERROR = "tansfererror"
INT_ERROR = "interror"
VALUE_ERROR = "valueerror"
NOT_ENOUGH_MONEY = "notenoughmoney"
USER2_NOT_IN_DB = "nouser2"
USER1_NOT_IN_DB = "nouser1"
TRANSFFERED = "tansfered"
USER_CREATED = "usercreated"
GETBALANCE = "getbalance"
WEALTH_GRP_NAME = "wgrpn"
WEALTH_GRP_DESC = "wgrpd"
TRANSFER_NAME = "tfn"
TRANSFER_DESC = "tfd"
BALANCE_NAME = "wbalancen"
BALANCE_DESC = "wbalanced"
