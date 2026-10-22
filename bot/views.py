# ----- Discord Python Library ----- #
from discord import Interaction
from discord import ui

# ----- Local Modules ----- #
from bot.menus import Menu_bot_settings
from discord.enums import ButtonStyle

class View_menu_controls(ui.View):
    menu: Menu_bot_settings = None
    
    def __init__(self, menu: Menu_bot_settings):
        super().__init__()
        self.menu = menu
        
    @ui.button(label="↑ Вира ↑", row=0)
    async def btn_up(self, interaction: Interaction, button: ui.Button):
        self.menu.move_cursor(-1)
        await interaction.response.edit_message(content=self.menu.render())

    @ui.button(label="↓ Майна ↓", row=0)
    async def btn_down(self, interaction: Interaction, button: ui.Button):
        self.menu.move_cursor(1)
        await interaction.response.edit_message(content=self.menu.render())

    @ui.button(label="Ввести", row=0, style=ButtonStyle.blurple)
    async def btn_enter(self, interaction: Interaction, button: ui.Button):
        self.menu.enter()
        await interaction.response.edit_message(content=self.menu.render())

    @ui.button(label="Назад", row=0, style=ButtonStyle.blurple)
    async def btn_back(self, interaction: Interaction, button: ui.Button):
        self.menu.back()
        await interaction.response.edit_message(content=self.menu.render())
        
    @ui.button(label="Предыдущая страница", row=1)
    async def btn_tabprev(self, interaction: Interaction, button: ui.Button):
        self.menu.change_page(-1)
        await interaction.response.edit_message(content=self.menu.render())

    @ui.button(label="Следующаяя страница", row=1)
    async def btn_tabnext(self, interaction: Interaction, button: ui.Button):
        self.menu.change_page(1)
        await interaction.response.edit_message(content=self.menu.render())

    @ui.button(label="Спаси и сохрани", row=2, style=ButtonStyle.green)
    async def btn_save(self, interaction: Interaction, button: ui.Button):
        await interaction.response.edit_message(content=f"Заглушка", view=None)

    @ui.button(label="Галя, у нас отмена", row=2, style=ButtonStyle.blurple)
    async def btn_stash(self, interaction: Interaction, button: ui.Button):
        await interaction.response.edit_message(content=f"Заглушка", view=None)

    @ui.button(label="Сброс к заводским", row=2, style=ButtonStyle.red)
    async def btn_factoryreset(self, interaction: Interaction, button: ui.Button):
        await interaction.response.edit_message(content=f"Заглушка", view=None)
    