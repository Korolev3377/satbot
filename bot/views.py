# ----- Discord Python Library ----- #
from discord import Interaction
from discord.ui import View, button

class View_menu_controls(View):
    menu = None
    
    def __init__(self, menu):
        self.menu = menu
        
        self.add_item(self.btn_up)
        # TODO: Добавить объявление кнопок
        
    @button("кнопочка!")
    def btn_up(self, interaction: Interaction):
        interaction.edit_original_response(content=f"Кнопка была нажата, тест успешен!\nНа кнопку нажал некий {interaction.user.mention}", view=None)
    # TODO: def действия кнопок с обновлением текста
    