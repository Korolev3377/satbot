import time
import http.client as httplib
import urllib
import json

from discord.ext import tasks
from environment import TG_TOKEN

loop_seconds = 1.0
cooling_rate = 1 / 1.2


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
    self.BOT.logger.info(["тик", round(self.cycle)])
    host = 'api.telegram.org'
    url = '/bot' + TG_TOKEN + '/getUpdates'
    url = url.replace("\n", "")

    values = {"offset": self.tg_offset}

    headers = {
      'User-Agent': 'python',
      'Content-Type': 'application/x-www-form-urlencoded',
    }

    values = urllib.parse.urlencode(values)

    conn = httplib.HTTPSConnection(host)
    conn.request("GET", url, values, headers)
    response = conn.getresponse()
    res = json.loads(response.read())
    if res.get("ok"):
      for upd in res.get("result"):
        self.BOT.logger.info("start")
        self.tg_offset = upd.get("update_id")+1
        self.BOT.logger.info(["1", upd.get("message").get("text"), "/allo@MFBK_bot", upd.get("message").get("text") == "/allo@MFBK_bot"])
        if upd.get("message").get("text") == "/allo@MFBK_bot":
          url = '/bot' + TG_TOKEN + '/sendMessage'
          url = url.replace("\n", "")

          values = {"chat_id": upd.get("message").get("chat").get("id"),
                    "text": f"chat.id = {upd.get('message').get('chat').get('id')}\n{upd.get('message').get('message_thread_id')}",
                    "reply_parameters": {"message_id": upd.get("message").get("message_id"),
                                         "chat_id": upd.get("message").get("chat").get("id")},
                    "message_thread_id": upd.get("message").get("message_thread_id")}

          headers = {
            'User-Agent': 'python',
            'Content-Type': 'application/x-www-form-urlencoded',
          }

          self.BOT.logger.info(json.dumps(values))
          values = urllib.parse.urlencode(json.dumps(values))
          self.BOT.logger.info(values)
          conn = httplib.HTTPSConnection(host)
          conn.request("POST", url, values, headers)
          response = conn.getresponse()
          self.BOT.logger.info(response.read())
          self.BOT.logger.info("end")

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
