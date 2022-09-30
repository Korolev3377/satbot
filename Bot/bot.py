import discord
from discord import Intents
from discord.ext import commands
from discord.app_commands import locale_str as _ls
import os
import re
import random

from Bot.misc import Env, Config
from Bot.cmds import register_all_commands
from Bot.translator import Translator

FACTS_EN = []
FACTS_RU = []

async def read_facts(guild):
    global FACTS_EN, FACTS_RU
    try:
        for channel in guild.channels:
            if channel.name == "nrc":
                message = await channel.fetch_message(channel.last_message_id)
                if message.attachments:
                    for attach in message.attachments:
                        await attach.save(str.lower(attach.filename))
                    with open('facts_en.txt', 'r', encoding='utf-8') as file:
                        FACTS_EN = str.split(file.read(), '\n')
                    os.remove('facts_en.txt')
                    with open('facts_ru.txt', 'r', encoding='utf-8') as file:
                        FACTS_RU = str.split(file.read(), '\n')
                    os.remove('facts_ru.txt')
                else:
                    await message.add_reaction('⚠️')
    except:
        print(f'Проблемы с чтеним фактов!')

def find_fact(msg):
    english = re.findall(r'\bfact(s)?\W*\b', msg)
    russian = re.findall(r'\bфакт(а|у|ом|е|ы|ов|ам|ами|ах|о)?\W*\b', msg)
    if english:
        return 'en'
    elif russian:
        return 'ru'
    else:
        return False

def start_bot():
    class Bot(commands.Bot):
        def __init__(self):
            super().__init__(command_prefix=Config.CMD_PREFIX,
                             help_command=None,
                             strip_after_prefix=True,
                             intents=Config.INTENTS)
            self.overload = 0.0

        async def setup_hook(self):
            self.tree.interaction_check = itr_check
            await self.tree.set_translator(Translator())
            await self.tree.sync()

    BOT = Bot()

    async def itr_check(interaction: discord.Interaction):
        if BOT.overload > 100:
            if await BOT.is_owner(interaction.user):
                await interaction.followup.send(T.soft_translate(string=BOT.tree.translator.soft_translate(_ls("fuck_u")), locale=interaction.locale))
            else:
                await interaction.followup.send(T.soft_translate(string=BOT.tree.translator.soft_translate(_ls("on_cd"), locale=interaction.locale)), ephemeral=True)

        if interaction.command.extras.get("disabled"):
            await interaction.response.send_message(BOT.tree.translator.soft_translate(_ls("cmd_disabled"), locale=interaction.locale), ephemeral=True)
            return False

        if not interaction.permissions.administrator and interaction.command.extras.get("admin_only"):
            if not await BOT.is_owner(interaction.user):
                await interaction.response.send_message(BOT.tree.translator.soft_translate(_ls("cmd_adminonly"), locale=interaction.locale), ephemeral=True)
                return False

        if not await BOT.is_owner(interaction.user) and interaction.command.extras.get("owner_only"):
            await interaction.response.send_message(BOT.tree.translator.soft_translate(_ls("cmd_owneronly"), locale=interaction.locale), ephemeral=True)
            return False
        BOT.overload += 0.1
        return True

    @BOT.event
    async def on_ready():
        print(f"Name: {BOT.user}\nID: {BOT.user.id}")
        if translate_not_found := BOT.tree.translator.translate_not_found:
            print(f"Translate not found for {translate_not_found}")

    @BOT.event
    async def on_message(message):
        if message.author == BOT.user or message.author.bot:
            return
        msg = message.content.lower()
        cho = re.findall(r'\b8915-7\b', msg)  # Костыли
        cho += re.findall(r'\b872406824765251594\b', msg)
        cho += re.findall(r'\bбарменбот(а|у|ом|е|ы|ов|ам|ами|ах|о)?\b', msg)
        cho += re.findall(r'\bбармен(а|у|ом|е|ы|ов|ам|ами|ах|о)?\b', msg)
        cho += re.findall(r'\bфактобот(а|у|ом|е|ы|ов|ам|ами|ах|о)?\b', msg)
        cho += re.findall(r'\bббот\b', msg)
        cho += re.findall(r'\bbbot\b', msg)
        cho += re.findall(r'\bbarmen\b', msg)
        cho += re.findall(r'\bbartender\b', msg)
        cho += re.findall(r'\bbartenderbot\b', msg)
        if lang := find_fact(msg):  # Пока-что вывод фактов такой. Потом нужно будет переделать
            await read_facts(message.guild)
            if lang == "en" and len(FACTS_EN) > 0:
                await message.channel.send(f'{random.choice(FACTS_EN)}')
            elif lang == "ru" and len(FACTS_RU) > 0:
                await message.channel.send(f'{random.choice(FACTS_RU)}')
        elif cho:
            try:
                await message.add_reaction(':89157:873334902005833778')
            except:
                await message.add_reaction(':af_pepe_tea: 1005139436134223882')

    """@BOT.event
    async def on_member_join(member: discord.Member):
        await member.guild.system_channel.send("{user} joined this Guild".format(user=member.mention))

    @BOT.event
    async def on_member_remove(member: discord.Member):
        await member.guild.system_channel.send("{user} left this Guild".format(user=member.mention))"""

    register_all_commands(BOT)
    BOT.run(Env.TOKEN)
