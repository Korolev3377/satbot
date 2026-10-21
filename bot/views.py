# ----- Discord Python Library ----- #
from discord import Interaction
from discord import ui

class View_menu_controls(ui.View):
    menu = None
    
    def __init__(self, menu):
        super().__init__()
        self.menu = menu
        # TODO: Добавить объявление кнопок
        
    @ui.button(label="Кнопочка!")
    async def btn_up(self, interaction: Interaction, button: ui.Button):
        await interaction.response.edit_message(content=f"Кнопка была нажата, тест успешен!\nНа кнопку нажал некий {interaction.user.mention}", view=None)
    # TODO: def действия кнопок с обновлением текста
    