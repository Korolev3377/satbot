import discord
from discord.ext import commands
import time
import asyncio
import random


class Nickblue:
    BOT = None  # Для работы с дисководом
    enable = 0  # 0  # Работает?
    runing = 0  # 1  # Ник выбран?
    guild = None  # Сервер где рулетка
    channel = None  # 2  # Канал для сообщение о новом нике
    role = None  # Роль синего ника
    current = None  # 3  # Текущий Синий ник
    timer = None  # 4  # Таймер
    candidates = []  # 5  # Список кандидатов на роль
    non_candidates = []  # 6  # Список последних синих ников
    op_channel = None  # Канал для хранения информации о рулетке

    def __init__(self, bot: commands.Bot = None, guild_id: int = None, channel_id: int = None, role_id: int = None,
                 op_channel_id: int = None):
        self.BOT = bot
        self.guild_id = guild_id
        self.channel_id = channel_id
        self.role_id = role_id
        self.op_channel_id = op_channel_id
        self.time_left = 0

    def data_pack(self):
        if self.current:
            current = self.current.id
        else:
            current = 0
        return f'{self.enable}; {self.runing}; {self.channel_id}; {current}; {self.time_left}; {" ".join(map(str, self.candidates)) or 0}; {" ".join(map(str, self.non_candidates)) or 0}'

    async def data_unpack(self, data):
        nb_list = str.split(data, '; ')  # Делим последнее сообщение на части
        self.enable = int(nb_list[0])  # 0
        self.runing = int(nb_list[1])  # 1
        self.channel = self.guild.get_channel_or_thread(int(nb_list[2]))  # 2
        if int(nb_list[3]) != 0:  # 3
            self.current = self.guild.get_member(int(nb_list[3]))
        self.timer = int(nb_list[4])  # 4
        if len(nb_list) > 5:
            for member in str.split(nb_list[5], ' '):  # 5
                if int(member) not in self.candidates:
                    self.candidates.append(int(member))
        if len(nb_list) > 6:
            if nb_list[6] != '0':
                for member in str.split(nb_list[6], ' '):  # 6
                    if int(member) not in self.non_candidates:
                        self.non_candidates.append(int(member))

    async def init(self):
        self.guild: discord.Guild = await self.BOT.fetch_guild(self.guild_id)
        self.role: discord.Role = self.guild.get_role(self.role_id)
        self.op_channel: discord.TextChannel = await self.BOT.fetch_channel(self.op_channel_id)

        op_channel_last_msg: discord.Message = await self.op_channel.fetch_message(self.op_channel.last_message_id)
        if op_channel_last_msg.content != 'STOP':  # Если в канале оператора последнее сообщение не STOP, то
            await self.data_unpack(op_channel_last_msg.content)
            await op_channel_last_msg.add_reaction('♻')  # Хорошо
            try:  # Проверка на правильность цвета роли
                if self.role:
                    if self.role.colour != 0x87CEEB:
                        await self.role.edit(colour=0x87CEEB, reason='Цвет должен быть синим')
            except:
                print(f'{BBOT.user.name}: Ошибка при попытке взаимодействия с ролью')
        else:
            await op_channel_last_msg.add_reaction('⛔')  # Остановка рулетки

    async def roll(self):  # Боль
        if self.enable and not self.runing:  # Нужно ли крутить рулетку
            if not self.current:  # Если Ник не выбран
                if len(self.candidates) > 1:  # Если список кандидатов больше 1
                    randomnick = random.choice(self.candidates)
                    async for mem in self.guild.fetch_members():
                        if mem.id == randomnick:
                            self.current = await self.guild.fetch_member(randomnick)  # Рандомыный выбор Ника
                    if not self.current:
                        self.candidates.remove(randomnick)
                    if self.role:
                        for member in self.role.members:
                            await member.remove_roles(self.role)  # Убирает лишнии роли
                        await self.current.add_roles(self.role,
                                                     reason='Присваивание роли из-за получения статуса Nick_Blue')
                    self.timer = int(time.time()) + 200  # 87600  # 24 часа и 20 минут
                    rounded_time = self.timer % 1200  # Каждые 20 минут
                    self.time_left = self.timer - rounded_time
                    if not self.channel:
                        self.channel = await self.guild.fetch_channel(self.channel_id)
                    async with self.channel.typing():  # Сообщение о смене Ника
                        await asyncio.sleep(1)
                        await self.channel.send(
                            f'''{self.current.mention} is now **Nick_Blue** until <t:{self.timer}>.
Congratulations! I hope we can all move on with our lives now.
{self.current.mention} теперь **Nick_Blue** до <t:{self.timer}>.
Поздравляю! Надеюсь, теперь мы все сможем вернуться к привычной жизни.
# ------ # ------ # ------ # ------ #''')
                    self.runing = 1  # Ник выбран
                    await self.op_channel.send(self.data_pack())  # Отправка информации в канал операторов
                elif len(self.non_candidates) > 1:  # Если бывших кандидатов больше 1
                    while len(self.candidates) < 5:  # Пока текущих кандидатов меньше 5
                        r = random.choice(self.non_candidates)  # Выбрать рандомного человека из списка бывших
                        self.candidates.append(r)
                        self.non_candidates.remove(r)  # Перемещяет челика из в список текущих
                else:  # Мало кандидатов
                    async with self.channel.typing():
                        await asyncio.sleep(1)
                        await self.channel.send(f'''Not enough candidates for the raffle. Should be at least two!
            Недостаточно участников для лотереи. Нужно хотя бы двое!''')
                    await self.op_channel.send('STOP')
                    self.enable = 0
                    return  # Выключение

    async def rolled(self):
        if self.role and self.current:
            await self.current.remove_roles(self.role, reason='Удаление роли из-за утраты статуса Nick_Blue')
        async with self.channel.typing():
            await asyncio.sleep(1)
            await self.channel.send(f'''# ------ # ------ # ------ # ------ #
{self.current.mention} is no longer **Nick_Blue**...
{self.current.mention} больше не **Nick_Blue**...''')
        if len(self.candidates) > 5:  # Если кандидатов большьше 5
            if self.current.id in self.candidates:
                self.non_candidates.append(self.current.id)
                self.candidates.remove(self.current.id)  # перемещение выбранного Ника в список бывших
        elif len(self.candidates) == 5:  # Если кандидатов 5
            if self.current.id in self.candidates:
                self.non_candidates.append(self.current.id)
                self.candidates.remove(self.current.id)
                if len(self.non_candidates) > 0:
                    self.candidates.append(self.non_candidates.pop(0))
        elif len(self.candidates) < 5:  # Если кандидатов меньше 5
            if self.current.id in self.candidates:
                self.non_candidates.append(self.current.id)
                self.candidates.remove(self.current.id)
            if len(self.non_candidates) > 0:
                while len(self.candidates) < 5 and len(self.non_candidates) > 0:
                    self.candidates.append(self.non_candidates.pop(0))
        self.current = None
        self.runing = 0
        if self.enable == 0:
            await self.op_channel.send('STOP')
        else:
            await self.op_channel.send(self.data_pack())
        await self.roll()

    async def add_candidate(self, mem_id, lang):
        if mem_id not in self.candidates and mem_id not in self.non_candidates:
            self.non_candidates.append(mem_id)
            await self.op_channel.send(self.data_pack())
            if lang == 'ru':
                return f'''Ты присоединился к лотерее **Nick_Blue** , смельчак!
Текущее количество участников: {len(self.candidates) + len(self.non_candidates)}'''
            else:
                return f'''You left the **Nick_Blue** raffle. I'm sorry to see you go. You made me sad. How could you?
Number of remaining participants: {len(self.candidates) + len(self.non_candidates)}'''
        else:
            if lang == 'ru':
                return '''Ты уже записан в лотерею **Nick_Blue**. Ты что, хочешь сбить меня с толку?
Чтобы покинуть лотерею, скажи \"8915-7, не играть\"'''
            else:
                return '''You're not participating in the **Nick_Blue** raffle. Why?
To join, say \"8915-7, join\"'''

    async def remove_candidate(self, mem_id, lang):
        if mem_id in self.candidates or mem_id in self.non_candidates:
            if mem_id in self.candidates:
                self.candidates.remove(mem_id)
            if mem_id in self.non_candidates:
                self.non_candidates.remove(mem_id)
            await self.op_channel.send(self.data_pack())
            if lang == 'ru':
                return f'''Вы покинули лотерею **Nick_Blue**. Мне жаль, что ты это сделал. Теперь мне грустно. Как ты мог?
Количество оставшихся участников: {len(self.candidates) + len(self.non_candidates)}'''
            else:
                return f'''You left the **Nick_Blue** raffle. I'm sorry to see you go. You made me sad. How could you?
Number of remaining participants: {len(self.candidates) + len(self.non_candidates)}'''
        else:
            if lang == 'ru':
                return '''Вы не учавствуете в лотерее **Nick_Blue**. Но... почему?
Чтобы присоединиться к лотерее, скажи \"8915-7, играть\"'''
            else:
                return '''You're not participating in the **Nick_Blue** raffle. Why?
To join, say \"8915-7, join\"'''

    async def show_candidates(self, lang):
        if self.current:
            diff = self.timer - int(time.time())
            hours = diff // 3600
            minutes = diff // 60 % 60
            seconds = diff % 60
            if len(self.candidates) > 0:
                t = []
                for member in self.candidates:
                    usr = await self.BOT.fetch_user(member)
                    t.append(usr.name)
                for member in self.non_candidates:
                    usr = await self.BOT.fetch_user(member)
                    t.append(usr.name)
                random.shuffle(t)
                if lang == 'ru':
                    candidates_list = f'Список участников лотереи **Nick_Blue** ({len(self.candidates) + len(self.non_candidates)}): {str.join(", ", t)}'
                else:
                    candidates_list = f'List of participants in the **Nick_Blue** raffle ({len(self.current.candidates) + len(self.non_candidates)}): {str.join(", ", t)}'
            else:
                if lang == 'ru':
                    candidates_list = '''Похоже, в лотерее Nick_Blue пока никто не участвует.
Ты можешь быть первым!
Ты также можешь оказаться единственным, выйдет неловко.
Чтобы присоединиться, скажи: "8915-7, играть"'''
                else:
                    candidates_list = '''There are no participants in today's **Nick_Blue** raffle.
You may be the first!
You may also turn out to be the only one, that'd be awkward.
To join, say \"8915-7, join\"'''
            if diff > 0:
                if lang == 'ru':
                    return f'''{self.current.name} - **Nick_Blue** до <t:{self.timer}>
Оставшееся время - {hours}ч {minutes}м {seconds}с
{candidates_list}'''
                else:
                    return f'''{self.current.name} is **Nick_Blue** until <t:{self.timer}>
Remaining time - {hours} hours {minutes} minutes {seconds} seconds
{candidates_list}'''
            else:
                return f'''{self.current.name} - **Nick_Blue**
{candidates_list}'''
        else:
            if lang == 'ru':
                return '**Nick_Blue** еще не был разыгран!'
            else:
                return '**Nick_Blue** hasn\'t been raffled yet!'
