import asyncio

import discord
from discord import app_commands

from .games.gol_game import GameOfLife
from discord.app_commands import locale_str as _ls
from translator.__init__ import T
from environment.variable import *

GAME_OF_LIVE_NAME = "gol_name"
GAME_OF_LIVE_DESC = "gol_desc"
START = "start"
STOP = "stop"
EXIT = "exit"
FSIZE = "fsize"

_locale = {
    GAME_OF_LIVE_NAME: {
        EN: 'game-of-live',
        RU: 'игра-в-жизнь'
    },
    GAME_OF_LIVE_DESC: {
        EN: 'Launch Game of life simulation',
        RU: 'Запустить симуляцию Игры в жизнь'
    },
    START: {
        EN: "Start",
        RU: "Запустить"
    },
    STOP: {
        EN: "Stop",
        RU: "Остановить"
    },

    EXIT: {
        EN: "Exit",
        RU: "Выйти"
    },

    FSIZE: {EN: "field-size",
            RU: "размер-поля"}
}

_T = T(locale_dict=_locale)


@app_commands.command(
    name=namedesc(GAME_OF_LIVE_NAME, _locale),
    description=namedesc(GAME_OF_LIVE_DESC, _locale),
    extras={USAGE: "gol_doc"}
)
@app_commands.rename(size=namedesc(FSIZE, _locale))
async def gameoflife(interaction: discord.Interaction, size: app_commands.Range[int, 3, 28] = 5):
    await interaction.response.defer()
    _T.set_language(interaction.locale)
    gol = GameOfLife()
    if 3 <= size <= 13:
        view = GameOfLifeView(interaction.user, gol, size)
    elif 14 <= size <= 28:
        view = GameOfLifeView(interaction.user, gol, size, binary=True)
    else:
        view = GameOfLifeView(interaction.user, gol, 5, langlang)
    await interaction.followup.send(content=view.render(), view=view)


class GameOfLifeView(discord.ui.View):
    runing = False

    def __init__(self, author, gol, size, binary=False):
        super().__init__()
        self.binary = binary
        self.field = gol.Field(size=size)
        self.user = author
        if self.binary:
            button_layers = [
                ["7", "8", "9"],
                ["4", "5", "6"],
                ["1", "2", "3"],
                ["S-E", "Q", "01"]
            ]
        else:
            button_layers = [
                ["7", "8", "9", "01"],
                ["4", "5", "6", "03"],
                ["1", "2", "3", None],
                ["02", None, None, None],
                ["S-E", "Q"]
            ]
        for y, layer in enumerate(button_layers):
            for button_type in layer:
                self.add_item(self.GolControlButton(button_type=button_type, row=y))

    def render(self):
        field = self.field.print_field()
        rendered_field = []
        if self.binary:
            for sym in field:
                if sym == "@":
                    rendered_field.append(("♪  ", "♫ ")[self.runing])
                elif sym == "+":
                    rendered_field.append("█")
                elif sym == "↓":
                    if self.runing:
                        rendered_field.append("█")
                    else:
                        rendered_field.append("▀")
                elif sym == "→":
                    if self.runing:
                        rendered_field.append("█")
                    else:
                        rendered_field.append("▌")
                elif sym == "0":
                    rendered_field.append("░")
                elif sym == "1":
                    rendered_field.append("█")
                elif sym == "\n":
                    rendered_field.append("\n")
        else:
            for sym in field:
                if sym == "@":
                    rendered_field.append(("🔴", "🟢")[self.runing])
                elif sym == "+":
                    rendered_field.append("🔹")
                elif sym == "↓":
                    if self.runing:
                        rendered_field.append("🔹")
                    else:
                        rendered_field.append("⬇️")
                elif sym == "→":
                    if self.runing:
                        rendered_field.append("🔹")
                    else:
                        rendered_field.append("➡️")
                elif sym == "0":
                    rendered_field.append("⬛")
                elif sym == "1":
                    rendered_field.append("◻️")
                elif sym == "2":
                    rendered_field.append("📦")
                elif sym == "3":
                    rendered_field.append("🧨")
                elif sym == "4":
                    rendered_field.append("💥")
                elif sym == "\n":
                    rendered_field.append("\n")
        return "".join(rendered_field)

    class GolControlButton(discord.ui.Button):
        def __init__(self, button_type=None, row=0):
            # Cursor move
            if button_type == "8":
                super().__init__(emoji="⬆️", row=row, custom_id=button_type)
            elif button_type == "4":
                super().__init__(emoji="⬅️", row=row, custom_id=button_type)
            elif button_type == "6":
                super().__init__(emoji="➡️", row=row, custom_id=button_type)
            elif button_type == "2":
                super().__init__(emoji="⬇️", row=row, custom_id=button_type)

            # Diagonal cursor move
            elif button_type == "7":
                super().__init__(emoji="↖️", row=row, custom_id=button_type)
            elif button_type == "9":
                super().__init__(emoji="↗️", row=row, custom_id=button_type)
            elif button_type == "1":
                super().__init__(emoji="↙️", row=row, custom_id=button_type)
            elif button_type == "3":
                super().__init__(emoji="↘️", row=row, custom_id=button_type)

            # Flip cell
            elif button_type == "5":
                super().__init__(style=discord.ButtonStyle.blurple, emoji="◻️", row=row, custom_id=button_type)
            elif button_type == "01":
                super().__init__(emoji="⏯️", row=row, custom_id=button_type)
            elif button_type == "02":
                super().__init__(emoji="📦", row=row, custom_id=button_type)
            elif button_type == "03":
                super().__init__(emoji="🧨", row=row, custom_id=button_type)

            # Control
            elif button_type == "Q":
                super().__init__(style=discord.ButtonStyle.red,
                                 label=_T.stranslate(_ls(EXIT)),
                                 row=row,
                                 custom_id=button_type)
            elif button_type == "S-E":
                super().__init__(style=discord.ButtonStyle.green,
                                 label=_T.stranslate(_ls(START)),
                                 row=row,
                                 custom_id=button_type)
            else:
                super().__init__(label="_", disabled=True, row=row)

        async def callback(self, interaction):
            await interaction.response.defer()
            view = self.view

            if interaction.user != view.user:
                return

            # Cursor move
            if self.custom_id == "8":
                view.field.move_cursor(0, -1)
            elif self.custom_id == "4":
                view.field.move_cursor(-1, 0)
            elif self.custom_id == "6":
                view.field.move_cursor(1, 0)
            elif self.custom_id == "2":
                view.field.move_cursor(0, 1)

            # Diagonal cursor move
            elif self.custom_id == "7":
                view.field.move_cursor(-1, -1)
            elif self.custom_id == "9":
                view.field.move_cursor(1, -1)
            elif self.custom_id == "1":
                view.field.move_cursor(-1, 1)
            elif self.custom_id == "3":
                view.field.move_cursor(1, 1)

            # Flip cell
            elif self.custom_id == "01":
                view.field.update()
            elif self.custom_id == "5":
                view.field.flip_cell()
            elif self.custom_id == "02":
                view.field.flip_cell(2)
            elif self.custom_id == "03":
                view.field.flip_cell(3)

            # Control
            elif self.custom_id == "S-E":
                if view.runing:
                    view.runing = False
                    self.label = (_T.stranslate(_ls(START)), _T.stranslate(_ls(STOP)))[view.runing]
                else:
                    view.runing = True
                    self.label = (_T.stranslate(_ls(START)), _T.stranslate(_ls(STOP)))[view.runing]
                    for child in view.children:
                        if child.custom_id in ("Q", "S-E"):
                            child.disabled = False
                        else:
                            child.disabled = True
                    while view.runing:
                        view.field.update()
                        content = view.render()
                        await interaction.edit_original_response(content=content, view=view)
                        await asyncio.sleep(1)
                    if not view.is_finished():
                        for child in view.children:
                            if child.label in (" ",):
                                child.disabled = True
                            else:
                                child.disabled = False
            elif self.custom_id == "Q":
                for child in view.children:
                    child.disabled = True
                view.runing = False
                view.stop()
            else:
                return

            content = view.render()
            await interaction.edit_original_response(content=content, view=view)
