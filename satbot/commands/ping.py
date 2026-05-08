# ----- Python Standard Library ----- #
import logging

# ----- Discord Python Library ----- #
import discord

Log = logging.getLogger(__name__)

async def callback(interaction: discord.Interaction):
    Log.debug("Command <ping> triggered")
    await interaction.response.defer(ephemeral=True, thinking=True)
    await interaction.followup.send("pong")

command = discord.app_commands.Command(
    name="ping",
    description="Test command",
    callback=callback
)