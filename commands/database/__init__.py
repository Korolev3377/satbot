import sqlite3 as sql
from typing import Any, Union, NoReturn

from discord.app_commands import Choice

from environment.variable import *


class DataBase:
  def __init__(self) -> None:
    self.db_connection = None
    self.db_cursor = None
    self.connect()
    self.disconnect()

  def connect(self) -> NoReturn:
    self.db_connection = sql.connect("database.db")
    self.db_cursor = self.db_connection.cursor()

  def disconnect(self) -> NoReturn:
    self.db_connection.commit()
    self.db_connection.close()

  async def execute(self, q: str, arg: tuple = None, fetchone: bool = True) -> Union[tuple, bool]:
    while LOCK.locked():
      await asyncio.sleep(0.5)
    async with LOCK:
      self.connect()
      self.db_cursor.execute(q, arg) if arg else self.db_cursor.execute(q)
      i = self.db_cursor.fetchone() if fetchone else self.db_cursor.fetchall()
      self.disconnect()
      return i or False

  # persistent messages
  async def select_message_data(self, message_id):
    return await self.execute("SELECT data FROM persistent WHERE message_id = ?;", (message_id,))

  async def insert_message_data(self, message_id, message_data):
    await self.execute("INSERT INTO persistent (message_id, data) VALUES (?, ?);", (message_id, message_data))

  async def update_message_data(self, message_id, message_data):
    await self.execute("UPDATE persistent SET data = ? WHERE message_id = ?;", (message_data, message_id))

  async def delete_message_data(self, message_id):
    await self.execute("DELETE FROM persistent WHERE message_id = ?;", (message_id,))

  # d2t bridge
  async def insert_d2t_data(self, discord_message_id, tg_message_id, tg_chat_id):
    await self.execute("INSERT INTO d2t_bridge (discord_message_id, tg_message_id, tg_chat_id) VALUES (?, ?, ?);",
                       (discord_message_id, tg_message_id, tg_chat_id))

  async def select_d2t_data(self, id_sourse, message_id, tg_chat_id=None):
    if id_sourse == "telegramm" and tg_chat_id:
      return await self.execute(
        "SELECT discord_message_id FROM d2t_bridge WHERE tg_message_id = ? AND tg_chat_id = ?;",
        (message_id, tg_chat_id)
      )
    elif id_sourse == "discord":
        return await self.execute(
            "SELECT tg_message_id, tg_chat_id FROM d2t_bridge WHERE discord_message_id = ?;",
            (message_id,)
        )


DB = DataBase()
