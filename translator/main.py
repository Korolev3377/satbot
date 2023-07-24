from discord import app_commands
from environment.variable import *


class T(app_commands.Translator):
    def __init__(self, locale_dict=None):
        super().__init__()
        self.language = None
        self.string = None
        self.translate_not_found = set()
        if locale_dict:
            self.locale_dict = locale_dict
        else:
            self.locale_dict = {
                "_": {"en": "_",
                      "ru": "_"},

                "cmd_broken": {"en": "Sorry. This command broken! :(",
                               "ru": "Простите. Эта комманда сломана! :("},

                "cmd_disabled": {"en": "Sorry. This command disabled! :(",
                                 "ru": "Простите. Эта комманда отключена! :("},

                "cmd_adminonly": {"en": "Sorry. This command only for admins! :(",
                                  "ru": "Простите. Эта комманда только для администраторов! :("},

                "cmd_owneronly": {"en": "Sorry. This command disabled! :(",
                                  "ru": "Простите. Эта комманда отключена! :("},

                "on_cd": {
                    "en": "Whoa, you're overloading my fragile circuits... Please wait {_} seconds before "
                          "making this request again.",
                    "ru": "Оу, ты так мне цепи перегрузишь... Подожди, пожалуйста, {_} секунд, прежде чем "
                          "спрашивать меня об этом снова."},

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

        if ln:
            language = ln
        else:
            language = self.language

        if self.locale_dict:
            result = self.locale_dict.get(string.message)  # Наименование, которое нужно перевести
            if not result:  # Если не удалось найти наименование в словаре перевода
                self.translate_not_found.add(string.message)
                return string.message

            ln = self.get_lang(language.value)

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
                return string.extras.get(EXTRAS).get(DICT).get(self.get_lang(locale.value))
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
