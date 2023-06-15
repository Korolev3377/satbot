import discord
import sqlite3
import asyncio

from discord import app_commands
from discord.app_commands import locale_str as _ls
from .dbcontrol import DB

from translator.main import T
from environment.variable import *

_ = ""
GETBALANCE = "getbalance"
WEALTH_GRP_NAME = "wgrpn"
WEALTH_GRP_DESC = "wgrpd"
TRANSFER_NAME = "tfn"
TRANSFER_DESC = "tfd"
BALANCE_NAME = "wbalancen"
BALANCE_DESC = "wbalanced"

_locale = {
    _: {EN: "",
        RU: ""},

    GETBALANCE: {EN: "You have {_} lots.",
                 RU: "У тебя есть {_} лот."},
    TRANSFER_NAME: {EN: "trasfer",
                    RU: "перевод"},
    TRANSFER_DESC: {EN: "Transfer your lots to outher user",
                    RU: "Дать шекелей другому пользователю."},
    WEALTH_GRP_NAME: {EN: "wallet",
                      RU: "кошелек"},
    WEALTH_GRP_DESC: {EN: "You control your money",
                      RU: "Ты контролируешь свои деньги"},
    BALANCE_NAME: {EN: "balance",
                   RU: "баланс"},
    BALANCE_DESC: {EN: "Get info about your savings",
                   RU: "Смотреть на сколько у вас не хватает денег"}
}

_T = T(locale_dict=_locale)

wealthgrp = create_group(WEALTH_GRP_NAME, WEALTH_GRP_DESC, _locale)


@wealthgrp.command(
    name=namedesc(BALANCE_NAME, _locale),
    description=namedesc(BALANCE_DESC, _locale)
)
async def balancecmd(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    _T.set_locale(locale=interaction.locale)
    while LOCK.locked():
        await asyncio.sleep(1)
    async with LOCK:
        DB.connect()
        data = DB.get_user_info(user_id=interaction.user.id, user_name=interaction.user.name, user_language=interaction.locale)
        DB.disconnect()
        if data == "usercreated":
            _T.set_string(
                string=_ls(
                    "usercreated"
                )
            )
        else:
            _T.set_string(
                string=_ls(
                    GETBALANCE,
                    extras={
                        FORMAT: {
                            "_": _T.stranslate(st=_ls(data))
                        }
                    }
                )
            )
        await interaction.followup.send(_T.stranslate())


@wealthgrp.command(
    name=namedesc(TRANSFER_NAME, _locale),
    description=namedesc(TRANSFER_DESC, _locale)
)
async def trasfercmd(interaction: discord.Interaction,  value: int, target_userid: str):
    await interaction.response.defer(thinking=True)
    _T.set_locale(locale=interaction.locale)
    while LOCK.locked():
        await asyncio.sleep(1)
    async with LOCK:
        DB.connect()
        status, data1, data2 = DB.ch_user_money(users=[interaction.user.id, target_userid], mode=TRANSFER, value=value)
        DB.disconnect()
        if status == "tansfered" and data1 and data2:
            _T.set_string(
                string=_ls(
                    "tansfered",
                    extras={
                        FORMAT: {
                            "wealth": data1.get(WEALTH),
                            "user2": data2.get(NAME)
                        }
                    }
                )
            )
        elif status == "nouser1":
            _T.set_string(
                string=_ls(
                    "nouser1"
                )
            )
        elif status == "nouser2":
            _T.set_string(
                string=_ls(
                    "nouser2"
                )
            )
        elif status == "notenoughmoney":
            _T.set_string(
                string=_ls(
                    "notenoughmoney",
                    extras={
                        FORMAT: {
                            "wealth": data1.get(WEALTH),
                            "value": value
                        }
                    }
                )
            )
        elif status == "valueerror":
            _T.set_string(
                string=_ls(
                    "valueerror"
                )
            )
        else:
            _T.set_string(
                string=_ls(
                    "tansfererror"
                )
            )
        await interaction.followup.send(_T.stranslate())
