# ----- Python Standard Library ----- #
import logging

# ----- Discord Python Library ----- #
import discord

# ----- Local Modules ----- #
from bot.menus import Menu_bot_settings
from bot.views import View_menu_controls

Log = logging.getLogger(__name__)

@discord.app_commands.command(
    name="bot_settings",
    description="Настройка бота"
)
@discord.app_commands.checks.has_permissions(administrator=True)
async def command(interaction: discord.Interaction):
    opening_lines = ["-# Тестовая версия меню", "# Настройка бота"]
    main_menu_name = "## Главное меню"
    items_map = {
        "Вложенное меню": {},
        "Переключатель 1": True,
        "Произвольный текст без редактирования": None,
        "Переключатель 2": False,
        "Текстовое поле": "Hello, World!"
    }
    menu = Menu_bot_settings(opening_lines, main_menu_name, items_map)
    view = View_menu_controls(menu)
    await interaction.response.send_message(menu.render(), view=view, ephemeral=True) # ephemeral Важно, так как нет TODO: проверки на права пользователя при нажатии кнопок

@command.error
async def error(interaction: discord.Interaction, e: discord.app_commands.AppCommandError):
    if isinstance(e, discord.app_commands.MissingPermissions):
        await interaction.response.send_message(f"Clearance insufficient")
    else:
        await interaction.response.send_message(f"Unhandled error: {str(e)}")
        exc = getattr(e, "original", e)
        Log.error("Unhandled error", (type(exc), exc, exc.__traceback__))
        
