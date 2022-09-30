from discord import app_commands
from .brainfuck import bf_cmd
from .tictactoe import tictactoe_cmd
from .gameoflife import gol_cmd

class FunGroup:
    def __init__(self, BOT):
        BOT.tree.add_command(bf_cmd)
        BOT.tree.add_command(tictactoe_cmd)
        BOT.tree.add_command(gol_cmd)
