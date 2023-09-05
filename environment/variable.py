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
ON_COOLDOWN = "on_cooldown"
ERROR = "error"
TIME = "time"

ID = "id"
NAME = "name"
WEALTH = "wealth"
SCORE = "score"
LANGUAGE = "language"
IS_VISIBLE = "is_visible"

# Замочег для базы данных.
LOCK = asyncio.Lock()

WEALTH_NAME_EN = "hex"

WEALTH_NAME_RU = "хекс"


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


def sort_by(obj_dict, key="id", orig="id", func=sorted):
    rev_dict = {}
    for k, v in obj_dict.items():
        assert v.get(key) is not None
        rev_dict[v.get(key)] = v
    rev_dict = dict(func(rev_dict.items()))
    output = {}
    for k, v in rev_dict.items():
        assert v.get(orig) is not None
        output[v.get(orig)] = v
    return output


def ls(string, extras: dict = None):
    return _ls(string, extras={FORMAT: extras})


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

# FUN

FUN_GROUP_NAME = "fungrp"
FUN_GROUP_DESC = "fungrp_d"

# ECONOMIC

BALANCE_CHANGED = "balance_changed"
USER_2 = "user2"
USER = "user"
TARGET = "target"
VALUE = "value"
TRANSFER_ERROR = "te"
INT_ERROR = "ie"
VALUE_ERROR = "ve"
NOT_ENOUGH_MONEY = "nem"
USER2_NOT_IN_DB = "nu2"
USER1_NOT_IN_DB = "nu1"
TRANSFFERED = "tf"
USER_CREATED = "uc"
GETBALANCE = "gb"
WEALTH_GRP_NAME = "wgrpn"
WEALTH_GRP_DESC = "wgrpd"
WEALTH_OPA_GRP_NAME = "wgrpon"
WEALTH_OPA_GRP_DESC = "wgrpod"
TRANSFER_NAME = "tfn"
TRANSFER_DESC = "tfd"
TRANSFER_OPA_NAME = "tfon"
TRANSFER_OPA_DESC = "tfod"
BALANCE_NAME = "wbn"
BALANCE_DESC = "wbd"
BALANCE_OPA_NAME = "wbon"
BALANCE_OPA_DESC = "wbod"
GETBALANCEOPA = "gbo"
NO_USER_OPA = "nuo"

# SHOP

HEX = "hex"
FREE = "free"
COST = "cost"
ROLE = "role"
ROLES_INV_D = "inv_cmd_desc"
ROLES_INV = "inv_cmd"
BUY_ROLES_D = "shop_cmd_desc"
BUY_ROLES = "shop_cmd"
SHOP_GROUP_D = "shop_group_desc"
SHOP_GROUP = "shop_group"
WEALTH_T = "wt"

# DATA

ROLE_ID = "user_id"
