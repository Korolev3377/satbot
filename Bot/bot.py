import discord
from discord import Intents
from discord.ext import commands
from discord.app_commands import locale_str as _ls
import os
import re
import random

from Bot.misc import Env, Config, Facts
from Bot.cmds import register_all_commands
from Bot.translator import Translator
from Bot.heart import Heart, Nickblue

def start_bot():
    class Bot(commands.Bot):
        def __init__(self):
            print('\nВход по токену бота!')
            super().__init__(command_prefix=Config.CMD_PREFIX,
                             help_command=None,
                             strip_after_prefix=True,
                             intents=Config.INTENTS)
            self.nickblue = Nickblue(self, 851871106373255168, 920357026209595392, 996418372071862372, 996418316006588516)
            self.overload = 0.0  # Это ограничитель спама комманд. ака КД
            self.heart = Heart(self)  # Это главный цикл бота. В нем идет пассивное уменьшение КД и проверка на то, когда нужно будет менять Синего ника.

        async def setup_hook(self):
            self.tree.interaction_check = itr_check
            await self.tree.set_translator(Translator())  # Установка переводчика описания и названия комманд для клиента
            await self.tree.sync()  # Синхронизация. Для обновления изменения комманд
            print('\nСоединение с сервером!')

    BOT = Bot()
    F = Facts()

    async def itr_check(interaction: discord.Interaction):  # Проверка на возможность выполнения комманды
        if BOT.overload > 100:  # Если бот в КД, то он не будет выполнять комманду
            await interaction.followup.send(T.soft_translate(string=BOT.tree.translator.soft_translate(_ls("on_cd", extras={"format": {"time_left": int(BOT.heart.time_to_cooldown() - 100)}}), locale=interaction.locale)), ephemeral=True)

        if interaction.command.extras.get("disabled"):  # Проверка на отключенную комманду
            await interaction.response.send_message(BOT.tree.translator.soft_translate(_ls("cmd_disabled"), locale=interaction.locale), ephemeral=True)
            return False

        if not interaction.permissions.administrator and interaction.command.extras.get("admin_only"):  # Проверка на администратора сервера
            if not await BOT.is_owner(interaction.user):
                await interaction.response.send_message(BOT.tree.translator.soft_translate(_ls("cmd_adminonly"), locale=interaction.locale), ephemeral=True)
                return False

        if not await BOT.is_owner(interaction.user) and interaction.command.extras.get("owner_only"):  # Проверка на владельца Бота
            await interaction.response.send_message(BOT.tree.translator.soft_translate(_ls("cmd_owneronly"), locale=interaction.locale), ephemeral=True)
            return False

        BOT.overload += 1  # Пассивное охлаждение убирает 1 перегрузку за 10 секунд (по умолчанию)
        return True

    @BOT.event
    async def on_ready():
        print('\nЗапуск бота...')
        print('Бот запущен!')
        print(f"Имя: {BOT.user}\nИД: {BOT.user.id}")
        if translate_not_found := BOT.tree.translator.translate_not_found:
            print(f"\nПеревод не найден: {translate_not_found}")
        print('\nЗапуск сердца...')
        await BOT.heart.heartbeat.start()

    @BOT.event
    async def on_message(message):
        if message.author == BOT.user or message.author.bot:
            return

        msg = message.content.lower()
        
        if lang := F.find_fact(msg=msg):
            if fact := await F.read_facts(guild=message.guild, lang=lang):
                await message.channel.send(fact)
        
        bot_mention = re.search(r"(\b8915-7\b|\b872406824765251594\b|\bбарменбот(а|у|ом|е|ы|ов|ам|ами|ах|о)?\b|\bбармен(а|у|ом|е|ы|ов|ам|ами|ах|о)?\b|\bфактобот(а|у|ом|е|ы|ов|ам|ами|ах|о)?\b|\bббот\b|\bbbot\b|\bbarmen\b|\bbartender\b|\bbartenderbot\b)", msg)
        if bot_mention:
                try:
                        await message.add_reaction(':89157:873334902005833778')
                except:
                        await message.add_reaction(':af_pepe_tea:1005139436134223882')

    """@BOT.event
    async def on_member_join(member: discord.Member):
        await member.guild.system_channel.send("{user} joined this Guild".format(user=member.mention))

    @BOT.event
    async def on_member_remove(member: discord.Member):
        await member.guild.system_channel.send("{user} left this Guild".format(user=member.mention))"""

    register_all_commands(BOT)
    BOT.run(Env.TOKEN)
