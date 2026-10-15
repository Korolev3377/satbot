# ----- Python Standard Library ----- #
import logging
import sqlite3

# ----- Discord Python Library ----- #
import discord

Log = logging.getLogger(__name__)

class Cli(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tree = None
        self.db = sqlite3.connect("database.db")
        self.db.execute("CREATE TABLE IF NOT EXISTS global_esteem (user_id INTEGER PRIMARY KEY, esteem INTEGER, time INTEGER)")

    def add_tree(self, cmdtree):
        self.tree = cmdtree

    async def on_ready(self):
        Log.info(f"SatBot online\nName: {self.user.name}\nId: {self.user.id}")
        Log.debug("Syncing command tree...")
        await self.tree.sync()
        Log.debug("Command tree synced!")

    async def on_message(self, message):
        # ----- Игнорировать сообщения от себя и других ботов ----- #
        if message.author == self.user or message.author.bot:
            return

    async def on_member_join(self):
        ...

    async def on_member_remove(self):
        ...