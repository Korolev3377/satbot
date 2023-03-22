import discord
import re
import random
import collections as coll
import os

from Bot.misc import Facts
from discord.app_commands import locale_str as _ls
from Bot.translator import Translator as T

locale = {"too_many_dices": {"en": "Too many dices. Maximum - 10",
                             "ru": "Слишком много игральных костей. Максимум - 10"},
          "noting_tosay": {"en": "Nothing to roll",
                           "ru": "Ничего не выпало"},
          "mem": {"en": "Members: {members_count}",
                  "ru": "Участников: {members_count}"},
          "top_c": {"en": "Top cults",
                    "ru": "Топ культов"},
          "no_facts": {"en": "Sorry. I don't have any facts yet! :(",
                       "ru": "Простите. У меня пока-что нету фактов! :("}}

_T = T(locale_dict=locale)
_F = Facts()

def capitalize_words(string):
    return str.join(' ', [word.capitalize() for word in string.split(' ')])

class Other:
    def __init__(self, BOT):
        @BOT.tree.command(name="cult_n", description="cult_d")
        async def cmd(interaction: discord.Interaction):
            await interaction.response.defer()
            lang = interaction.locale
            clist = []
            for member in interaction.guild.members:
                if member.nick:
                    s = str.find(member.nick, '[') + 1
                    e = str.find(member.nick, ']')
                    if s != -1 and e != -1:
                        clist.append(str.lower(member.nick[s:e]))
                else:
                    s = str.find(member.name, '[') + 1
                    e = str.find(member.name, ']')
                    if s != -1 and e != -1:
                        clist.append(str.lower(member.name[s:e]))
            cults_tuple = list(dict(coll.Counter(clist).most_common(10)).items())
            if len(cults_tuple) > 0:
                embed = discord.Embed(
                    title=_T.soft_translate(_ls("top_c"), locale=lang))
                for i, cult in enumerate(cults_tuple):
                    cult_name, members_count = cult
                    if members_count > 1:
                        embed.add_field(name=f"{i + 1}) {capitalize_words(cult_name)}",
                                        value=_T.soft_translate(_ls("mem",
                                                                    extras={
                                                                        "format": {"members_count": members_count}}),
                                                                locale=lang),
                                        inline=False)
                await interaction.followup.send(embed=embed)

        @BOT.tree.command(name="dice_n", description="dice_d")
        async def cmd(interaction: discord.Interaction, *, dice_args: str):
            await interaction.response.defer()
            lang = interaction.locale
            results = {}
            dices = re.findall(r'\d*[dк-]\d+', dice_args)
            if len(dices) > 10:
                await interaction.followup.send(_T.soft_translate(_ls("too_many_dices"), locale=lang))
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
                await interaction.followup.send(_T.soft_translate(_ls("noting_tosay"), locale=lang))
                return
            await interaction.followup.send(tosay)

        @BOT.tree.command(name="fact_n", description="fact_d")
        async def cmd(interaction: discord.Interaction):
            await interaction.response.defer()
            if fact := await _F.read_facts(guild=interaction.guild, lang=lang):
                await interaction.followup.send(fact)
            else:
                await interaction.followup.send(_T.soft_translate(_ls("no_facts"), locale=interaction.locale))

