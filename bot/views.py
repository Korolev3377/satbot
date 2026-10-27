# ----- Discord Python Library ----- #
from discord import Interaction
from discord import ui
from discord import SelectOption

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
        cur_item = self.menu.get_current_item()
        match cur_item[0]:
            case "text":
                modal = Modal_text_prompt(title=cur_item[1], menu=self.menu)
                await interaction.response.send_modal(modal)
            case "chooseable":
                view = View_choose_prompt(menu=self.menu, original_view=self)
                await interaction.response.edit_message(view=view)
            case _:
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

class Modal_text_prompt(ui.Modal):
    def __init__(self, title: str, menu: Menu_bot_settings):
        super().__init__(title=title)
        self.menu = menu
        self.text_input = ui.TextInput(label="Введите новое значение")
        self.add_item(self.text_input)
        
    async def on_submit(self, interaction: Interaction):
        if self.text_input.value:
            self.menu.enter(self.text_input.value)
        else:
            self.menu.enter()
        await interaction.response.edit_message(content=self.menu.render())

class View_choose_prompt(ui.View):
    def __init__(self, menu: Menu_bot_settings, original_view):
        super().__init__()
        self.menu = menu
        self.original_view = original_view
        self.selected = None
        
        options = [SelectOption(label=l, value=i) for i, l in enumerate(self.menu.get_current_item()[3])]
        self.select = ui.Select(options=options, row=0)
        self.select.callback = self.select_callback
        
        self.add_item(self.select)
        
    async def select_callback(self, interaction: Interaction):
        await interaction.response.defer()
        self.selected = int(self.select.values[0])
    
    @ui.button(label="Выбрать", row=1, style=ButtonStyle.green)
    async def btn_enter(self, interaction: Interaction, button: ui.Button):
        if self.selected:
            self.menu.enter(self.selected)
        await interaction.response.edit_message(content=self.menu.render(), view=self.original_view)

    @ui.button(label="Отмена", row=1, style=ButtonStyle.red)
    async def btn_back(self, interaction: Interaction, button: ui.Button):
        await interaction.response.edit_message(content=self.menu.render(), view=self.original_view)