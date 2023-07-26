import discord
import re
import random
import collections as coll

# from environment import Facts
from discord import app_commands
from translator.main import T
from discord.app_commands import locale_str as _ls
from environment.variable import *
from environment.facts import Facts
from commands.database.dbcontrol import DB


_F = Facts()


def capitalize_words(string):
    return str.join(' ', [word.capitalize() for word in string.split(' ')])


FACT_CMD_NAME = "fact_cmd_name"
FACT_CMD_DESC = "fact_cmd_desc"
NO_FACTS_IN_DB = "no_facts_in_db"

CULTS_CMD_NAME = "cults_cmd_name"
CULTS_CMD_DESC = "cults_cmd_desc"
TOP_CULTS = "top_cults"
MEMBERS_IN_CULT = "members_in_cult"
NO_CULTS = "no_cults"
BY_WEALTH = "by_wealth"
BY_MEMBERS = "by_members"
SORT = "sort"
DICEARGS = "diceargs"
ROLLDICE_CMD_NAME = "rolldice_cmd_name"
ROLLDICE_CMD_DESC = "rolldice_cmd_desc"
TOO_MANY_DICE = "too_many_dice"
NOTHING_TO_ROLL = "nothing_to_roll"

_locale = {
    FACT_CMD_NAME: {EN: "fun-fact",
                    RU: "забавный-факт"},
    FACT_CMD_DESC: {EN: "Learn a fun fact",
                    RU: "Узнать забавный факт"},
    NO_FACTS_IN_DB: {EN: "Sorry... I don't have any facts yet! :(",
                     RU: "Простите... У меня пока что нету фактов! :("},

    CULTS_CMD_NAME: {EN: "cults",
                     RU: "культы"},
    CULTS_CMD_DESC: {EN: "Show server cults",
                     RU: "Показать культы сервера"},
    TOP_CULTS: {EN: "Top cults",
                RU: "Топ культов"},
    MEMBERS_IN_CULT: {EN: "Members: {_} - Wealth: {_1}.",
                      RU: "Участников: {_} - Богатство: {_1}."},  #
    NO_CULTS: {EN: "Sorry, no cults on this server.",
               RU: "Извините, на этом сервере нет культов."},

    ROLLDICE_CMD_NAME: {EN: "roll-dice",
                        RU: "кинуть-игральные-кости"},
    ROLLDICE_CMD_DESC: {EN: "Randomizer",
                        RU: "Рандомайзер"},
    TOO_MANY_DICE: {EN: "Too many dice. Maximum is 10",
                    RU: "Слишком много игральных костей. Максимум - 10"},
    NOTHING_TO_ROLL: {EN: "Nothing to roll",
                      RU: "Нечего кидать"},  #
    SORT: {EN: "sort",
           RU: "сортировать"},
    BY_MEMBERS: {EN: "By members",
                 RU: "По участникам"},
    BY_WEALTH: {EN: "By wealth",
                RU: "По богатству"},
    DICEARGS: {EN: "dice",
               RU: "игральные-кубики"}
}

_T = T(locale_dict=_locale)


# _F = Facts()


@app_commands.command(
    name=namedesc(FACT_CMD_NAME, _locale),
    description=namedesc(FACT_CMD_DESC, _locale),
    extras={IS_BROKEN: False}
)
async def facts(interaction: discord.Interaction):
    await interaction.response.defer()
    _T.set_language(interaction.locale)
    if fact := await _F.read_facts(guild=interaction.guild, lang=_T.get_lang(interaction.locale.value)):
        await interaction.followup.send(fact)
    else:
        await interaction.followup.send(_T.stranslate(_ls(NO_FACTS_IN_DB)))


@app_commands.command(
    name=namedesc(CULTS_CMD_NAME, _locale),
    description=namedesc(CULTS_CMD_DESC, _locale)
)
@app_commands.rename(sort_by=namedesc(SORT, _locale))
@app_commands.choices(sort_by=[
    app_commands.Choice(name=namedesc(BY_MEMBERS, _locale), value=0),
    app_commands.Choice(name=namedesc(BY_WEALTH, _locale), value=1)])
async def cults(interaction: discord.Interaction, sort_by: app_commands.Choice[int] = 0):
    await interaction.response.defer()
    _T.set_language(interaction.locale)
    clist = {}
    cmoney = {}
    for member in interaction.guild.members:
        while LOCK.locked():
            await asyncio.sleep(0.5)
        async with LOCK:
            DB.connect()
            if member.nick:
                s = str.find(member.nick, '[') + 1
                e = str.find(member.nick, ']')
                if s != -1 and e != -1:
                    dat = DB.execute("SELECT wealth FROM users WHERE id = ?;",
                                     (member.id,))
                    if not dat:
                        dat = 0
                    else:
                        dat = dat[0]
                    if cmoney.get(str.lower(member.nick[s:e])):
                        cmoney[str.lower(member.nick[s:e])] += dat
                    else:
                        cmoney[str.lower(member.nick[s:e])] = dat
                    if clist.get(str.lower(member.nick[s:e])):
                        clist[str.lower(member.nick[s:e])] += 1
                    else:
                        clist[str.lower(member.nick[s:e])] = 1
            else:
                s = str.find(member.name, '[') + 1
                e = str.find(member.name, ']')
                if s != -1 and e != -1:
                    dat = DB.execute("SELECT wealth FROM users WHERE id = ?;",
                                     (member.id,))
                    if not dat:
                        dat = 0
                    else:
                        dat = dat[0]
                    if cmoney.get(str.lower(member.nick[s:e])):
                        cmoney[str.lower(member.nick[s:e])] += dat
                    else:
                        cmoney[str.lower(member.nick[s:e])] = dat
                    if clist.get(str.lower(member.nick[s:e])):
                        clist[str.lower(member.nick[s:e])] += 1
                    else:
                        clist[str.lower(member.nick[s:e])] = 1
            DB.disconnect()
    if sort_by == 1:
        cults_tuple = dict(coll.Counter(cmoney).most_common(10))
    else:
        cults_tuple = dict(coll.Counter(clist).most_common(10))
    if len(cults_tuple) > 0:
        embed = discord.Embed(
            title=_T.stranslate(
                _ls(
                    TOP_CULTS,
                    extras={
                        FORMAT: {"_": len(cults_tuple)}
                    }
                )
            )
        )
        for i, cult_name in enumerate(cults_tuple.keys()):
            if clist.get(cult_name) > 1:
                embed.add_field(
                    name=f"{i + 1}) {capitalize_words(cult_name)}",
                    value=_T.stranslate(
                        _ls(
                            MEMBERS_IN_CULT,
                            extras={
                                FORMAT: {"_": clist.get(cult_name),
                                         "_1": cmoney.get(cult_name)}
                            }
                        )
                    ),
                    inline=False)
        if len(embed.fields) > 1:
            await interaction.followup.send(embed=embed)
            return
    await interaction.followup.send(_T.stranslate(_ls(NO_CULTS)))


@app_commands.command(
    name=namedesc(ROLLDICE_CMD_NAME, _locale),
    description=namedesc(ROLLDICE_CMD_DESC, _locale)
)
@app_commands.rename(dice_args=namedesc(DICEARGS, _locale))
async def rolldice(interaction: discord.Interaction, *, dice_args: str):
    await interaction.response.defer()
    _T.set_language(interaction.locale)
    results = {}
    dices = re.findall(r'(\d*)([dк])(\d+)([+-\\*/]?)(\d+)?', dice_args)
    if len(dices) > 10:
        await interaction.followup.send(_T.stranslate(_ls(TOO_MANY_DICE)))
        return
    for dice in dices:
        count, spliter, value, op, num = dice
        result = []
        if count != '':
            if not (0 < int(count) < 11) or not (1 < int(value) < 101):
                continue
            for i in range(1, int(count) + 1):
                res = random.randint(1, int(value))
                if num:
                    if op == "+":
                        res += int(num)
                    elif op == "-":
                        res -= int(num)
                    elif op == "*":
                        res *= int(num)
                    elif op == "/":
                        res = res/int(num)
                result.append(res)
        else:
            if not (1 < int(value) < 101):
                continue
            res = random.randint(1, int(value))
            if num:
                if op == "+":
                    res += int(num)
                elif op == "-":
                    res -= int(num)
                elif op == "*":
                    res *= int(num)
                elif op == "/":
                    if int(num)>0:
                        res = res / int(num)
                    else:
                        res = 0
            result.append(res)
        results[f'{count}{spliter}{value}{op}{num}'] = result
    tosay = ''
    gsum = 0
    for r in results.items():
        if len(r[1]) > 1:
            tosay += f'''{r[0]}: {' + '.join(map(str, r[1]))} = {sum(r[1])}
'''
            gsum += sum(r[1])
        else:
            tosay += f'''{r[0]}: {sum(r[1])}
'''
            gsum += sum(r[1])
    if len(results.items()) > 1:
        tosay += f'{gsum}'
    if tosay == '':
        await interaction.followup.send(_T.stranslate(_ls(NOTHING_TO_ROLL)))
        return
    await interaction.followup.send(tosay[:2000])
