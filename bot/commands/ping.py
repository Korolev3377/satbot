# ----- Python Standard Library ----- #
import logging

# ----- Discord Python Library ----- #
import discord

Log = logging.getLogger(__name__)

@discord.app_commands.command(
    name="ping",
    description="Test command"
)
async def command(interaction: discord.Interaction):
    Log.debug("Command <ping> triggered")
    await interaction.response.defer(ephemeral=True, thinking=True)
    await interaction.followup.send("pong")