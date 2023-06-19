import discord
import sqlite3
import asyncio

from discord import app_commands
from discord.app_commands import locale_str as _ls
from discord.app_commands import Choice
from .dbcontrol import DB

from translator.main import T
from environment.variable import *

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
    WEALTH_GRP_DESC: {EN: "You control your money.",
                      RU: "Ты контролируешь свои деньги."},
    BALANCE_NAME: {EN: "balance",
                   RU: "баланс"},
    BALANCE_DESC: {EN: "Get info about your savings.",
                   RU: "Смотреть на сколько у вас не хватает денег."},
    USER_CREATED: {
        EN: "You don't seem to be in my database. I will add you to it. Now you can check your balance, tranfer lots and accept the transfer.",
        RU: "Похоже, вас нету в моей базе данныз. Я добавлю вас в нее. Теперь вы можете проверять свой баланс, отправлять и принимать лоты."},
    TRANSFFERED: {EN: "You transferred {wealth} lots to a user \"{user2}\"",
                  RU: "Вы перевели пользователю \"{user2}\" {wealth} лот."},
    USER1_NOT_IN_DB: {EN: "Ouh nyo! You not in by database. Please execute \"/wallet balance\" command to fix it.",
                      RU: "Оу нет! Вас нету в моей базе данных. Выполните комманду \"/кошелек баланс\" что бы пофиксить это."},
    USER2_NOT_IN_DB: {EN: "Ouh nyo! You are trying to trasfer lots tp someone who is not in my database",
                      RU: "Оу нет! Вы пытаетесь перевести лоты пользователю, которого нету в моей базе данных."},
    NOT_ENOUGH_MONEY: {EN: "You are trying to transfer {value} lots, but you only have {wealth} lots.",
                       RU: "Вы пытаетесь прыгнуть выше головы! Вы пытаетесь перевести {value} лот, когда у вас всего {wealth} лот."},
    VALUE_ERROR: {EN: "An error in the value of the trasfer amouth.",
                  RU: "Ошибка в значении суммы перевода."},
    INT_ERROR: {EN: "An error in the value of the target user.",
                RU: "Ошибка в значении цели перевода."},
    TRANSFER_ERROR: {EN: "Korolev nakodil govna.",
                     RU: "Korolev накодил говна."},
    VALUE: {EN: "amouth",
            RU: "сколько"},
    TARGET: {EN: "target",
             RU: "кому"}
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
        data = DB.get_user_info(user_id=interaction.user.id, user_name=interaction.user.name,
                                user_language=interaction.locale)
        DB.disconnect()
        if data == USER_CREATED:
            _T.set_string(
                string=_ls(
                    USER_CREATED
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
        await DB.reload(interaction.client)
        await interaction.followup.send(_T.stranslate())


@wealthgrp.command(
    name=namedesc(TRANSFER_NAME, _locale),
    description=namedesc(TRANSFER_DESC, _locale)
)
@app_commands.rename(target_user="кому", value="сколько")
@app_commands.choices(target_user=DB.users)
async def trasfercmd(interaction: discord.Interaction, target_user: Choice[str], value: app_commands.Range[int, 1, 1000]):
    await interaction.response.defer(thinking=True)
    _T.set_locale(locale=interaction.locale)
    while LOCK.locked():
        await asyncio.sleep(1)
    async with LOCK:
        try:
            target_userid = int(target_user.value)
        except:
            _T.set_string(
                string=_ls(
                    INT_ERROR
                )
            )
            await interaction.followup.send(_T.stranslate())
            return
        DB.connect()
        status, data1, data2 = DB.ch_user_money(users=[interaction.user.id, target_userid], mode=TRANSFER, value=value)
        DB.disconnect()
        if status == TRANSFFERED and data1 and data2:
            _T.set_string(
                string=_ls(
                    TRANSFFERED,
                    extras={
                        FORMAT: {
                            WEALTH: value,
                            USER_2: data2.get(NAME)
                        }
                    }
                )
            )
        elif status == USER1_NOT_IN_DB:
            _T.set_string(
                string=_ls(
                    USER1_NOT_IN_DB
                )
            )
        elif status == USER2_NOT_IN_DB:
            _T.set_string(
                string=_ls(
                    USER2_NOT_IN_DB
                )
            )
        elif status == NOT_ENOUGH_MONEY:
            _T.set_string(
                string=_ls(
                    NOT_ENOUGH_MONEY,
                    extras={
                        FORMAT: {
                            WEALTH: data1.get(WEALTH),
                            VALUE: value
                        }
                    }
                )
            )
        elif status == VALUE_ERROR:
            _T.set_string(
                string=_ls(
                    VALUE_ERROR
                )
            )
        else:
            _T.set_string(
                string=_ls(
                    TRANSFER_ERROR
                )
            )
        await interaction.followup.send(_T.stranslate())
