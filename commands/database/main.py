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
WEALTH_GRP_DESK = "wgrpd"
BALANCE_NAME = "wbalancen"
BALANCE_DESC = "wbalanced"

_locale = {
    _: {EN: "",
        RU: ""},

    GETBALANCE: {EN: "You have {_} lots.",
                 RU: "У тебя есть {_} лот."},

    WEALTH_GRP_NAME: {EN: "wallet",
                      RU: "кошелек"},
    WEALTH_GRP_DESK: {EN: "You control your money",
                      RU: "Ты контролируешь свои деньги"},
    BALANCE_NAME: {EN: "balance",
                   RU: "баланс"},
    BALANCE_DESC: {EN: "Get info about your savings",
                   RU: "Смотреть на сколько у вас не хватает денег"}
}

_T = T(locale_dict=_locale)

wealthgrp = create_group(WEALTH_GRP_NAME, WEALTH_GRP_DESK, _locale)


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
        data = DB.get_user_info(interaction.user.id, interaction.user.name, interaction.locale)
        DB.disconnect()
        _T.set_string(
            string=_ls(
                GETBALANCE,
                extras={
                    FORMAT: {
                        "_": _T.stranslate(st=_ls(data.get("wealth")))
                    }
                }
            )
        )
        await interaction.followup.send(_T.stranslate())

