import discord
from discord import app_commands

from .games.bf import Brainfuck

@app_commands.command(name="bf_n", description="bf_d")
async def bf_cmd(interaction, code: str, *, input: str = None):
    await interaction.response.defer()
    await interaction.followup.send("`"+Brainfuck().run(code, input)+"`")
