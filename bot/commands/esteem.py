# ----- Python Standard Library ----- #
import logging
from random import random
import time

# ----- Discord Python Library ----- #
import discord

import sqlite3

Log = logging.getLogger(__name__)

@discord.app_commands.command(
    name="esteem",
    description="Повысь свою самооценку"
)
async def command(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    conn: sqlite3.Connection = interaction.client.db
    user_data = conn.execute("SELECT * FROM global_esteem WHERE user_id = ?;", [interaction.user.id]).fetchone()
    add_esteem = round(random()*10)-2
    new_esteem = None
    on_cd = False
    if user_data:
        if user_data[2]+604800 > round(time.time()):
            on_cd = True
        else:
            new_esteem = user_data[1]+add_esteem
            conn.execute(
            "UPDATE global_esteem SET user_id = ?, esteem = ?, time = ? WHERE user_id = ?;",
                [
                    user_data[0],
                    new_esteem,
                    round(time.time()),
                    interaction.user.id
                ]
            )
    else:
        conn.execute("INSERT INTO global_esteem VALUES (?, ?, ?);", [interaction.user.id, add_esteem, round(time.time())])
    conn.commit()
    if on_cd:
        await interaction.followup.send(f"Вы можете повысить свою самооценку <t:{user_data[2]+604800}:R>")
    else:
        if add_esteem > 0:
            await interaction.followup.send(f"Ваша самооценка повысилась на {add_esteem} и теперь составляет {new_esteem or add_esteem}")
        elif add_esteem < 0:
            await interaction.followup.send(f"Ваша самооценка понизилась на {add_esteem} и теперь составляет {new_esteem or add_esteem}")
        else:
            await interaction.followup.send("Ваша самооценка никак не изменилась")