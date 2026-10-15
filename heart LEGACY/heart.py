import time

from discord.ext import tasks

loop_seconds = 1.0
cooling_rate = 1/1.2


class Heart:
    cycle = 0
    step_cycle = 1
    end_cycle = 0

    def __init__(self, bot):
        self.BOT = bot

    def time_to_cooldown(self, overload):
        return (overload / cooling_rate) * loop_seconds

    @tasks.loop(seconds=loop_seconds, reconnect=False)
    async def beat(self):
        """if self.BOT.nickblue.enable:
            if time.time() > self.BOT.nickblue.time_left:  # Идемя Врет
                await self.BOT.nickblue.rolled()"""
        for _id, _user in dict(self.BOT.antispam).items():
            if _user.get('overload') > 0:  # Пассивное охлаждение
                _user['overload'] -= cooling_rate
            if _user.get('overload') < 0:
                _user['overload'] = 0
            if _user.get('overload') > 100:
                _user['overloaded'] = True
                _user['overload'] = 100
            if _user.get('overload') == 0:
                self.BOT.antispam.pop(_id)
        self.cycle += cooling_rate/10000
        if self.cycle >= self.end_cycle:
            self.end_cycle += self.step_cycle
            self.BOT.logger.info(f'Цикл: {round(self.cycle)}')

    @beat.before_loop
    async def before_loop(self):
        self.BOT.logger.info('Сердце запущено!')

    @beat.after_loop
    async def after_loop(self):
        self.BOT.logger.critical("Сердце остановлено!")
