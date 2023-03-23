import discord
from discord.ext import commands
from discord.app_commands import locale_str as _ls

from commands.main import declare_cmds
from environment.main import Env, Cfg, Facts
from heart.heart import Heart
from translator.main import T

if __name__ == '__main__':
    class Bot(commands.Bot):
        def __init__(self):
            super().__init__(command_prefix=Cfg.CMD_PREFIX,
                             help_command=None,
                             strip_after_prefix=True,
                             intents=Cfg.INTENTS)
            self.antispam = {}  # Это ограничитель спама комманд для каждого пользователя.
            # Срабатывает при превышении лимита и отключается при понижении до 0.
            self.heart = Heart(self)
            # Это главный цикл бота. В нем идет пассивное уменьшение КД и проверка на то,
            # когда нужно будет менять Синего ника.

        async def setup_hook(self):
            self.tree.interaction_check = itr_check
            await self.tree.set_translator(T())  # Установка переводчика
            await self.tree.sync()  # Синхронизация. Для обновления изменения комманд


    BOT = Bot()
    _F = Facts()
    _T = T()


    async def itr_check(interaction: discord.Interaction):  # Проверка на возможность выполнения комманды
        _T.set_locale(interaction.locale)
        _user = interaction.user.id

        # Системные комманды могут вызываться без последствий
        if interaction.command.extras.get('system'):
            if BOT.antispam.get(_user):
                if BOT.antispam.get(_user).get('overload') > 100.0:
                    BOT.antispam[_user]['overloaded'] = True
            return True

        # Проверка на перегрузку
        if BOT.antispam.get(_user):
            if BOT.antispam.get(_user).get('overloaded'):
                _T.set_string(
                    _ls("on_cd",
                        extras={"format":
                            {"time_left": int(BOT.heart.time_to_cooldown(BOT.antispam.get(_user).get('overload')))}
                        }
                    )
                )
                await interaction.response.send_message(_T.stranslate(), ephemeral=False)
                return False

        # Проверка на отключенную комманду
        if interaction.command.extras.get("disabled"):
            _T.set_string(
                _ls("cmd_disabled")
            )
            await interaction.response.send_message(_T.stranslate(), ephemeral=False)
            return False

        # Предупреждение, что эта комманда сломана.
        if interaction.command.extras.get("broken"):
            _T.set_string(
                _ls("cmd_broken")
            )
            await interaction.response.send_message(_T.stranslate(), ephemeral=False)
            return False

        # Проверка на администратора сервера
        if not interaction.permissions.administrator and interaction.command.extras.get("admin_only"):
            if not await BOT.is_owner(interaction.user):
                _T.set_string(
                    _ls("cmd_adminonly")
                )
                await interaction.response.send_message(_T.stranslate(), ephemeral=False)
                return False

        # Проверка на создателя бота
        if not await BOT.is_owner(interaction.user) and interaction.command.extras.get("owner_only"):
            _T.set_string(
                _ls("cmd_owneronly")
            )
            await interaction.response.send_message(_T.stranslate(), ephemeral=False)
            return False

        if not BOT.antispam.get(_user):
            BOT.antispam[_user] = {
                'overload': 0,
                'overloaded': False
            }
        BOT.antispam[_user]['overload'] += BOT.antispam[_user]['overload']+20
        if BOT.antispam.get(_user).get('overload') > 100.0:
            BOT.antispam[_user]['overloaded'] = True
        return True


    @BOT.event
    async def on_ready():
        print('Бот запущен!\n')
        print(f"Имя: {BOT.user}\nИД: {BOT.user.id}")
        if translate_not_found := BOT.tree.translator.translate_not_found:
            print(f"\nПеревод не найден для: {translate_not_found}")
        await BOT.heart.beat.start()


    @BOT.event
    async def on_message(message):
        if message.author == BOT.user or message.author.bot:
            return

        msg = message.content.lower()

        if lang := _F.find_fact(msg=msg):
            if fact := await _F.read_facts(guild=message.guild, lang=lang):
                await message.channel.send(fact)

        """bot_mention = re.search(
            r"(\b8915-7\b|"
            r"\b872406824765251594\b|"
            r"\bбарменбот(а|у|ом|е|ы|ов|ам|ами|ах|о)?\b|"
            r"\bбармен(а|у|ом|е|ы|ов|ам|ами|ах|о)?\b|"
            r"\bфактобот(а|у|ом|е|ы|ов|ам|ами|ах|о)?\b"
            r"|\bббот\b|"
            r"\bbbot\b|"
            r"\bbarmen\b|"
            r"\bbartender\b|"
            r"\bbartenderbot\b)", msg)"""


    @BOT.event
    async def on_member_join(member: discord.Member):
        await member.guild.system_channel.send("{user} joined this Guild".format(user=member.mention))


    @BOT.event
    async def on_member_remove(member: discord.Member):
        await member.guild.system_channel.send("{user} left this Guild".format(user=member.mention))


    declare_cmds(BOT)
    BOT.run(Env.TOKEN)
