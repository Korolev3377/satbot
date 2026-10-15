import discord
from discord import app_commands
from discord.ext import commands


class Nickblue_cmds:
    def __init__(self, BOT):
        nb_group = app_commands.Group(name="nb_n", description="nb_d")

        @nb_group.command(name="join_nb_n", description="join_nb_d")
        async def join_nb(interaction: discord.Interaction):
            await interaction.response.defer()
            lang = BOT.tree.translator.get_lang(interaction.locale.value)

            await interaction.followup.send(await BOT.nickblue.add_candidate(interaction.user.id, lang))

        @nb_group.command(name="left_nb_n", description="left_nb_d")
        async def left_nb(interaction: discord.Interaction):
            await interaction.response.defer()
            lang = BOT.tree.translator.get_lang(interaction.locale.value)

            await interaction.followup.send(await BOT.nickblue.remove_candidate(interaction.user.id, lang))

        @nb_group.command(name="show_nb_n", description="show_nb_d")
        async def show_nb(interaction: discord.Interaction):
            await interaction.response.defer()
            lang = BOT.tree.translator.get_lang(interaction.locale.value)

            await interaction.followup.send(await BOT.nickblue.show_candidates(lang))

        BOT.tree.add_command(nb_group)
