import os
import discord
import discord.ext.commands as commands
    
TOKEN = 'OTg4MzU2OTA4MTAyNTk0NTgy.GxtTas.sbH8GqVyDbG_M4T96cmOB8iZnCE1-U6QtbDPaI'

class quit_view(discord.ui.View):
    def __init__(self, user):
        super().__init__()
        self.user = user

    @discord.ui.button(style=discord.ButtonStyle.red, label='Да, уходи')
    async def confirm(self, interaction: discord.Interaction,
                      button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            await interaction.edit_original_response(content='Ладно, я уйду...',
                                                    view=None)
            self.stop()
            await interaction.guild.leave()

    @discord.ui.button(style=discord.ButtonStyle.grey, label='Нет, оставайся')
    async def cancel(self, interaction: discord.Interaction,
                     button: discord.ui.Button):
        await interaction.response.defer()
        if interaction.user == self.user:
            await interaction.edit_original_response(
                content='Хорошо, я останусь!', view=None)
            self.stop()


class TicTacToeButton(discord.ui.Button['TicTacToe']):
    def __init__(self, x: int, y: int):
        super().__init__(style=discord.ButtonStyle.secondary, label=' ', row=y)
        self.x = x
        self.y = y

    async def callback(self, interaction: discord.Interaction):
        global DEBUGUS
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
            if view.player_two:
                content = f"Крестики нолики: Ожидание хода {view.player_two.mention} :green_circle:"
            else:
                content = "Крестики нолики: Ожидание хода второго игрока :green_circle:"
        elif view.current_player == view.O and interaction.user == view.player_two and state not in (
                view.X, view.O):
            self.style = discord.ButtonStyle.green
            view.board[self.y][self.x] = view.O
            view.current_player = view.X
            if self.view.player_two:
                content = f"Крестики нолики: Ожидание хода {self.view.player_one.mention} :red_circle:"
            else:
                content = "Крестики нолики: Ожидание хода первого игрока :red_circle:"

        winner = view.check_board_winner()
        if winner is not None:
            if view.player_one == view.player_two:
                content = "Крестики нолики: Игра закончена"
            else:
                if winner == view.X:
                    content = f'Крестики нолики: Игра закончена\n{view.player_one.mention} :red_circle: побеждает!\n{view.player_two.mention} :green_circle: проигрывает!'
                elif winner == view.O:
                    content = f'Крестики нолики: Игра закончена\n{view.player_two.mention} :green_circle: побеждает!\n{view.player_one.mention} :red_circle: проигрывает!'
                else:
                    content = f'Крестики нолики: Игра закончена\nНичья между {self.view.player_one.mention} :red_circle: и :green_circle: {self.view.player_two.mention}!'

            for child in view.children:
                child.disabled = True

            view.stop()

        view.busy = False
        await interaction.edit_original_response(content=content, view=view)


class TicTacToe(discord.ui.View):
    busy = False
    player_one = None
    player_two = None
    X = -1
    O = 1
    Tie = 2

    def __init__(self):
        super().__init__()
        self.current_player = self.X
        self.board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]

        for x in range(3):
            for y in range(3):
                self.add_item(TicTacToeButton(x, y))

    def check_board_winner(self):

        # Check vertical
        for across in self.board:
            value = sum(across)
            if value == 3:
                return self.O
            elif value == -3:
                return self.X

        for line in range(3):
            value = self.board[0][line] + self.board[1][line] + self.board[2][
                line]
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


intents = discord.Intents.default()


class Bot(commands.Bot):
    def __init__(self, *, intents=intents):
        super().__init__(command_prefix=commands.when_mentioned_or('!'),
                         intents=intents)

    async def setup_hook(self):
        await bot.tree.sync()


bot = Bot()


@bot.check
def check(ctx):
    return False if ctx.guild is None else True


@bot.event
async def on_ready():
    print(f'Запущено под именем {bot.user} (ID: {bot.user.id})')


@bot.tree.command(name='ttt', description='Играть в крестики нолики')
async def ttt(interaction: discord.Interaction):
    await interaction.response.send_message(
        f'Крестики нолики: Ожидание хода первого игрока :red_circle:',
        view=TicTacToe())


@bot.tree.command(name='quit', description='Выгнать бота')
async def quit(interaction: discord.Interaction):
    if interaction.user.guild_permissions.administrator or interaction.user.id == 400989403482423296:
        await interaction.response.send_message(
            'Ты действительно хочешь меня выгнать?',
            view=quit_view(interaction.user))
    else:
        await interaction.response.send_message(
            f'Я протестую, {interaction.user.mention}!')


@bot.tree.context_menu(name='Delete Interaction')
async def del_msg(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.defer(ephemeral=True, thinking=True)
    if message.interaction:
        if message.interaction.user == interaction.user:
            await message.delete()
            await interaction.followup.send('Сообщение успешно удалено.',
                                            ephemeral=True)
        else:
            await interaction.followup.send(
                'Вы можете удалять только те сообщения, которые вы создали взаимодействуя со мной.',
                ephemeral=True)
    else:
        await interaction.followup.send(
            'Вы можете удалять только те сообщения, которые вы создали взаимодействуя со мной.',
            ephemeral=True)


bot.run(TOKEN)
