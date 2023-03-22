import asyncio

import discord
from discord import app_commands

from discord.app_commands import locale_str as _ls
from Bot.translator import Translator

locale = {"p1_wait": {"en": "Tic Tac Toe: Waiting for player {player1} :red_circle:",
                      "ru": "Крестики Нолики: Ожидание игрока {player1} :red_circle:"},

          "p2_wait": {"en": "Tic Tac Toe: Waiting for player {player2} :green_circle:",
                      "ru": "Крестики Нолики: Ожидание игрока {player2} :green_circle:"},

          "p1_win": {
              "en": "Tic Tac Toe: Game over\n{player1} :red_circle: Won!\n{player2} :green_circle: Loses!",
              "ru": "Крестики Нолики: Игра окончена\n{player1} :red_circle: Побеждает!\n{player2} :green_circle: Проигрывает!"},

          "p2_win": {
              "en": "Tic Tac Toe: Game over\nPlayer {player2} :green_circle: Won!\nPlayer {player1} :red_circle: Loses!",
              "ru": "Крестики Нолики: Игра окончена\nИгрок {player2} :green_circle: Побеждает!\nИгрок {player1} :red_circle: Проигрывает!"},

          "draw": {
              "en": "Tic Tac Toe: Game over\nDraw between\nPlayer {player1} :red_circle:\n&\nPlayer  {player2} :green_circle:!",
              "ru": "Крестики Нолики: Игра окончена\nНичья между\nИгроком {player1} :red_circle:\n&\nИгроком {player2} :green_circle:!"},

          "gameover": {"en": "Tic Tac Toe: Game over",
                       "ru": "Крестики Нолики: Игра окончена"}
          }

T = Translator(locale_dict=locale)

@app_commands.command(name="ttt_n", description="ttt_d")
async def tictactoe_cmd(interaction: discord.Interaction):
    await interaction.response.defer()
    lang = interaction.locale
    await interaction.followup.send(T.soft_translate(string=_ls("p1_wait", extras={"format": {"player1": "1"}}), locale=lang), view=TicTacToeView(lang))


class TicTacToeView(discord.ui.View):
    busy = False
    player_one = None
    player_two = None
    X = -1
    O = 1
    Tie = 2

    def __init__(self, lang):
        super().__init__()
        self.lang = lang
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(self.TicTacToeButton(x, y))

    def check_board_winner(self):

        # Check horizontal
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.O
        elif diag == -3:
            return self.X

        # Check Tie
        if all(i != 0 for row in self.board for i in row):
            return self.Tie

        return None

    class TicTacToeButton(discord.ui.Button):
        def __init__(self, x: int, y: int):
            super().__init__(label='_', row=y)
            self.x = x
            self.y = y

        async def callback(self, interaction: discord.Interaction):
            await interaction.response.defer()
            view = self.view
            state = view.board[self.y][self.x]
            content = interaction.message.content

            if view.busy:
                return
            view.busy = True

            if view.player_one is None:
                view.player_one = interaction.user
            elif view.player_two is None:
                view.player_two = interaction.user

            if view.current_player == view.X and interaction.user == view.player_one and state not in (
                    view.X, view.O):
                self.style = discord.ButtonStyle.red
                view.board[self.y][self.x] = view.X
                view.current_player = view.O
                if self.view.player_two:
                    content = T.soft_translate(string=_ls("p2_wait", extras={"format": {"player2": self.view.player_two.mention}}), locale=view.lang)
                else:
                    content = T.soft_translate(string=_ls("p2_wait", extras={"format": {"player2": "2"}}), locale=view.lang)
            elif view.current_player == view.O and interaction.user == view.player_two and state not in (
                    view.X, view.O):
                self.style = discord.ButtonStyle.green
                view.board[self.y][self.x] = view.O
                view.current_player = view.X
                if self.view.player_two:
                    content = T.soft_translate(string=_ls("p1_wait", extras={"format": {"player1": self.view.player_one.mention}}), locale=view.lang)
                else:
                    content = T.soft_translate(string=_ls("p1_wait", extras={"format": {"player1": "1"}}), locale=view.lang)

            winner = view.check_board_winner()
            if winner is not None:
                if view.player_one == view.player_two:
                    content = T.soft_translate(string=_ls("gameover"), locale=view.lang)
                else:
                    if winner == view.X:
                        content = T.soft_translate(string=_ls("p1_win", extras={"format": {"player1": self.view.player_one.mention, "player2": self.view.player_two.mention}}), locale=view.lang)
                    elif winner == view.O:
                        content = T.soft_translate(string=_ls("p2_win", extras={"format": {"player1": self.view.player_one.mention, "player2": self.view.player_two.mention}}), locale=view.lang)
                    else:
                        content = T.soft_translate(string=_ls("draw", extras={"format": {"player1": self.view.player_one.mention, "player2": self.view.player_two.mention}}), locale=view.lang)

                for child in view.children:
                    child.disabled = True

                view.stop()

            await interaction.edit_original_response(content=content, view=view)
            await asyncio.sleep(1)
            view.busy = False
