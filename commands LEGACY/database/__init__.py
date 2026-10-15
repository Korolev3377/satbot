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

    async def select_message_data(self, message_id):
        return await self.execute("SELECT data FROM persistent WHERE message_id = ?;", (message_id,))

    async def insert_message_data(self, message_id, message_data):
        await self.execute("INSERT INTO persistent (message_id, data) VALUES (?, ?);", (message_id, message_data))

    async def update_message_data(self, message_id, message_data):
        await self.execute("UPDATE persistent SET data = ? WHERE message_id = ?;", (message_data, message_id))

    async def delete_message_data(self, message_id):
        await self.execute("DELETE FROM persistent WHERE message_id = ?;", (message_id,))


DB = DataBase()
