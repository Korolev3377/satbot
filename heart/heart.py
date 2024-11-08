import time
import http.client as httplib
import urllib
import json

from discord.ext import tasks
from environment import TG_TOKEN, tg_req
from commands.database import DB

loop_seconds = 4.0
cooling_rate = 1 / 0.3


async def tg_send_message(discord_message_id, discord_channel_id, upd, BOT):
  discord_channel = BOT.get_channel(int(discord_channel_id))
  if discord_message_id is False:
    discord_sended_message = await BOT.get_channel(int(discord_channel_id)).send(
      f"{upd.get('message').get('from').get('username')}:\n{upd.get('message').get('text')}")
  else:
    discord_message = discord_channel.get_partial_message(discord_message_id[0])
    discord_sended_message = await discord_message.reply(
      f"{upd.get('message').get('from').get('username')}:\n{upd.get('message').get('text')}")
  return discord_sended_message


class Heart:
  cycle = 0
  step_cycle = 1
  end_cycle = 0
  tg_offset = -1

  def __init__(self, bot):
    self.BOT = bot

  def time_to_cooldown(self, overload):
    return (overload / cooling_rate) * loop_seconds

  @tasks.loop(seconds=loop_seconds, reconnect=False)
  async def beat(self):
    url = '/bot' + TG_TOKEN + '/getUpdates'
    values = {"offset": self.tg_offset}
    res = tg_req("GET", url=url, values=values)

    if res.get("ok"):
      try:
        for upd in res.get("result"):
          self.tg_offset = upd.get("update_id")+1
          if upd.get("message").get("text") == "/allo@MFBK_bot":

            url = '/bot' + TG_TOKEN + '/sendMessage'
            values = {"chat_id": upd.get("message").get("chat").get("id"),
                      "text": f"\"chat.id\" = {upd.get('message').get('chat').get('id')}\n\"message_thread_id\" = {upd.get('message').get('message_thread_id')}",
                      "reply_parameters": f'{{"message_id": {upd.get("message").get("message_id")}, "chat_id": {upd.get("message").get("chat").get("id")}}}',
                      "message_thread_id": upd.get("message").get("message_thread_id")}
            tg_req("POST", url, values=values)

          if upd.get('message').get('text'):
            discord_channel_id = None
            for g_id in self.BOT.guilds_data:
              mfilter = self.BOT.guilds_data.get(g_id).get("discord2tg_bridge").get('from_discord').split(" ")
              # mfilter == ["0000:-0000+00", "1111:-1111+11"]
              for mf in mfilter:
                tg_chat_and_thread = mf.split(":")[1].split("+")  # ["-0000", "00"]
                if tg_chat_and_thread[0] != str(upd.get("message").get("chat").get("id")):
                  continue

                discord_channel_id = mf.split(":")[0]
                if upd.get("message").get("is_topic_message"):
                  if tg_chat_and_thread[1] != str(upd.get("message").get("message_thread_id")):
                    continue

                  if upd.get("message").get("reply_to_message").get("forum_topic_created"):
                    discord_sended_message = await tg_send_message(False, discord_channel_id, upd, self.BOT)
                  else:
                    discord_message_id = await DB.select_d2t_data(id_sourse="telegramm",
                                                                  message_id=str(upd.get("message").get(
                                                                    "reply_to_message").get("message_id")),
                                                                  tg_chat_id=str(upd.get("message").get(
                                                                    "reply_to_message").get("chat").get("id")))
                    discord_sended_message = await tg_send_message(discord_message_id, discord_channel_id, upd, self.BOT)
                else:
                  if tg_chat_and_thread[1] != "0":
                    continue

                  if upd.get("message").get("reply_to_message"):
                    discord_message_id = await DB.select_d2t_data(id_sourse="telegramm",
                                                                  message_id=str(upd.get("message").get(
                                                                    "reply_to_message").get("message_id")),
                                                                  tg_chat_id=str(upd.get("message").get(
                                                                    "reply_to_message").get("chat").get("id")))
                    discord_sended_message = await tg_send_message(discord_message_id, discord_channel_id, upd, self.BOT)
                  else:
                    discord_sended_message = await tg_send_message(False, discord_channel_id, upd, self.BOT)
                await DB.insert_d2t_data(discord_message_id=discord_sended_message.id, tg_message_id=int(upd.get("message").get("message_id")), tg_chat_id=int(upd.get("message").get("chat").get("id")))
          else:
            self.BOT.logger.error(["d2t_b: Нету текста в сообщении.", [upd.get("message").get("chat").get("id"), upd.get("message").get("message_thread_id") or "0"]])
      except Exception as err:
        self.BOT.logger.error(f"В сердце была обнаружена ошибка.\nСистема предотвратила критический сбой, но программа все равно работает не правильно.\nСообщение ошибки:\n{err}")

    for _id, _user in dict(self.BOT.antispam).items():
      if _user.get('overload') > 0:  # Пассивное охлаждение
        _user['overload'] -= cooling_rate
      if _user.get('overload') < 0:
        _user['overload'] = 0
      if _user.get('overload') > 100:
        _user['overloaded'] = True
        _user['overload'] = 100
      if _user.get('overload') == 0:
        self.BOT.antispam.pop(_id)
    self.cycle += cooling_rate / 10000
    if self.cycle >= self.end_cycle:
      self.end_cycle += self.step_cycle
      self.BOT.logger.info(f'Цикл: {round(self.cycle)}')

  @beat.before_loop
  async def before_loop(self):
    self.BOT.logger.info('Сердце запущено!')

  @beat.after_loop
  async def after_loop(self):
    self.BOT.logger.critical("Сердце остановлено!")
