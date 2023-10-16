import os
import sys
import asyncio
import time
import logging
import pickle as pik

import discord
from discord.ext import commands
from discord.app_commands import locale_str as _ls

from commands import declare_commands
from environment import *
from heart import Heart
from translator import T
from commands.admin import BotsayView
from commands.database import DB

LOGGING_MODE = logging.INFO

if __name__ == '__main__':
    class Bot(commands.Bot):
        def __init__(self):
            super().__init__(command_prefix=CONFIG.CMD_PREFIX,
                             help_command=None,
                             strip_after_prefix=True,
                             intents=CONFIG.INTENTS)

            # Настройка логгера.
            self.logger = logging.getLogger('discord')
            self.logger.setLevel(LOGGING_MODE)

            self.formatter = logging.Formatter("[%(asctime)s] [%(levelname)-8s] %(message)s", '%Y-%m-%d %H:%M:%S')

            curtime = time.strftime("%Y-%m-%d %H-%M-%S")
            try:
                self.handler = logging.FileHandler("logs/%s.log" % curtime, 'w', encoding="utf-8")
            except FileNotFoundError:
                os.mkdir("logs")
                self.handler = logging.FileHandler("logs/%s.log" % curtime, 'w', encoding="utf-8")

            self.handler.setFormatter(self.formatter)

            self.stream = logging.StreamHandler(sys.stdout)
            self.stream.setFormatter(self.formatter)

            logging.Handler()
            self.logger.addHandler(self.handler)
            self.logger.addHandler(self.stream)

            self.guilds_data = {}

            self.antispam = {}
            # Это ограничитель спама комманд для каждого пользователя.
            # Срабатывает при превышении лимита и отключается при понижении до 0.

            self.heart = Heart(self)
            # Это главный цикл бота. В нем идет пассивное уменьшение КД и проверка на то,
            # когда нужно будет менять Синего ника. Если вообще нужно будет.

        async def setup_hook(self):
            self.tree.interaction_check = itr_check  # Проверка на возможность выполнения команд
            self.tree.on_error = on_error_handler  # Заглушка для ошибок
            declare_commands(self)  # Обьявить выбранные команды
            await self.tree.set_translator(T(bot=self))  # Установка переводчика
            await self.tree.sync()  # Синхронизация. Для обновления изменения комманд
            for i in (BotsayView,):  # Запуск постоянных View
                self.add_view(i())
            async for g in self.fetch_guilds():  # Загрузка кофига серверов.
                await DB.execute("CREATE TABLE if not exists servers_config (server_id INTEGER NOT NULL UNIQUE, cfg_data);")
                data = await DB.execute("SELECT cfg_data FROM servers_config WHERE server_id IS ?;", (g.id,))
                try:
                    assert data[0]
                    self.guilds_data[g.id] = pik.loads(data[0])
                except:
                    data = {
                        "roles_to_sale": {
                            ROLE_ID: {
                                "id": "role_id",
                                "name": "role name",
                                "cost": None,
                                "stock": 0,
                                "visible": False
                            }
                            # cost - 0 - Бесплатное
                            # cost - None - Не продается
                            # stock - 0 - Закончился товар
                            # stock - None - Бесконечное количество
                        },
                        "users_role_inv": {
                            ROLE_ID: []  # Лист ролей, которые есть у пользователя.
                        }
                    }
                    self.guilds_data[g.id] = data
                    await DB.execute("INSERT INTO servers_config (server_id, cfg_data) VALUES (?, ?);",
                                     (g.id, pik.dumps(self.guilds_data[g.id])))


    BOT = Bot()
    _F = Facts()
    _T = T()


    async def on_error_handler(interaction: discord.Interaction, error):
        _T.set_string(
            _ls(ERROR)
        )
        BOT.logger.error(error, interaction.user, interaction)
        await interaction.followup.send(_T.stranslate(), ephemeral=True)
        return False


    async def itr_check(interaction: discord.Interaction):  # Проверка на возможность выполнения комманды
        _T.set_language(interaction.locale)
        _user = interaction.user.id

        # Системные комманды могут вызываться без последствий
        if interaction.command.extras.get(IS_SYSTEM) or interaction.type == discord.InteractionType.autocomplete:
            if BOT.antispam.get(_user):
                if BOT.antispam.get(_user).get(USER_LOAD) > 100.0:
                    BOT.antispam[_user][IS_USER_OVERLOADED] = True
            return True

        # Проверка на личные ссообщения
        if not interaction.command.extras.get(IS_DM_ALLOWED) and not interaction.channel.guild:
            _T.set_string(_ls(IS_DM_ALLOWED))
            await interaction.response.send_message(_T.stranslate(), ephemeral=True)
            return False

        # Проверка на перегрузку
        if BOT.antispam.get(_user):
            if BOT.antispam.get(_user).get(IS_USER_OVERLOADED):
                _T.set_string(ls(
                    ON_COOLDOWN,
                    {TIME: int(BOT.heart.time_to_cooldown(BOT.antispam.get(_user).get(USER_LOAD)))}))
                await interaction.response.send_message(_T.stranslate(), ephemeral=True)
                return False

        # Проверка на отключенную комманду
        if interaction.command.extras.get(IS_DISABLED):
            _T.set_string(_ls(IS_DISABLED))
            await interaction.response.send_message(_T.stranslate(), ephemeral=True)
            return False

        # Предупреждение, что эта комманда сломана.
        if interaction.command.extras.get(IS_BROKEN):
            _T.set_string(_ls(IS_BROKEN))
            await interaction.response.send_message(_T.stranslate(), ephemeral=True)
            return False

        # Проверка на администратора сервера
        if not interaction.permissions.administrator and interaction.command.extras.get(IS_ADMIN_ONLY):
            if not await BOT.is_owner(interaction.user):
                _T.set_string(_ls(IS_DM_ALLOWED))
                await interaction.response.send_message(_T.stranslate(), ephemeral=True)
                return False

        # Проверка на создателя бота
        if not await BOT.is_owner(interaction.user) and interaction.command.extras.get(IS_OWNER_ONLY):
            _T.set_string(_ls(IS_OWNER_ONLY))
            await interaction.response.send_message(_T.stranslate(), ephemeral=True)
            return False

        if not BOT.antispam.get(_user):
            BOT.antispam[_user] = {
                USER_LOAD: 0,
                IS_USER_OVERLOADED: False
            }
        BOT.antispam[_user][USER_LOAD] += BOT.antispam[_user][USER_LOAD] + 15
        if BOT.antispam.get(_user).get(USER_LOAD) > 100.0:
            BOT.antispam[_user][IS_USER_OVERLOADED] = True
        return True


    @BOT.event
    async def on_ready():
        BOT.logger.info(f"Бот запущен! Имя: {BOT.user} ИД: {BOT.user.id}")
        if translate_not_found := BOT.tree.translator.translate_not_found:
            BOT.logger.error(f"Перевод не найден для: {translate_not_found}")
        if not BOT.heart.beat.is_running():
            await BOT.heart.beat.start()


    @BOT.event
    async def on_connect():
        BOT.logger.info("Соединение с Дискордом установлено!")


    @BOT.event
    async def on_disconnect():
        BOT.logger.info(f"Переподключение к Дискорду. Цикл: {round(BOT.heart.cycle, 3)}")


    @BOT.event
    async def on_message(message):
        if message.guild:
            if message.author == BOT.user or message.author.bot or message.guild.get_member(872406824765251594):
                return

            msg = message.content.lower()

            await DB.execute("CREATE TABLE if not exists funfact_ignore (id INTEGER NOT NULL, value INTEGER DEFAULT (0));")
            ignore = await DB.execute("SELECT value FROM funfact_ignore WHERE id = ?;", (message.author.id,))
            if ignore is False:
                await DB.execute("INSERT INTO funfact_ignore (id, value) VALUES (?, ?);", (message.author.id, 0))
                ignore = await DB.execute("SELECT value FROM funfact_ignore WHERE id = ?;", (interaction.user.id,), True)
            ignore = ignore[0]
            if lang := _F.find_fact(msg=msg) and ignore == 0:
                if fact := await _F.read_facts(guild=message.guild, lang=lang):
                    await message.channel.send(fact)

            """bot_mention = re.search(
                r"(\b8915-7\b|"
                r"\b872406824765251594\b|"
                r"\bбарменбот(а|у|ом|е|ы|ов|ам|ами|ах|о)?\b|"
                r"\bбармен(а|у|ом|е|ы|ов|ам|ами|ах|о)?\b|"
                r"\bфактобот(а|у|ом|е|ы|ов|ам|ами|ах|о)?\b"
                r"|\bббот\b|"
                r"\bbbot\b|"
                r"\bbarmen\b|"
                r"\bbartender\b|"
                r"\bbartenderbot\b)", msg)"""


    @BOT.event
    async def on_member_join(member: discord.Member):
        await member.guild.system_channel.send("{user} :inbox_tray:".format(user=member.mention))


    @BOT.event
    async def on_member_remove(member: discord.Member):
        await member.guild.system_channel.send("{user} :outbox_tray:".format(user=member.mention))


    BOT.run(TOKEN, log_formatter=BOT.formatter, log_handler=logging.NullHandler(), root_logger=True)
