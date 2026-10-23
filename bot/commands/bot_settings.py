# ----- Python Standard Library ----- #
import logging
import json

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
    
    items_list = [ # items_map используется вместе с json.dumps и json.loads, по этому в этом объекте содержатся только списки
        ['note', 'Ниже представлены примеры пунктов меню:'],
        ['switch', 'Переключатель с True и False', True],
        ['text', 'Поле для ввода текста', 'Hello, World!'],
        ['chooseable', 'Выбор из списка', 0, ['Первое', 'Второе', 'Третье']],
        ['menu', 'Вложенное меню', [
            ['note', 'Элемент 1'],
            ['switch', 'Элемент 2', False],
            ['note', 'Элемент 3'],
            ['note', 'Элемент 4'],
            ['note', 'Элемент 5'],
            ['note', 'Элемент 6'],
            ['note', 'Элемент 7']]]
    ] # Список содержит строгую структуру: [тип, визуальное_название, значение, дополнительные_параметры]
    
    items_list = json.loads(json.dumps(items_list)) # Очистка от мусора и валидация json
    
    menu = Menu_bot_settings(opening_lines, main_menu_name, items_list)
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
        
