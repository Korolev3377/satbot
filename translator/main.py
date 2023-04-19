from discord import app_commands
from environment.variable import *


class T(app_commands.Translator):
    def __init__(self, locale_dict=None):
        super().__init__()
        self.locale = None
        self.string = None
        self.translate_not_found = set()
        if locale_dict:
            self.locale_dict = locale_dict
        else:
            self.locale_dict = {
                "_": {"en": "_",
                      "ru": "_"},

                "test_n": {"en": "test",
                           "ru": "тест"},

                "test_d": {"en": "Experemental commands",
                           "ru": "Эксперементальные комманды"},

                "help_n": {"en": "help",
                           "ru": "помощь"},

                "help_d": {"en": "Command for output all commands",
                           "ru": "Команда для вывода всех комманд и их использования"},

                "st_n": {"en": "slap-tangakk",
                         "ru": "шлепнуть-тангакка"},

                "st_d": {"en": "Command for slap Tangakk",
                         "ru": "Команда для отшлепывания Тангакка. А так же для тестирования комманд."},

                "cmd_broken": {"en": "Sorry. This command broken! :(",
                               "ru": "Простите. Эта комманда сломана! :("},

                "cmd_disabled": {"en": "Sorry. This command disabled! :(",
                                 "ru": "Простите. Эта комманда отключена! :("},

                "cmd_adminonly": {"en": "Sorry. This command only for admins! :(",
                                  "ru": "Простите. Эта комманда только для администраторов! :("},

                "cmd_owneronly": {"en": "Sorry. This command disabled! :(",
                                  "ru": "Простите. Эта комманда отключена! :("},

                "fun_n": {"en": "games",
                          "ru": "игры"},

                "fun_d": {"en": "Funny commands",
                          "ru": "Комманды для развлечения"},

                "bf_n": {"en": "brainfuck",
                         "ru": "брэйнфак"},

                "bf_d": {"en": "Brainfuck code reader",
                         "ru": "Запустить брэйнфак код"},

                "gol_n": {"en": "game-of-life",
                          "ru": "игра-в-жизнь"},

                "gol_d": {"en": "Launch Game of life simulation",
                          "ru": "Запустить симуляцию игры в жизнь"},

                "ttt_n": {"en": "tic-tac-toe",
                          "ru": "крестики-нолики"},

                "ttt_d": {"en": "Create Tic Tac Toe field",
                          "ru": "Создать поле для крестиков ноликов"},

                "self_destroy_n": {"en": "self-destruction",
                                   "ru": "самоуничтожение"},

                "self_destroy_d": {"en": "Mutual self-destruction",
                                   "ru": "Взаимное самоуничтжение"},

                "cooldown_n": {"en": "cooldown-core",
                               "ru": "охладить-ядро"},

                "coolldown_d": {"en": "Initialize the core cooling protocol",
                                "ru": "Инициализировать протокол охлаждения ядра"},

                "facts_count_n": {"en": "how-many-facts",
                                  "ru": "количество-фактов"},

                "facts_count_d": {"en": "(WIP) How many facts in 8915-7's DataBase",
                                  "ru": "(WIP) Количество фактов в БазеДанных 8915-7"},

                "nick_blue_n": {"en": "nick-blue",
                                "ru": "синий-ник"},

                "nick_blue_d": {"en": "(WIP)",
                                "ru": "(WIP)"},

                "cult_n": {"en": "cults",
                           "ru": "культы"},

                "cult_d": {"en": "Show guild cults",
                           "ru": "Показать культы сервера"},

                "dice_n": {"en": "roll-dice",
                           "ru": "кинуть-игральные-кости"},

                "dice_d": {"en": "Randomizer",
                           "ru": "Рандомайзер"},

                "dice_args": {"en": "dices",
                              "ru": "кости"},

                "fact_n": {"en": "enjoy-fact",
                           "ru": "забавный-факт"},

                "fact_d": {"en": "Let me tell you a enjoy fact",
                           "ru": "Расскажу вам один забавный факт"},

                "on_cd": {
                    "en": "Whoa, you're overloading my fragile circuits... Please wait {time_left} seconds before "
                          "making this request again.",
                    "ru": "Оу, ты так мне цепи перегрузишь... Подожди, пожалуйста, {time_left} секунд, прежде чем "
                          "спрашивать меня об этом снова."},

                "nb_n": {"en": "nickblue",
                         "ru": "синий-ник"},

                "nb_d": {"en": "Nickblue raffle",
                         "ru": "Рулетка в честь Синего ника"},

                "join_nb_n": {"en": "join",
                              "ru": "присоединиться"},

                "join_nb_d": {"en": "Join nickblue raffle",
                              "ru": "Приcоединиться к рулетке Nick_blue"},

                "left_nb_n": {"en": "exit",
                              "ru": "выйти"},

                "left_nb_d": {"en": "Exit from nickblue raffle",
                              "ru": "Выйти из рулетки Nick_blue"},

                "show_nb_n": {"en": "status",
                              "ru": "статус"},

                "show_nb_d": {"en": "Who is Nickblue and candidates",
                              "ru": "Кто Nick_blue и кандидаты"},

                "input": {"en": "input",
                          "ru": "ввод"},

                "code": {"en": "code",
                         "ru": "код"},

                "size": {"en": "field-size",
                         "ru": "размер-поля"},

                "command": {"en": "command",
                            "ru": "комманда"},

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

    def set_locale(self, locale):
        self.locale = locale

    def set_string(self, string):
        self.string = string

    def stranslate(self, st=None, lc=None):
        if st:
            string = st
        else:
            string = self.string

        if lc:
            locale = lc
        else:
            locale = self.locale

        if self.locale_dict:
            result = self.locale_dict.get(string.message)  # Наименование, которое нужно перевести
            if not result:  # Если не удалось найти наименование в словаре перевода
                self.translate_not_found.add(string.message)
                return string.message

            lang = self.get_lang(locale.value)

            result = result.get(lang)  # Получение перевода из locale_dict
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
