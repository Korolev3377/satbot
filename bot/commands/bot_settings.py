# ----- Python Standard Library ----- #
import logging

# ----- Discord Python Library ----- #
import discord

from satbot.menu import Menu

Log = logging.getLogger(__name__)

@discord.app_commands.command(
    name="bot_settings",
    description="Настройка бота"
)
@discord.app_commands.checks.has_permissions(administrator=True)
async def command(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    opening_lines = ["-# Это тестовая версия меню", "# Меню"]
    main_menu_name = "## Главное меню"
    items_map = {
        "Вложенное меню": {},
        "Переключатель 1": True,
        "Переключатель 2": False,
        "Текстовое поле": "Hello, World!",
        "Просто текст": None,

    }
    menu = Menu(opening_lines, main_menu_name, items_map)
    await interaction.followup.send(menu.render())

@command.error
async def error(interaction: discord.Interaction, e: discord.app_commands.AppCommandError):
    await interaction.response.defer(thinking=True, ephemeral=True)
    if isinstance(e, discord.app_commands.MissingPermissions):
        await interaction.followup.send(f"Clearance insufficient")
    else:
        await interaction.followup.send(f"Unhandled error: {str(e)}")
