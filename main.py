import os
import sys
import asyncio
import time
import logging
import pickle as pik
import http.client as httplib
import urllib

import atexit
import signal

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
      for i in (BotsayView,):  # Запуск постоянных View
        self.add_view(i())

      async for g in self.fetch_guilds():  # Загрузка кофига серверов.
        await DB.execute(
          "CREATE TABLE if not exists servers_config (server_id NOT NULL UNIQUE, cfg_data);")
        data = await DB.execute("SELECT cfg_data FROM servers_config WHERE server_id IS ?;", (str(g.id),))
        try:
          assert data[0]
          self.guilds_data[str(g.id)] = pik.loads(data[0])
        except:
          self.guilds_data[str(g.id)] = CONFIG.DEFAULT_CFG
          await DB.execute("INSERT INTO servers_config (server_id, cfg_data) VALUES (?, ?);",
                           (str(g.id), pik.dumps(self.guilds_data[str(g.id)])))

        self.guilds_data[str(g.id)] = config_autofix(self.guilds_data[str(g.id)], CONFIG.DEFAULT_CFG)
        await DB.execute("UPDATE servers_config SET cfg_data = ? WHERE server_id = ?;",
                         ((pik.dumps(self.guilds_data[str(g.id)])), str(g.id)))


  BOT = Bot()
  _F = Facts(BOT.logger)
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
    BOT.tree.on_error = on_error_handler  # Заглушка для ошибок
    BOT.tree.interaction_check = itr_check  # Проверка на возможность выполнения команд
    await BOT.tree.set_translator(T(bot=BOT))  # Установка переводчика
    await declare_commands(BOT)  # Обьявить выбранные команды

    @atexit.register
    def bot_exit_handler():
      BOT.logger.critical(f"Бот остановлен! Имя: {BOT.user} ИД: {BOT.user.id}")

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
      if message.author == BOT.user:
        return

      status_d2t_0, _ = check_config(BOT.guilds_data, [str(message.guild.id), "discord2tg_bridge", "enable_d2t"])
      status_d2t_1, _ = check_config(BOT.guilds_data,
                                     [str(message.guild.id), "discord2tg_bridge", "enable_from_discord"])
      status_d2t_2, _ = check_config(BOT.guilds_data, [str(message.guild.id), "discord2tg_bridge", "from_discord"])
      if status_d2t_0 and status_d2t_1 and status_d2t_2:
        if BOT.guilds_data.get(str(message.guild.id)).get("discord2tg_bridge", "enable_d2t"):
          if BOT.guilds_data.get(str(message.guild.id)).get("discord2tg_bridge", "enable_from_discord"):
            mfilter = BOT.guilds_data.get(str(message.guild.id)).get("discord2tg_bridge").get("from_discord").split(" ")
            # mfilter == ["1090104010005050103:-1000202090908+2060", "1090104010005050103:-1000202090908+2060"]
            for mf in mfilter:
              if str(message.channel.id) == mf.split(":")[0] and message.content:  # "1090104010005050103"
                tg_chat_and_thread = mf.split(":")[1].split("+")  # ["-1000202090908", "2060"]
                url = '/bot' + TG_TOKEN + '/sendMessage'
                values = {"chat_id": tg_chat_and_thread[0],
                          "text": f"{message.author.name}:\n{message.content}",
                          "message_thread_id": tg_chat_and_thread[1]}
                upd = tg_req("POST", url=url, values=values)
                DB.insert_d2t_data(discord_message_id=message.id,
                                   tg_message_id=int(upd.get("message").get("message_thread_id") or "0"),
                                   tg_chat_id=int(upd.get("message").get("chat").get("id")))

      if message.author.bot:
        return

      status, _ = check_config(BOT.guilds_data, [str(message.guild.id), "fact_word_react"])
      if status:
        if not BOT.guilds_data.get(str(message.guild.id)).get("fact_word_react"):
          return

      msg = message.content.lower()

      await DB.execute(
        "CREATE TABLE if not exists funfact_ignore (id INTEGER NOT NULL, value INTEGER DEFAULT (0));")
      ignore = await DB.execute("SELECT value FROM funfact_ignore WHERE id = ?;", (message.author.id,))
      if ignore is False:
        await DB.execute("INSERT INTO funfact_ignore (id, value) VALUES (?, ?);", (message.author.id, 0))
        ignore = await DB.execute("SELECT value FROM funfact_ignore WHERE id = ?;", (message.author.id,), True)
      ignore = ignore[0]
      if ignore == 0:
        if lang := _F.find_fact(msg=msg):
          if fact := await _F.read_facts(guild=message.guild, lang=lang):
            await message.channel.send(fact)


  @BOT.event
  async def on_member_join(member: discord.Member):
    status_1, code_1 = check_config(BOT.guilds_data, [str(member.guild.id), "server_member_join_leave", "enable"])
    status_2, code_2 = check_config(BOT.guilds_data, [str(member.guild.id), "server_member_join_leave", "on_join"])
    status_3, code_3 = check_config(BOT.guilds_data, [str(member.guild.id), "server_member_join_leave", "on_leave"])
    status_4, code_4 = check_config(BOT.guilds_data,
                                    [str(member.guild.id), "server_member_join_leave", "channel_id"])

    codes = {
      0: f"Ошибка в конфигурации сервера \"{member.guild.name}\": Нету конфигурации для сервера.",
      1: f"Ошибка в конфигурации сервера \"{member.guild.name}\": Проблема \"server_member_join_leave\" в конфигурации сервера.",
      2: f"Ошибка в конфигурации сервера \"{member.guild.name}\": Отсутствует внутренний парамтер в \"server_member_join_leave\""
    }
    if status_1:
      if BOT.guilds_data.get(str(member.guild.id)).get("server_member_join_leave").get("enable"):
        if status_2 and status_3 and status_3:
          if not BOT.guilds_data.get(str(member.guild.id)).get("server_member_join_leave").get("channel_id"):
            channel = member.guild.system_channel
          else:
            channel = member.guild.get_channel(
              int(BOT.guilds_data.get(str(member.guild.id)).get("server_member_join_leave").get(
                "channel_id")))
          await channel.send(
            BOT.guilds_data.get(str(member.guild.id)).get("server_member_join_leave").get("on_join").format(
              user_mention=member.mention, user_id=member.id, user_name=member.name))
    else:
      BOT.logger.error(codes.get(code_1))


  @BOT.event
  async def on_member_remove(member: discord.Member):
    status_1, code_1 = check_config(BOT.guilds_data, [str(member.guild.id), "server_member_join_leave", "enable"])
    status_2, code_2 = check_config(BOT.guilds_data, [str(member.guild.id), "server_member_join_leave", "on_join"])
    status_3, code_3 = check_config(BOT.guilds_data, [str(member.guild.id), "server_member_join_leave", "on_leave"])
    status_4, code_4 = check_config(BOT.guilds_data,
                                    [str(member.guild.id), "server_member_join_leave", "channel_id"])

    codes = {
      0: f"Ошибка в конфигурации сервера \"{member.guild.name}\": Нету конфигурации для сервера.",
      1: f"Ошибка в конфигурации сервера \"{member.guild.name}\": Проблема \"server_member_join_leave\" в конфигурации сервера.",
      2: f"Ошибка в конфигурации сервера \"{member.guild.name}\": Отсутствует внутренний парамтер в \"server_member_join_leave\""
    }
    if status_1:
      if BOT.guilds_data.get(str(member.guild.id)).get("server_member_join_leave").get("enable"):
        if status_2 and status_3 and status_3:
          if not BOT.guilds_data.get(str(member.guild.id)).get("server_member_join_leave").get("channel_id"):
            channel = member.guild.system_channel
          else:
            channel = member.guild.get_channel(
              int(BOT.guilds_data.get(str(member.guild.id)).get("server_member_join_leave").get(
                "channel_id")))
          await channel.send(
            BOT.guilds_data.get(str(member.guild.id)).get("server_member_join_leave").get(
              "on_leave").format(
              user_mention=member.mention, user_id=member.id, user_name=member.name))
    else:
      BOT.logger.error(codes.get(code_1))


  BOT.run(TOKEN, log_formatter=BOT.formatter, log_handler=logging.NullHandler(), root_logger=True)
