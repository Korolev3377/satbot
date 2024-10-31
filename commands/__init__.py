import discord.abc

from commands.admin import admingrp
from .regular import facts, cults, rolldice, facts_ignore, facts_count
from .fun import fungrp
from .wealth import wealthgrp, wealthopagrp
from .shop import shopgrp
from environment.variable import *

COMMANDS_DICT = {
    "facts": facts,
    "facts_ignore": facts_ignore,
    "facts_count": facts_count,
    "cults": cults,
    "rolldice": rolldice,
    "fungrp": fungrp,
    "wealthgrp": wealthgrp,
    "wealthopagrp": wealthopagrp
}

async def declare_commands(bot):
    bot.logger.info("Запущено обновление команд.")
    async for g in bot.fetch_guilds():  # Загрузка конфига комманд для каждого сервера. И настройка конфигов пересылки сообщений...
        bot.logger.info(["g", g.id])
        status_d2t_0, _ = check_config(bot.guilds_data, [str(g.id), "discord2tg_bridge", "enable_d2t"])
        status_d2t_1, _ = check_config(bot.guilds_data, [str(g.id), "discord2tg_bridge", "enable_from_tg"])
        status_d2t_2, _ = check_config(bot.guilds_data, [str(g.id), "discord2tg_bridge", "from_tg"])
        if status_d2t_0 and status_d2t_1 and status_d2t_2:
            if bot.guilds_data.get(str(g.id)).get("discord2tg_bridge", "enable_d2t"):
                if bot.guilds_data.get(str(g.id)).get("discord2tg_bridge", "enable_from_tg"):
                    mfilter = bot.guilds_data.get(str(g.id)).get("discord2tg_bridge").get("from_tg").split(" ")
                    # mfilter == ["1090104010005050103:-1000202090908+2060", "1090104010005050103:-1000202090908+2060"]
                    for mf in mfilter:
                        bot.guilds_data[str(mf.split(":")[1].split("+")[0])] = {str(mf.split(":")[1].split("+")[1]): str(mf.split(":")[0])}

        bot.tree.clear_commands(guild=g)
        bot.tree.add_command(admingrp, guild=g)
        for k, v in COMMANDS_DICT.items():
            status, code = check_config(bot.guilds_data, [str(g.id), "commands_to_declare", k])
            codes = {
                0: f"Ошибка в конфигурации сервера \"{g.name}\": Нету конфигурации для сервера.",
                1: f"Ошибка в конфигурации сервера \"{g.name}\": Не найден \"commands_to_declare\" в конфигурации сервера.",
                2: f"Ошибка в конфигурации сервера \"{g.name}\": Отсутствует \"{k}\" в \"commands_to_declare\""
            }
            if status:
                if bot.guilds_data.get(str(g.id)).get("commands_to_declare").get(k):
                    bot.tree.add_command(v, guild=g)
            else:
                bot.logger.error(codes.get(code))
        await bot.tree.sync(guild=g)  # Синхронизация. Для обновления изменения комманд
    await bot.tree.sync()
    bot.logger.info("Обновление команд завершено.")
