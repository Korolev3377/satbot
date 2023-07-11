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


FACT_NAME = "fact_name"
FACT_DESC = "facts_desc"
NO_FACTS = "no_facts"

CULTS_NAME = "cults_name"
CULTS_DESC = "cults_desc"
TOP_CULT = "top_cults"
CULT_INFO = "members_count"
NO_CULTS = "no_cults"

ROLLDICE_NAME = "rd_name"
ROLLDICE_DESC = "rd_desc"
TOO_MANY_DICES = "tmd"
ZERO_OUTPUT = "zo"

_locale = {
    FACT_NAME: {EN: "fun-fact",
                RU: "забавный-факт"},
    FACT_DESC: {EN: "Let me gave u funny fackt.",
                RU: "Дай мне дать тебе забавный факт."},
    NO_FACTS: {EN: "Sorry, no facts on this server",
               RU: "Сорри, нету фактов на этом сервере."},

    CULTS_NAME: {EN: "top-cults",
                 RU: "топ-культов"},
    CULTS_DESC: {EN: "Check most popular cults on this server.",
                 RU: "Проверить наиболее популярные культы на этом сервере."},
    TOP_CULT: {EN: "Top {_} cults",
               RU: "Топ {_} культов"},
    CULT_INFO: {EN: "Members: {_}. Wealth: {_1}.",
                RU: "Участников: {_}. Богатство: {_1}."},
    NO_CULTS: {EN: "Sorry, no cults on this server.",
               RU: "Извините, на этом сервере нет культов."},

    ROLLDICE_NAME: {EN: "roll-dice",
                    RU: "кинуть-кубики"},
    ROLLDICE_DESC: {EN: "Trhow some dises.",
                    RU: "Книуть немного кубеков."},
    TOO_MANY_DICES: {EN: "Too many dices. Maxium == 10.",
                     RU: "Слишком много кубиков. Максимум - 10."},
    ZERO_OUTPUT: {EN: "No info for output. Check input.",
                  RU: "Нет информации для вывода. Проверте ввод."},
    "sort_by": {EN: "sort",
                RU: "сортировать"},
    "by_members": {EN: "By members",
                   RU: "По участникам"},
    "by_wealth": {EN: "By wealth",
                  RU: "По богатству"}
}

_T = T(locale_dict=_locale)


# _F = Facts()


@app_commands.command(
    name=namedesc(FACT_NAME, _locale),
    description=namedesc(FACT_DESC, _locale),
    extras={IS_BROKEN: False}
)
async def facts(interaction: discord.Interaction):
    await interaction.response.defer()
    _T.set_language(interaction.locale)
    if fact := await _F.read_facts(guild=interaction.guild, lang=_T.get_lang(interaction.locale.value)):
        await interaction.followup.send(fact)
    else:
        await interaction.followup.send(_T.stranslate(_ls(NO_FACTS)))


@app_commands.command(
    name=namedesc(CULTS_NAME, _locale),
    description=namedesc(CULTS_DESC, _locale)
)
@app_commands.rename(sort_by=namedesc("sort_by", _locale))
@app_commands.choices(sort_by=[
    app_commands.Choice(name=namedesc("by_members", _locale), value=0),
    app_commands.Choice(name=namedesc("by_wealth", _locale), value=1)])
async def cults(interaction: discord.Interaction, sort_by: app_commands.Choice[int] = 0):
    await interaction.response.defer()
    _T.set_language(interaction.locale)
    sort_by = sort_by.value
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
                    dat = DB.get_user_info(user_id=member.id, user_name=member.name,
                                           user_language=_T.get_lang(interaction.locale.value), create_usr=False)
                    if dat in ("usercreated", "nouser"):
                        dat = 0
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
                    dat = DB.get_user_info(user_id=member.id, user_name=member.name,
                                           user_language=_T.get_lang(interaction.locale.value), create_usr=False)
                    if dat in ("usercreated", "nouser"):
                        dat = 0
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
                    TOP_CULT,
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
                            CULT_INFO,
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
    name=namedesc(ROLLDICE_NAME, _locale),
    description=namedesc(ROLLDICE_DESC, _locale)
)
async def rolldice(interaction: discord.Interaction, *, dice_args: str):
    await interaction.response.defer()
    _T.set_language(interaction.locale)
    results = {}
    dices = re.findall(r'\d*[dк-]\d+', dice_args)
    if len(dices) > 10:
        await interaction.followup.send(_T.stranslate(_ls(TOO_MANY_DICES)))
        return
    for dice in dices:
        count, value = re.split(r'[dк-]', dice)
        result = []
        if count != '':
            if not (0 < int(count) < 11) or not (1 < int(value) < 101):
                continue
            for i in range(1, int(count) + 1):
                result.append(random.randint(1, int(value)))
        else:
            if not (1 < int(value) < 101):
                continue
            result.append(random.randint(1, int(value)))
        results[f'{dice}'] = result
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
        await interaction.followup.send(_T.stranslate(_ls(ZERO_OUTPUT)))
        return
    await interaction.followup.send(tosay)
