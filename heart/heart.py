import time

from discord.ext import tasks

loop_seconds = 1.0
cooling_rate = 1/1.2


class Heart:
    cycle = 0

    def __init__(self, bot):
        self.bot = bot

    def time_to_cooldown(self, overload):
        return (overload / cooling_rate) * loop_seconds

    @tasks.loop(seconds=loop_seconds)
    async def beat(self):
        """if self.BOT.nickblue.enable:
            if time.time() > self.BOT.nickblue.time_left:  # Идемя Врет
                await self.BOT.nickblue.rolled()"""
        for _id, _user in dict(self.bot.antispam).items():
            if _user.get('overload') > 0:  # Пассивное охлаждение
                _user['overload'] -= cooling_rate
            if _user.get('overload') < 0:
                _user['overload'] = 0
            if _user.get('overload') > 100:
                _user['overloaded'] = True
            if _user.get('overload') == 0:
                self.bot.antispam.pop(_id)
        self.cycle += cooling_rate/100

    @beat.before_loop
    async def before_loop(self):
        print('\nКонец инициализации!')
