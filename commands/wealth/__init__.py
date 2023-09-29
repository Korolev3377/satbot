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
    GETBALANCE: {EN: "You have {value}.", RU: "У тебя есть {value}."},
    GETBALANCEOPA: {EN: "User \"{user}\" have {value}.", RU: "У пользователя \"{user}\" есть {value}."},
    TRANSFER_NAME: {EN: "trasfer", RU: "перевод"}, TRANSFER_DESC: {
        EN: f"Transfer your {WEALTH_NAME_EN} to outher user", RU: f"Дать {WEALTH_NAME_RU} другому пользователю."},
    WEALTH_GRP_NAME: {EN: "wallet", RU: "кошелек"},
    WEALTH_GRP_DESC: {EN: "You control your money.", RU: "Ты контролируешь свои деньги."},
    WEALTH_OPA_GRP_NAME: {EN: "wealth-opa", RU: "кошелек-опа"},
    WEALTH_OPA_GRP_DESC: {EN: "You control not your money.", RU: "Ты контролируешь не свои деньги."},
    BALANCE_NAME: {EN: "balance", RU: "баланс"}, BALANCE_OPA_NAME: {EN: "check-user", RU: "проверить-пользоватея"},
    BALANCE_OPA_DESC: {EN: "Get info about not your savings.", RU: "Смотреть на сколько не у вас не хватает денег."},
    BALANCE_DESC: {EN: "Get info about your savings.", RU: "Смотреть на сколько у вас не хватает денег."},
    USER_CREATED: {
        EN: f"You don't seem to be in my database. I will add you to it. Now you can check your balance, tranfer {WEALTH_NAME_EN} and accept the transfer.",
        RU: f"Похоже, вас нету в моей базе данных. Я добавлю вас в нее. Теперь вы можете проверять свой баланс, отправлять и принимать {WEALTH_NAME_RU}."},
    TRANSFFERED: {
        EN: "You have transferred {wealth} to the user \"{user2}\"",
        RU: "Вы перевели {wealth} пользователю \"{user2}\"."},
    USER1_NOT_IN_DB: {
        EN: "Ouh nyo! You not in by database. Please execute \"/wallet balance\" command to fix it.",
        RU: "Оу нет! Вас нету в моей базе данных. Выполните комманду \"/кошелек баланс\" что бы пофиксить это."},
    USER2_NOT_IN_DB: {
        EN: f"Ouh nyo! You are trying to trasfer {WEALTH_NAME_EN} to someone who is not in my database",
        RU: f"Оу нет! Вы пытаетесь перевести {WEALTH_NAME_RU} пользователю, которого нету в моей базе данных."},
    NOT_ENOUGH_MONEY: {
        EN: "You are trying to transfer {value}, but you only have {wealth}.",
        RU: "Вы пытаетесь прыгнуть выше головы! Невозможно перевести {value}, когда у вас всего {wealth}."},
    VALUE_ERROR: {EN: "An error in the value of the trasfer amouth.", RU: "Ошибка в значении суммы перевода."},
    INT_ERROR: {EN: "An error in the value of the target user.", RU: "Ошибка в значении цели перевода."},
    TRANSFER_ERROR: {EN: "Korolev nakodil govna.", RU: "Korolev накодил говна."}, VALUE: {EN: "amouth", RU: "сколько"},
    TARGET: {EN: "target", RU: "кому"},
    USER: {EN: "user", RU: "пользователь"},
    WEALTH_T: {EN: WEALTH_NAME_EN, RU: WEALTH_NAME_RU},
    NO_USER_OPA: {EN: "User not in BD.",
                  RU: "Пользователя нет в базе данных."},
    BALANCE_CHANGED: {
        EN: "Your balance has changed!\n{old_value} >>> {new_value}.",
        RU: "Ваш баланс изменился!\n{old_value} >>> {new_value}."},
    BALANCE_CHANGED + "0": {
        EN: "Your balance has changed!\n{old_value} >>> {new_value}.\nYou have transferred {value} to the user \"{user}\".",
        RU: "Ваш баланс изменился!\n{old_value} >>> {new_value}.\nВы перевели {value} пользователю \"{user}\"."},
    BALANCE_CHANGED + "1": {
        EN: "Your balance has changed!\n{old_value} >>> {new_value}.\nUser \"{user}\" has transferred {value} to you.",
        RU: "Ваш баланс изменился!\n{old_value} >>> {new_value}.\nПользователь \"{user}\" перевел вам {value}."},
    USER_FROM: {
        EN: f"from-user",
        RU: f"от-пользователя"},
    USER_TO: {
        EN: f"to-user",
        RU: f"пользователю"},
    ALARM: {
        EN: f"alarm-user",
        RU: f"предупредить"},
    TEXT1: {
        EN: f"message-to-user-1",
        RU: f"сообщение-пользователю-1"},
    TEXT2: {
        EN: f"message-to-user-2",
        RU: f"сообщение-пользователю-2"},
    POV: {
        EN: "\n(From \"{user}\"'s point of view)",
        RU: "\n(С точки зрения \"{user}\")"},
    NOT_DELIVERED: {
        EN: "Message to \"{user}\" not delivered.",
        RU: "Сообщение пользователю \"{user}\" не доставлено."},
    TRANSFER_OPA_NAME: {
        EN: f"force-transfer",
        RU: f"принудительный-перевод"},
    TRANSFER_OPA_DESC: {
        EN: f"None desc",
        RU: f"Нет опис"},
    MSG_TO_USER: {EN: "message-to-user", RU: "сообщение-пользователю"},
    MSG: {EN: "\nMessage: ", RU: "\nСообщение: "}}

_T = T(locale_dict=_locale)

wealthgrp = create_group(WEALTH_GRP_NAME, WEALTH_GRP_DESC, _locale)


@wealthgrp.command(name=namedesc(BALANCE_NAME, _locale), description=namedesc(BALANCE_DESC, _locale))
async def balancecmd(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True, ephemeral=True)
    _T.set_language(language=interaction.locale)
    i = await DB.execute("SELECT id, wealth FROM users WHERE id = ?;", (interaction.user.id,))
    if i:
        await DB.execute("UPDATE users SET name = ? WHERE id = ?;", (interaction.user.name, i[0]))
        message = ls(
            GETBALANCE,
            {VALUE: f"{i[1]} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T)))[0].make_agree_with_number(i[1]).word}"})
    else:
        await DB.execute(
            "INSERT INTO users (id, name, language) VALUES (?, ?, ?);",
            (interaction.user.id, interaction.user.name, interaction.locale.value))
        message = ls(USER_CREATED)
    await interaction.followup.send(_T.stranslate(message))


@wealthgrp.command(name=namedesc(TRANSFER_NAME, _locale), description=namedesc(TRANSFER_DESC, _locale))
@app_commands.rename(user2_id=namedesc(TARGET, _locale), value=namedesc(VALUE, _locale), message=namedesc(MSG_TO_USER, _locale))
async def trasfercmd(interaction: discord.Interaction, user2_id: str, value: app_commands.Range[int, 1], message: str = None):
    await interaction.response.defer(thinking=True, ephemeral=True)

    _T.set_language(language=interaction.locale)  # Устанавливаем язык переводчика
    stdout = TRANSFER_ERROR  # Эта переменная часто меняется тут. Нужно быть внимательнее.
    success = False

    try:
        user2_id = int(user2_id)  # Проверка на int
    except:
        stdout = ls(INT_ERROR)

    if interaction.user.id == user2_id:
        interaction.client.logger.debug(f"Пользователь {interaction.user.name} пробует перевести лоты себе самому.")

    user1 = await DB.execute("SELECT name, wealth, language FROM users WHERE id = ?;", (interaction.user.id,))
    # Получение имени и количество лотов пользователя 1

    user2 = await DB.execute("SELECT name, wealth, language FROM users WHERE id = ?;", (user2_id,))
    # Получение имени и количество лотов пользователя 2

    if not user1:
        stdout = ls(USER1_NOT_IN_DB)
    elif not user2:
        stdout = ls(USER2_NOT_IN_DB)
    elif value <= 0:
        stdout = ls(VALUE_ERROR)
    elif user1[1] - value < 0:
        stdout = ls(
            NOT_ENOUGH_MONEY, {
                WEALTH: f"{user1[1]} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T)))[0].make_agree_with_number(user1[1]).word}",
                VALUE: f"{value} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T)))[0].make_agree_with_number(value).word}"})
    else:
        await DB.execute("UPDATE users SET wealth = ? WHERE id = ?;", (user1[1] - value, interaction.user.id))
        user2 = await DB.execute("SELECT name, wealth, language FROM users WHERE id = ?;", (user2_id,))
        await DB.execute("UPDATE users SET wealth = ? WHERE id = ?;", (user2[1] + value, user2_id))
        stdout = ls(
            TRANSFFERED, {
                WEALTH: f"{value} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T)))[0].make_agree_with_number(value).word}",
                USER_2: user2[0]})
        success = True

    await interaction.followup.send(_T.stranslate(stdout))

    if success:
        stdout = ls(
            BALANCE_CHANGED + "0", {
                "old_value": f"{user1[1]} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T), user1[2]))[0].make_agree_with_number(user1[1]).word}",
                "new_value": f"{user1[1] - value} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T), user1[2]))[0].make_agree_with_number(user1[1] - value).word}",
                USER: user2[0],
                VALUE: f"{value} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T), user2[2]))[0].make_agree_with_number(value).word}"})
        text_out = [_T.stranslate(stdout, user1[2])]
        if message:
            text_out.append(_T.stranslate(_ls(MSG)))
            text_out.append(message)
        try:
            await interaction.client.get_user(interaction.user.id).send("".join(text_out))
        except:
            await interaction.followup.send(_T.stranslate(ls(NOT_DELIVERED, {USER: user1[0]})), ephemeral=True)
        stdout = ls(
            BALANCE_CHANGED + "1", {
                "old_value": f"{user2[1]} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T), user2[2]))[0].make_agree_with_number(user2[1]).word}",
                "new_value": f"{user2[1] + value} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T), user2[2]))[0].make_agree_with_number(user2[1] + value).word}",
                USER: user1[0],
                VALUE: f"{value} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T), user2[2]))[0].make_agree_with_number(value).word}"})
        text_out = [_T.stranslate(stdout, user1[2])]
        if message:
            text_out.append(_T.stranslate(_ls(MSG)))
            text_out.append(message)
        try:
            await interaction.client.get_user(user2_id).send("".join(text_out))
        except:
            await interaction.followup.send(_T.stranslate(ls(NOT_DELIVERED, {USER: user2[0]})), ephemeral=True)


@trasfercmd.autocomplete("user2_id")
async def db_users_autocomplite(interaction: discord.Interaction, current: str):
    data = await DB.execute("SELECT id, name FROM users WHERE is_visible = 1;", fetchone=False)
    ac = []
    for _ in data:
        if current in _[1] and interaction.guild.get_member(int(_[0])):
            ac.append(app_commands.Choice(name=str(_[1]), value=str(_[0])))
    return ac[:25]


wealthopagrp = create_group(WEALTH_OPA_GRP_NAME, WEALTH_OPA_GRP_DESC, _locale)
wealthopagrp.default_permissions = discord.Permissions.none()


@app_commands.rename(user_id=namedesc(USER, _locale))
@wealthopagrp.command(name=namedesc(BALANCE_OPA_NAME, _locale), description=namedesc(BALANCE_OPA_DESC, _locale))
async def balanceopacmd(interaction: discord.Interaction, user_id: str, create: bool = False):
    await interaction.response.defer(thinking=True, ephemeral=True)
    _T.set_language(language=interaction.locale)
    i = await DB.execute("SELECT name, wealth FROM users WHERE id = ?;", (int(user_id),))
    if i:
        message = ls(
            GETBALANCE, {
                USER: i[0],
                VALUE: f"{i[1]} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T)))[0].make_agree_with_number(i[1]).word}"})
        await interaction.followup.send((_T.stranslate(message) + _T.stranslate(ls(POV, {USER: i[0]}))))
    else:
        message = ls(NO_USER_OPA)
        await interaction.followup.send((_T.stranslate(message)))


@balanceopacmd.autocomplete("user_id")
async def db_users_autocomplite(interaction: discord.Interaction, current: str):
    data = await DB.execute("SELECT id, name FROM users WHERE is_visible = 1;", fetchone=False)
    ac = []
    for _ in data:
        if current in _[1] and interaction.guild.get_member(int(_[0])):
            ac.append(app_commands.Choice(name=str(_[1]), value=str(_[0])))
    return ac[:25]


@wealthopagrp.command(name=namedesc(TRANSFER_OPA_NAME, _locale), description=namedesc(TRANSFER_OPA_DESC, _locale))
@app_commands.rename(user1_id=namedesc(USER_FROM, _locale), user2_id=namedesc(USER_TO, _locale), value=namedesc(VALUE, _locale),
                     alarm=namedesc(ALARM, _locale), text1=namedesc(TEXT1, _locale), text2=namedesc(TEXT2, _locale))
async def trasferopacmd(interaction: discord.Interaction, user1_id: str, user2_id: str,
                        value: app_commands.Range[int, 1], alarm: bool = False, text1: str = None, text2: str = None):
    await interaction.response.defer(thinking=True, ephemeral=True)

    _T.set_language(language=interaction.locale)  # Устанавливаем язык переводчика
    stdout = TRANSFER_ERROR  # Эта переменная часто меняется тут. Нужно быть внимательнее.
    success = False

    try:
        user1_id = int(user1_id)
        user2_id = int(user2_id)  # Проверка на int
    except:
        stdout = ls(INT_ERROR)

    user1 = await DB.execute("SELECT name, wealth, language FROM users WHERE id = ?;", (user1_id,))
    # Получение имени и количество лотов пользователя 1

    user2 = await DB.execute("SELECT name, wealth, language FROM users WHERE id = ?;", (user2_id,))
    # Получение имени и количество лотов пользователя 2

    if not user1:
        stdout = ls(USER1_NOT_IN_DB)
    elif not user2:
        stdout = ls(USER2_NOT_IN_DB)
    elif value <= 0:
        stdout = ls(VALUE_ERROR)
    elif user1[1] - value < 0:
        stdout = ls(
            NOT_ENOUGH_MONEY, {
                WEALTH: f"{user1[1]} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T)))[0].make_agree_with_number(user1[1]).word}",
                VALUE: f"{value} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T)))[0].make_agree_with_number(value).word}"})
    else:
        await DB.execute("UPDATE users SET wealth = ? WHERE id = ?;", (user1[1] - value, user1_id))
        user2 = await DB.execute("SELECT name, wealth, language FROM users WHERE id = ?;", (user2_id,))
        await DB.execute("UPDATE users SET wealth = ? WHERE id = ?;", (user2[1] + value, user2_id))
        stdout = ls(
            TRANSFFERED, {
                WEALTH: f"{value} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T)))[0].make_agree_with_number(value).word}",
                USER_2: user2[0]})
        success = True

    await interaction.followup.send(_T.stranslate(stdout) + _T.stranslate(ls(POV, {USER: user1[0]})))

    if success and alarm:
        stdout = ls(
            BALANCE_CHANGED, {
                "old_value": f"{user1[1]} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T), user1[2]))[0].make_agree_with_number(user1[1]).word}",
                "new_value": f"{user1[1] - value} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T), user1[2]))[0].make_agree_with_number(user1[1] - value).word}"})
        text_out = [_T.stranslate(stdout, user1[2])]
        if text1:
            text_out.append("\n")
            text_out.append(text1)
        try:
            await interaction.client.get_user(user1_id).send("".join(text_out))
        except:
            await interaction.followup.send(_T.stranslate(ls(NOT_DELIVERED, {USER: user1[0]})), ephemeral=True)
        stdout = ls(
            BALANCE_CHANGED, {
                "old_value": f"{user2[1]} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T), user2[2]))[0].make_agree_with_number(user2[1]).word}",
                "new_value": f"{user2[1] + value} {MORPH_RU.parse(_T.stranslate(_ls(WEALTH_T), user2[2]))[0].make_agree_with_number(user2[1] + value).word}"})
        text_out = [_T.stranslate(stdout, user2[2])]
        if text2:
            text_out.append("\n")
            text_out.append(text2)
        try:
            await interaction.client.get_user(user2_id).send("".join(text_out))
        except:
            await interaction.followup.send(_T.stranslate(ls(NOT_DELIVERED, {USER: user2[0]})), ephemeral=True)


@trasferopacmd.autocomplete("user1_id")
async def db_users_autocomplite(interaction: discord.Interaction, current: str):
    data = await DB.execute("SELECT id, name FROM users WHERE is_visible = 1;", fetchone=False)
    ac = []
    for _ in data:
        if current in _[1] and interaction.guild.get_member(int(_[0])):
            ac.append(app_commands.Choice(name=str(_[1]), value=str(_[0])))
    return ac[:25]


@trasferopacmd.autocomplete("user2_id")
async def db_users_autocomplite(interaction: discord.Interaction, current: str):
    data = await DB.execute("SELECT id, name FROM users WHERE is_visible = 1;", fetchone=False)
    ac = []
    for _ in data:
        if current in _[1] and interaction.guild.get_member(int(_[0])):
            ac.append(app_commands.Choice(name=str(_[1]), value=str(_[0])))
    return ac[:25]
