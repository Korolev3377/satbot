import discord
import sqlite3
import asyncio
import pymorphy2

from discord import app_commands
from discord.app_commands import locale_str as _ls
from discord.app_commands import Choice
from commands.database import DB

from translator.__init__ import T
from environment.variable import *

MORPH_RU = pymorphy2.MorphAnalyzer(lang="ru")

_locale = {
    GETBALANCE: {EN: "You have {value}.",
                 RU: "У тебя есть {value}."},
    TRANSFER_NAME: {EN: "trasfer",
                    RU: "перевод"},
    TRANSFER_DESC: {EN: f"Transfer your {WEALTH_NAME_EN} to outher user",
                    RU: f"Дать {WEALTH_NAME_RU} другому пользователю."},
    WEALTH_GRP_NAME: {EN: "wallet",
                      RU: "кошелек"},
    WEALTH_GRP_DESC: {EN: "You control your money.",
                      RU: "Ты контролируешь свои деньги."},
    BALANCE_NAME: {EN: "balance",
                   RU: "баланс"},
    BALANCE_DESC: {EN: "Get info about your savings.",
                   RU: "Смотреть на сколько у вас не хватает денег."},
    USER_CREATED: {
        EN: f"You don't seem to be in my database. I will add you to it. Now you can check your balance, tranfer {WEALTH_NAME_EN} and accept the transfer.",
        RU: f"Похоже, вас нету в моей базе данных. Я добавлю вас в нее. Теперь вы можете проверять свой баланс, отправлять и принимать {WEALTH_NAME_RU}."},
    TRANSFFERED: {EN: "You have transferred {wealth} to the user \"{user2}\"",
                  RU: "Вы перевели {wealth} пользователю \"{user2}\"."},
    USER1_NOT_IN_DB: {EN: "Ouh nyo! You not in by database. Please execute \"/wallet balance\" command to fix it.",
                      RU: "Оу нет! Вас нету в моей базе данных. Выполните комманду \"/кошелек баланс\" что бы пофиксить это."},
    USER2_NOT_IN_DB: {
        EN: f"Ouh nyo! You are trying to trasfer {WEALTH_NAME_EN} to someone who is not in my database",
        RU: f"Оу нет! Вы пытаетесь перевести {WEALTH_NAME_RU} пользователю, которого нету в моей базе данных."},
    NOT_ENOUGH_MONEY: {
        EN: "You are trying to transfer {value}, but you only have {wealth}.",
        RU: "Вы пытаетесь прыгнуть выше головы! Невозможно перевести {value}, когда у вас всего {wealth}."},
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
    WEALTH_T: {EN: WEALTH_NAME_EN,
               RU: WEALTH_NAME_RU},
    BALANCE_CHANGED: {EN: "Your balance has changed!\n{old_value} >>> {new_value}.",
                      RU: "Ваш баланс изменился!\n{old_value} >>> {new_value}."},
    BALANCE_CHANGED + "0": {
        EN: "Your balance has changed!\n{old_value} >>> {new_value}.\nYou have transferred {value} to the user \"{user}\".",
        RU: "Ваш баланс изменился!\n{old_value} >>> {new_value}.\nВы перевели {value} пользователю \"{user}\"."},
    BALANCE_CHANGED + "1": {
        EN: "Your balance has changed!\n{old_value} >>> {new_value}.\nUser \"{user}\" has transferred {value} to you.",
        RU: "Ваш баланс изменился!\n{old_value} >>> {new_value}.\nПользователь \"{user}\" перевел вам {value}."}
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
                VALUE: f"{i[1]} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T)))[0].make_agree_with_number(i[1]).word}"
            }}
        ))
    else:
        await DB.execute("INSERT INTO users (id, name, language) VALUES (?, ?, ?);",
                         (interaction.user.id, interaction.user.name, interaction.locale.value))
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
    r = 0
    string = TRANSFER_ERROR
    extras = None
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

    if interaction.user.id == user2_id:
        interaction.client.logger.debug(f"Пользователь {interaction.user.name} пробует перевести лоты себе самому.")

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
        await interaction.followup.send(_T.stranslate())
        return
    elif not user2:
        string = USER2_NOT_IN_DB
        r = 1
    elif user1[1] - value >= 0 and value > 0:
        await DB.execute("UPDATE users SET wealth = ? WHERE id = ?;",
                         (user1[1] - value, interaction.user.id))
        user2 = await DB.execute("SELECT name, wealth, language FROM users WHERE id = ?;",
                                 (user2_id,))
        await DB.execute("UPDATE users SET wealth = ? WHERE id = ?;",
                         (user2[1] + value, user2_id))

        string = TRANSFFERED,
        extras = {FORMAT: {
            WEALTH: f"{value} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T)))[0].make_agree_with_number(value).word}",
            USER_2: user2[0]}}

        await interaction.followup.send(_T.stranslate())
    elif value <= 0:
        _T.set_string(
            string=_ls(
                VALUE_ERROR
            )
        )
        await interaction.followup.send(_T.stranslate())
        return
    else:
        _T.set_string(
            string=_ls(
                NOT_ENOUGH_MONEY,
                extras={
                    FORMAT: {
                        WEALTH: f"{user1[1]} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T)))[0].make_agree_with_number(user1[1]).word}",
                        VALUE: f"{value} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T)))[0].make_agree_with_number(value).word}"
                    }
                }
            )
        )
        await interaction.followup.send(_T.stranslate())
        r = 1

    _T.set_string(
        string=_ls(
            string
        )
    )
    await interaction.followup.send(_T.stranslate())

    if r:
        return

    await interaction.client.get_user(interaction.user.id).send(_T.stranslate(_ls(BALANCE_CHANGED + "0",
                                                                                  extras={
                                                                                      FORMAT: {
                                                                                          "old_value": f"{user1[1]} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T), user1[2]))[0].make_agree_with_number(user1[1]).word}",
                                                                                          "new_value": f"{user1[1] - value} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T), user1[2]))[0].make_agree_with_number(user1[1] - value).word}",
                                                                                          "user": user2[0],
                                                                                          VALUE: f"{value} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T)))[0].make_agree_with_number(value).word}"
                                                                                      }
                                                                                  }), user1[2]))
    await interaction.client.get_user(user2_id).send(_T.stranslate(_ls(BALANCE_CHANGED + "1",
                                                                       extras={
                                                                           FORMAT: {
                                                                               "old_value": f"{user2[1]} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T), user2[2]))[0].make_agree_with_number(user2[1]).word}",
                                                                               "new_value": f"{user2[1] + value} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T)))[0].make_agree_with_number(user2[1] + value).word}",
                                                                               "user": user1[0],
                                                                               VALUE: f"{value} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T), user2[2]))[0].make_agree_with_number(value).word}"
                                                                           }
                                                                       }), user2[2]))


@trasfercmd.autocomplete("user2_id")
async def db_users_autocomplite(interaction: discord.Interaction, current: str):
    data = await DB.execute("SELECT id, name FROM users WHERE is_visible = 1;", fetchone=False)
    ac = []
    for _ in data:
        if current in _[1]:
            ac.append(app_commands.Choice(name=str(_[1]), value=str(_[0])))
    return ac[:25]
