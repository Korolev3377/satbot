import os, json
import discord
from discord.ext import commands, tasks

import cmds

TOKEN_PATH = os.environ.get("BOT_TOKEN")
TOKEN = None

with open(TOKEN_PATH, 'r') as file:
	TOKEN = file.read()

class Bot(commands.Bot):
	def __init__(self):
		super().__init__(command_prefix=commands.when_mentioned_or(">_"), strip_after_prefix=True, intents=discord.Intents.all())

	#async def on_command_error(self, ctx, exception):
	#	await ctx.send(exception)

bot = Bot()

@tasks.loop(minutes=1.0)
async def check_battery():
	if os.popen("uname -o").read() == "Android\n":
		battery = json.loads(os.popen("termux-battery-status").read())
		
		details = f"Battery {battery.get('status').lower()}: {battery.get('percentage')}% {round(battery.get('temperature'))}°C"
		
		activity = discord.Game(name=details)
	else:
		check_battery.cancel()
		details = f"Battery: Not detected"
		activity = discord.Game(name=details)
		
	await bot.change_presence(activity=activity)

cmds.load_globals(bot=bot, task=check_battery)

quit = cmds.Quit()
tictactoe = cmds.TicTacToe()
battery = cmds.Battery()

bot.add_command(quit.quit)
bot.add_command(tictactoe.ttt)
bot.add_command(battery.battery)

@bot.check
def is_guild(ctx):
	if ctx.guild is None:
		raise commands.CommandError("Error: Guild only command")
	else:
		return True

@bot.event
async def on_ready():
	print(f"Name: {bot.user}\nID: {bot.user.id}")
	await check_battery.start()

@bot.tree.context_menu(name="Delete your interaction")
async def del_int(interaction, message: discord.Message):
    await interaction.response.defer(ephemeral=True, thinking=True)
    if message.interaction:
        if message.interaction.user == interaction.user:
            await message.delete()
            await interaction.followup.send("Deleted successfully", ephemeral=True)
        else:
            await interaction.followup.send("You can delete only the Interactions you have created", ephemeral=True)
    else:
        await interaction.followup.send("You can delete only the Interactions you have created", ephemeral=True)

bot.run(TOKEN)
