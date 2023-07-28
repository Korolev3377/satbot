import discord
import sqlite3
import asyncio

from discord import app_commands
from discord.app_commands import locale_str as _ls
from discord.app_commands import Choice
from .dbcontrol import DB

from translator.main import T
from environment.variable import *

_locale = {
    GETBALANCE: {EN: f"You have {{lots}} {WEALTH_NAME.get('en')[1]}.",
                 RU: f"У тебя есть {{lots}} {WEALTH_NAME.get('kto_chto')[0]}(а/ов)."},
    TRANSFER_NAME: {EN: "trasfer",
                    RU: "перевод"},
    TRANSFER_DESC: {EN: f"Transfer your {WEALTH_NAME.get('en')[1]} to outher user",
                    RU: f"Дать {WEALTH_NAME.get('kto_chto')[1]} другому пользователю."},
    WEALTH_GRP_NAME: {EN: "wallet",
                      RU: "кошелек"},
    WEALTH_GRP_DESC: {EN: "You control your money.",
                      RU: "Ты контролируешь свои деньги."},
    BALANCE_NAME: {EN: "balance",
                   RU: "баланс"},
    BALANCE_DESC: {EN: "Get info about your savings.",
                   RU: "Смотреть на сколько у вас не хватает денег."},
    USER_CREATED: {
        EN: f"You don't seem to be in my database. I will add you to it. Now you can check your balance, tranfer {WEALTH_NAME.get('en')[1]} and accept the transfer.",
        RU: f"Похоже, вас нету в моей базе данных. Я добавлю вас в нее. Теперь вы можете проверять свой баланс, отправлять и принимать {WEALTH_NAME.get('kto_chto')[1]}."},
    TRANSFFERED: {EN: f"You have transferred {{wealth}} {WEALTH_NAME.get('en')[1]} to the user \"{{user2}}\"",
                  RU: f"Вы перевели {{wealth}} {WEALTH_NAME.get('kto_chto')[0]}(а/ов) пользователю \"{{user2}}\"."},
    USER1_NOT_IN_DB: {EN: "Ouh nyo! You not in by database. Please execute \"/wallet balance\" command to fix it.",
                      RU: "Оу нет! Вас нету в моей базе данных. Выполните комманду \"/кошелек баланс\" что бы пофиксить это."},
    USER2_NOT_IN_DB: {
        EN: f"Ouh nyo! You are trying to trasfer {WEALTH_NAME.get('en')[1]} to someone who is not in my database",
        RU: f"Оу нет! Вы пытаетесь перевести {WEALTH_NAME.get('kto_chto')[1]} пользователю, которого нету в моей базе данных."},
    NOT_ENOUGH_MONEY: {
        EN: f"You are trying to transfer {{value}} {WEALTH_NAME.get('en')[1]}, but you only have {{wealth}} {WEALTH_NAME.get('en')[1]}.",
        RU: f"Вы пытаетесь прыгнуть выше головы! Невозможно перевести {{value}} {WEALTH_NAME.get('kto_chto')[1]}, когда у вас всего {{wealth}} {WEALTH_NAME.get('kto_chto')[0]}(а/ов)."},
    VALUE_ERROR: {EN: "An error in the value of the trasfer amouth.",
                  RU: "Ошибка в значении суммы перевода."},
    INT_ERROR: {EN: "An error in the value of the target user.",
                RU: "Ошибка в значении цели перевода."},
    TRANSFER_ERROR: {EN: "Korolev nakodil govna.",
                     RU: "Korolev накодил говна."},
    VALUE: {EN: "amouth",
            RU: "сколько"},
    TARGET: {EN: "target",
             RU: "кому"},
    BALANCE_CHANGED: {EN: f"Your balance has changed!\n{{old_value}} >>> {{new_value}} {WEALTH_NAME.get('en')[1]}.",
                      RU: f"Ваш баланс изменился!\n{{old_value}} >>> {{new_value}} {WEALTH_NAME.get('kto_chto')[0]}(а/ов)."},
    BALANCE_CHANGED + "0": {
        EN: f"Your balance has changed!\n{{old_value}} >>> {{new_value}} {WEALTH_NAME.get('en')[1]}.\nYou have transferred {{value}} {WEALTH_NAME.get('en')[1]} to the user \"{{user}}\".",
        RU: f"Ваш баланс изменился!\n{{old_value}} >>> {{new_value}} {WEALTH_NAME.get('kto_chto')[0]}(а/ов).\nВы перевели {{value}} {WEALTH_NAME.get('kto_chto')[0]}(а/ов) пользователю \"{{user}}\"."},
    BALANCE_CHANGED + "1": {
        EN: f"Your balance has changed!\n{{old_value}} >>> {{new_value}} {WEALTH_NAME.get('en')[1]}.\nUser \"{{user}}\" has transferred {{value}} {WEALTH_NAME.get('en')[1]} to you.",
        RU: f"Ваш баланс изменился!\n{{old_value}} >>> {{new_value}} {WEALTH_NAME.get('kto_chto')[0]}(а/ов).\nПользователь \"{{user}}\" перевел вам {{value}} {WEALTH_NAME.get('kto_chto')[0]}(а/ов)."}
}

_T = T(locale_dict=_locale)

wealthgrp = create_group(WEALTH_GRP_NAME, WEALTH_GRP_DESC, _locale)


@wealthgrp.command(
    name=namedesc(BALANCE_NAME, _locale),
    description=namedesc(BALANCE_DESC, _locale)
)
async def balancecmd(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True, ephemeral=True)
    _T.set_language(language=interaction.locale)
    i = await DB.execute("SELECT id, wealth FROM users WHERE id = ?;",
                         (interaction.user.id,))
    if i:
        await DB.execute("UPDATE users SET name = ? WHERE id = ?;",
                         (interaction.user.name, i[0]))
        _T.set_string(string=_ls(
            GETBALANCE,
            extras={FORMAT: {
                "lots": _T.stranslate(st=_ls(i[1]))
            }}
        ))
    else:
        await DB.execute("INSERT INTO users (name, language) VALUES (?, ?);",
                         (interaction.user.name, interaction.locale))
        _T.set_string(
            string=_ls(
                USER_CREATED
            )
        )
    await interaction.followup.send(_T.stranslate())


@wealthgrp.command(
    name=namedesc(TRANSFER_NAME, _locale),
    description=namedesc(TRANSFER_DESC, _locale)
)
@app_commands.rename(user2_id=namedesc(TARGET, _locale), value=namedesc(VALUE, _locale))
async def trasfercmd(interaction: discord.Interaction, user2_id: str, value: app_commands.Range[int, 1, 1000]):
    await interaction.response.defer(thinking=True, ephemeral=True)
    _T.set_language(language=interaction.locale)  # Устанавливаем язык переводчика
    try:
        user2_id = int(user2_id)  # Проверка на int
    except:
        _T.set_string(
            string=_ls(
                INT_ERROR  # Вывод ошибки, если таргет не int
            )
        )
        await interaction.followup.send(_T.stranslate())
        return

    user1 = await DB.execute("SELECT name, wealth, language FROM users WHERE id = ?;",
                             (interaction.user.id,))  # Получение имени и количество лотов пользователя 1
    user2 = await DB.execute("SELECT name, wealth, language FROM users WHERE id = ?;",
                             (user2_id,))  # Получение имени и количество лотов пользователя 2
    if not user1:
        _T.set_string(
            string=_ls(
                USER1_NOT_IN_DB
            )
        )
    elif not user2:
        _T.set_string(
            string=_ls(
                USER2_NOT_IN_DB
            )
        )
    elif user1[1] - value >= 0 and value > 0:
        await DB.execute("UPDATE users SET wealth = ? WHERE id = ?;",
                         (user1[1] - value, interaction.user.id))
        await DB.execute("UPDATE users SET wealth = ? WHERE id = ?;",
                         (user2[1] + value, user2_id))
        _T.set_string(
            string=_ls(
                TRANSFFERED,
                extras={
                    FORMAT: {
                        WEALTH: value,
                        USER_2: user2[0]
                    }
                }
            )
        )
    elif value <= 0:
        _T.set_string(
            string=_ls(
                VALUE_ERROR
            )
        )
    else:
        _T.set_string(
            string=_ls(
                NOT_ENOUGH_MONEY,
                extras={
                    FORMAT: {
                        WEALTH: user1[1],
                        VALUE: value
                    }
                }
            )
        )
    await interaction.followup.send(_T.stranslate())

    await interaction.client.get_user(interaction.user.id).send(_T.stranslate(_ls(BALANCE_CHANGED + "0",
                                                                                  extras={
                                                                                      FORMAT: {
                                                                                          "old_value": user1[1],
                                                                                          "new_value": user1[1] - value,
                                                                                          "user": user2[0],
                                                                                          "value": value
                                                                                      }
                                                                                  }), user2[2]))
    await interaction.client.get_user(user2_id).send(_T.stranslate(_ls(BALANCE_CHANGED + "1",
                                                                       extras={
                                                                           FORMAT: {
                                                                               "old_value": user2[1],
                                                                               "new_value": user2[1] + value,
                                                                               "user": user1[0],
                                                                               "value": value
                                                                           }
                                                                       }), user2[2]))


@trasfercmd.autocomplete("user2_id")
async def db_users_autocomplite(interaction: discord.Interaction, current: str):
    data = await DB.execute("SELECT id, name FROM users WHERE is_visible = 1;", fetchone=False)
    ac = []
    for _ in data:
        if _[1].startswith(current):
            ac.append(app_commands.Choice(name=str(_[1]), value=str(_[0])))
    return ac[:25]
