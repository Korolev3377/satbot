import os
import json
import discord
import discord.ext.commands as commands
import discord.ext.tasks as tasks
	
TOKEN_PATH = os.environ.get("BOT_TOKEN")
TOKEN = None

with open(TOKEN_PATH, 'r') as file:
	TOKEN = file.read()

class quit_view(discord.ui.View):

	def __init__(self, user):
		super().__init__()
		self.user = user

	async def interaction_check(self, interaction):
		if interaction.type is discord.InteractionType.component:
			return interaction.user == self.user
		else:
			return False

	@discord.ui.button(style=discord.ButtonStyle.red, label="Yes")
	async def confirm(self, interaction,  button):
		for child in self.children:
			child.disabled = True
		button.label = '> '+button.label+' <'
		await interaction.response.edit_message(content="Bye :(", view=self)
		self.stop()
		# await interaction.guild.leave()

	@discord.ui.button(style=discord.ButtonStyle.grey, label="No")
	async def cancel(self, interaction, button):
		for child in self.children:
			child.disabled = True
		button.label = '> '+button.label+' <'
		await interaction.response.edit_message(content="Command cancelled", view=self)
		self.stop()

intents = discord.Intents.default()


class Bot(commands.Bot):
	def __init__(self, *, intents=intents):

		super().__init__(command_prefix=commands.when_mentioned_or(">_"), intents=intents)

	async def on_command_error(self, ctx, exception):
		await ctx.send(exception)

	async def setup_hook(self):
		await bot.tree.sync()

bot = Bot()

def is_guild(ctx):
	if ctx.guild is None:
		raise commands.CommandError("Error: Guild only command")
	else:
		return True
bot.add_check(is_guild)

@bot.event
async def on_ready():
	print(f"Name: {bot.user}\nID: {bot.user.id}")
	await check_battery.start()


@tasks.loop(minutes=5.0)
async def check_battery():
	try:
		battery = json.loads(os.popen("termux-battery-status").read())
		details = f"Battery {battery.get('status').lower()}: {battery.get('percentage')}% {round(battery.get('temperature'))}°C"

		activity = discord.Game(name=details)

	except:
		check_battery.cancel()
		details = f"Battery: Not detected"
		activity = discord.Game(name=details)

	await bot.change_presence(activity=activity)


def is_battery():
	if os.system("termux-battery-status") != 0:
		raise commands.CommandError("Error: Battery not detected")
	return True

@bot.hybrid_command(name="check_battery", description="Return current battery status")
async def chk_btr(ctx):
	await ctx.defer()
	is_battery()
	battery = json.loads(os.popen("termux-battery-status").read())
	details = f"""Battery status: {battery.get('status').lower().capitalize()}
Charge: {battery.get('percentage')}%
Temperature: {round(battery.get('temperature'))}°C"""
	await ctx.send(details)

@bot.hybrid_command(name="stop_checking_battery", description="Cancel check_battery task", check=is_battery)
async def stop_chk_btr(ctx):
	await ctx.defer()
	is_battery()
	if check_battery.is_running() is True:
		check_battery.cancel()
		await bot.change_presence(activity=None)
		await ctx.send("Checking battery stopped")
	else:
		await ctx.send("Already stopped")

@bot.hybrid_command(name="start_checking_battery", description="Starts check_battery task", check=is_battery)
async def start_chk_btr(ctx):
	await ctx.defer()
	is_battery()
	if check_battery.is_running() is False:
		check_battery.start()
		await ctx.send("Checking battery started")
	else:
		await ctx.send("Already started")


@bot.hybrid_command(name="quit", description="Kick bot from this guild")
async def quit(ctx):
	if ctx.permissions.administrator:
		await ctx.send("Are you sure want to kick me?", view=quit_view(ctx.author))
	else:
		raise commands.CommandError("Error: User permissions")


@bot.tree.context_menu(name="Delete your interaction")
async def del_int(interaction: discord.Interaction, message: discord.Message):
	if message.interaction:
		if message.interaction.user == interaction.user:
			await message.delete()
			await interaction.followup.delete()
		else:
			await interaction.response.send_message(
				"You can delete only the Interactions you have created",
				ephemeral=True)
	else:
		await interaction.response.send_message(
			"You can delete only the Interactions you have created",
			ephemeral=True)

bot.run(TOKEN)
