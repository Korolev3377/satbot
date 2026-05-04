# ----- Python Standard Library ----- #
import logging
# ----------------------------------- #

# ----- Discord Python Library ----- #
import discord
# ---------------------------------- #

Log = logging.getLogger(__name__)

class Client(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        Log.info(f"SatBot online\nName: {self.user.name}\nId: {self.user.id}")