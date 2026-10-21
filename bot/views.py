# ----- Discord Python Library ----- #
from discord import Interaction
from discord import ui

# ----- Local Modules ----- #
from bot.menus import Menu_bot_settings

class View_menu_controls(ui.View):
    menu: Menu_bot_settings = None
    
    def __init__(self, menu: Menu_bot_settings):
        super().__init__()
        self.menu = menu
        
    @ui.button(label="↑ Вира ↑")
    async def btn_up(self, interaction: Interaction, button: ui.Button):
        self.menu.move_cursor(-1)
        await interaction.response.edit_message(content=self.menu.render())

    @ui.button(label="↓ Майна ↓")
    async def btn_down(self, interaction: Interaction, button: ui.Button):
        self.menu.move_cursor(1)
        await interaction.response.edit_message(content=self.menu.render())

    @ui.button(label="ВВод")
    async def btn_enter(self, interaction: Interaction, button: ui.Button):
        await interaction.response.edit_message(content=f"Кнопка была нажата, тест успешен!\nНа кнопку нажал некий {interaction.user.mention}", view=None)

    @ui.button(label="Назад")
    async def btn_back(self, interaction: Interaction, button: ui.Button):
        await interaction.response.edit_message(content=f"Кнопка была нажата, тест успешен!\nНа кнопку нажал некий {interaction.user.mention}", view=None)

    @ui.button(label="Спаси и сохрани")
    async def btn_save(self, interaction: Interaction, button: ui.Button):
        await interaction.response.edit_message(content=f"Кнопка была нажата, тест успешен!\nНа кнопку нажал некий {interaction.user.mention}", view=None)

    @ui.button(label="Галя, у нас отмена")
    async def btn_stash(self, interaction: Interaction, button: ui.Button):
        await interaction.response.edit_message(content=f"Кнопка была нажата, тест успешен!\nНа кнопку нажал некий {interaction.user.mention}", view=None)

    @ui.button(label="Следующаяя страница")
    async def btn_tabnext(self, interaction: Interaction, button: ui.Button):
        await interaction.response.edit_message(content=f"Кнопка была нажата, тест успешен!\nНа кнопку нажал некий {interaction.user.mention}", view=None)
        
    @ui.button(label="Предыдущая страница")
    async def btn_tabprev(self, interaction: Interaction, button: ui.Button):
        await interaction.response.edit_message(content=f"Кнопка была нажата, тест успешен!\nНа кнопку нажал некий {interaction.user.mention}", view=None)

    @ui.button(label="Сброс к заводским")
    async def btn_factoryreset(self, interaction: Interaction, button: ui.Button):
        await interaction.response.edit_message(content=f"Кнопка была нажата, тест успешен!\nНа кнопку нажал некий {interaction.user.mention}", view=None)
    