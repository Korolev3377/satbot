import discord


async def callback(interaction: discord.Interaction):
    await interaction.followup.send("pong")

command = discord.app_commands.Command(
    name="Ping",
    description="Test command",
    callback=callback
)