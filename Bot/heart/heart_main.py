import time

from discord.ext import tasks

loop_seconds = 30.0
cooling_rate = 0.5

class Heart:
    def __init__(self, BOT):
        self.BOT = BOT

    def time_to_cooldown(self):
        return (self.BOT.overload / cooling_rate) * loop_seconds

    @tasks.loop(seconds=loop_seconds)
    async def heartbeat(self):
        if self.BOT.nickblue.enable:
            if time.time() > self.BOT.nickblue.time_left:  # Идемя Врет
                await self.BOT.nickblue.rolled()
        if self.BOT.overload > 0:  # Пассивное охлаждение
            self.BOT.overload -= cooling_rate

    @heartbeat.before_loop
    async def before_loop(self):
        print('Сердце запущено!')
        print('\nКонец инициализации!')
