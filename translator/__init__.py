from discord import app_commands
from environment.variable import *


class T(app_commands.Translator):
    def __init__(self, locale_dict=None, bot=None):
        super().__init__()
        self.language = None
        self.string = None
        self.translate_not_found = set()
        self.bot = bot
        if locale_dict:
            self.locale_dict = locale_dict
        else:
            self.locale_dict = {
                ERROR: {EN: "Oops, something went wrong!",
                        RU: "Ой-ей. Что-то пошло не так!"},

                IS_BROKEN: {EN: "I'm sorry. This command is broken! :(",
                            RU: "Простите. Эта команда сломана! :("},

                IS_DISABLED: {EN: "I'm sorry. This command is disabled! :(",
                              RU: "Простите. Эта команда отключена! :("},

                IS_ADMIN_ONLY: {EN: "I'm sorry. This command is for admins only! :(",
                                RU: "Простите. Эта команда только для администраторов! :("},

                IS_OWNER_ONLY: {EN: "I'm sorry. This command very unstable! Usage prohibited. :(",
                                RU: "Простите. Эта команда очень нестабильна! Использование запрещено. :("},

                IS_DM_ALLOWED: {EN: "I'm sorry. Most commands cannot be used in private messages. :(",
                                RU: "Простите. Большенство команд невозможно использовать в личных сообщениях. :("},

                ON_COOLDOWN: {
                    EN: "Whoa, you're overloading my fragile circuits... "
                        "Please wait {time} seconds before making this request again.",
                    RU: "Оу, ты так мне цепи перегрузишь... "
                        "Подожди, пожалуйста, {time} секунд, прежде чем спрашивать меня об этом снова."},

                "…": {"en": "...",
                      "ru": "..."}
            }

        self.inverted_locale_dict = {}
        for translate_name, translate_dict in self.locale_dict.items():
            for translate in translate_dict.values():
                self.inverted_locale_dict[translate] = translate_name

    def get_lang(self, locale_value):
        if locale_value in ("ru", "uk"):  # Проверка на руссоподобную принадлежность локализации дискорда
            lang = "ru"
        else:  # Если перевода не предусмотренно
            lang = "en"  # Стандартный язык перевода (он всегда должен быть в словаре)
        return lang

    def set_language(self, language):
        self.language = language

    def set_string(self, string):
        self.string = string

    def stranslate(self, st=None, ln=None):
        if st:
            string = st
        else:
            string = self.string

        try:
            if ln:
                ln = ln.value
            elif self.language:
                ln = self.language.value
            else:
                ln = discord.Locale.american_english.value
        except:
            if ln:
                ln = ln
            elif self.language:
                ln = self.language
            else:
                ln = discord.Locale.american_english
        finally:
            ln = self.get_lang(ln)

        if self.locale_dict:
            result = self.locale_dict.get(string.message)  # Наименование, которое нужно перевести
            if not result:  # Если не удалось найти наименование в словаре перевода
                self.translate_not_found.add(string.message)
                return string.message

            result = result.get(ln)  # Получение перевода из locale_dict
            if not result:
                return string.message

            if string.extras:  # Проверка format (значение, которое нужно вставить в текст)
                if format_dict := string.extras[EXTRAS].get(FORMAT):
                    result = result.format(**format_dict)

            return result
        else:
            self.translate_not_found.add(string.message)
            return string.message

    async def translate(self,
                        string,
                        locale,
                        context=None) -> str:  # Язык клиента дискорда
        if string.extras.get(EXTRAS):
            if string.extras.get(EXTRAS).get(TYPE) == CMD:
                try:
                    return string.extras.get(EXTRAS).get(DICT).get(self.get_lang(locale.value))
                except:
                    self.bot.logger.error(f"Ошибка перевода: {string} - {locale}")
                    return string.message

        else:
            return string.message


# Как использовать:
"from discord.app_commands import locale_str as _T"  # Импорт locale_str as _T
"@app_commands.command(name=_T('bonk_usr', translate_dict))"  # Дискорд сам активирует translate()

""" Структура словаря:
{"bonk_usr": {"en": "{user} have been bonked",
              "ru": "{user} был стукнут"}
}
"""
