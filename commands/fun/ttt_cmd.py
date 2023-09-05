import asyncio

import discord
from discord import app_commands

from discord.app_commands import locale_str as _ls
from translator.__init__ import T
from environment.variable import *

TTT_DESC = "ttt_desc"

TTT_NAME = 'ttt_name'

PLAYER1_TURN = "p1_wait"
PLAYER2_TURN = "p2_wait"
PLAYER1_WIN = "p1_win"
PLAYER2_WIN = "p2_win"
DRAW = "draw"
GAMEOVER = "gameover"

_locale = {
    TTT_NAME: {
        EN: 'tic-tac-toe',
        RU: 'крестики-нолики'
    },
    TTT_DESC: {
        EN: 'Create a Tic-tac-toe field',
        RU: 'Создать поле для крестиков-ноликов'
    },

    PLAYER1_TURN: {EN: "Tic Tac Toe: Waiting for player {player1} :red_circle:",
                   RU: "Крестики Нолики: Ожидание игрока {player1} :red_circle:"},

    PLAYER2_TURN: {EN: "Tic Tac Toe: Waiting for player {player2} :green_circle:",
                   RU: "Крестики Нолики: Ожидание игрока {player2} :green_circle:"},

    PLAYER1_WIN: {
        EN: "Tic Tac Toe: Game over\n"
            "{player1} :red_circle: Won!\n"
            "{player2} :green_circle: Lost!",
        RU: "Крестики Нолики: Игра окончена\n"
            "{player1} :red_circle: Победил!\n"
            "{player2} :green_circle: Проиграл!"},

    PLAYER2_WIN: {
        EN: "Tic Tac Toe: Game over\n"
            "Player {player2} :green_circle: Won!\n"
            "Player {player1} :red_circle: Lost!",
        RU: "Крестики Нолики: Игра окончена\n"
            "Игрок {player2} :green_circle: Победил!\n"
            "Игрок {player1} :red_circle: Проиграл!"},

    DRAW: {
        EN: "Tic Tac Toe: Game over\n"
            "Draw between\n"
            "Player {player1} :red_circle:\n"
            "&\n"
            "Player  {player2} :green_circle:!",
        RU: "Крестики Нолики: Игра окончена\n"
            "Ничья между\n"
            "Игроком {player1} :red_circle:\n"
            "&\n"
            "Игроком {player2} :green_circle:!"},

    GAMEOVER: {EN: "Tic Tac Toe: Game over",
               RU: "Крестики Нолики: Игра окончена"}
}

_T = T(locale_dict=_locale)


@app_commands.command(
    name=namedesc(TTT_NAME, _locale),
    description=namedesc(TTT_DESC, _locale)
)
async def tictactoe(interaction: discord.Interaction):
    await interaction.response.defer()
    _T.set_language(interaction.locale)
    _T.set_string(
        _ls(
            PLAYER1_TURN,
            extras={
                FORMAT: {
                    "player1": "1"
                }
            }
        )
    )
    await interaction.followup.send(_T.stranslate(), view=TicTacToeView())


class TicTacToeView(discord.ui.View):
    busy = False
    player_one = None
    player_two = None
    tic = -1
    tac = 1
    toe = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.tic
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
                return self.tac
            elif value == -3:
                return self.tic

        # Check vertical
        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][line]
            if value == 3:
                return self.tac
            elif value == -3:
                return self.tic

        # Check diagonals
        diag = self.board[0][2] + self.board[1][1] + self.board[2][0]
        if diag == 3:
            return self.tac
        elif diag == -3:
            return self.tic

        diag = self.board[0][0] + self.board[1][1] + self.board[2][2]
        if diag == 3:
            return self.tac
        elif diag == -3:
            return self.tic

        # Check Tie
        if all(i != 0 for row in self.board for i in row):
            return self.toe

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

            if view.current_player == view.tic and interaction.user == view.player_one and state not in (
                    view.tic, view.tac):
                self.style = discord.ButtonStyle.red
                view.board[self.y][self.x] = view.tic
                view.current_player = view.tac
                if self.view.player_two:
                    _T.set_string(
                        _ls(
                            PLAYER2_TURN,
                            extras={
                                FORMAT: {
                                    "player2": self.view.player_two.mention
                                }
                            }
                        )
                    )

                else:
                    _T.set_string(
                        _ls(
                            PLAYER2_TURN,
                            extras={
                                FORMAT: {
                                    "player2": "2"
                                }
                            }
                        )
                    )
                content = _T.stranslate()
            elif view.current_player == view.tac and interaction.user == view.player_two and state not in (
                    view.tic, view.tac):
                self.style = discord.ButtonStyle.green
                view.board[self.y][self.x] = view.tac
                view.current_player = view.tic
                if self.view.player_two:
                    _T.set_string(
                        _ls(
                            PLAYER1_TURN,
                            extras={
                                FORMAT: {
                                    "player1": self.view.player_one.mention
                                }
                            }
                        )
                    )
                else:
                    _T.set_string(
                        _ls(
                            PLAYER1_TURN,
                            extras={
                                FORMAT: {
                                    "player1": "1"
                                }
                            }
                        )
                    )
                content = _T.stranslate()

            winner = view.check_board_winner()
            if winner is not None:
                if view.player_one == view.player_two:
                    _T.set_string(
                        _ls(
                            GAMEOVER
                        )
                    )
                else:
                    if winner == view.tic:
                        _T.set_string(
                            _ls(
                                PLAYER1_WIN,
                                extras={
                                    FORMAT: {
                                        "player1": self.view.player_one.mention,
                                        "player2": self.view.player_two.mention
                                    }
                                }
                            )
                        )
                    elif winner == view.tac:
                        _T.set_string(
                            _ls(
                                PLAYER2_WIN,
                                extras={
                                    FORMAT: {
                                        "player1": self.view.player_one.mention,
                                        "player2": self.view.player_two.mention}
                                }
                            )
                        )
                    else:
                        _T.set_string(
                            _ls(
                                DRAW,
                                extras={
                                    FORMAT: {
                                        "player1": self.view.player_one.mention,
                                        "player2": self.view.player_two.mention
                                    }
                                }
                            )
                        )
                content = _T.stranslate()

                for child in view.children:
                    child.disabled = True

                view.stop()

            await interaction.edit_original_response(content=content, view=view)
            await asyncio.sleep(1)
            view.busy = False
