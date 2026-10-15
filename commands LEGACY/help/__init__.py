import discord
from discord import app_commands

from discord.app_commands import locale_str as _ls
from _translator import T as T

locale = {"sc": {"en": "**Subcommands:**",
                 "ru": "**Подкомманды:**"},

          "help": {"en": "Help",
                   "ru": "Помощь"},

          "ac": {"en": "Available commands:",
                 "ru": "Доступные комманды:"},

          "cmd_notfound": {"en": "Error: Command \"{cmd}\" not found",
                           "ru": "Ошибка: Комманда \"{cmd}\" не найдена"},

          "cmd_sig": {"en": "Command \"{cmd}\":",
                      "ru": "Комманда \"{cmd}\":"}
          }

_T = Tra(locale_dict=locale)

doc = {"help_doc": {"en": "**Usage:** help <command>",
                    "ru": "**Использование:** помощь <комманда>"},
       "gol_doc": {"en": """**Usage:** games game-of-life <field-size>
Default field size - 5
Minimum field size - 3
Maximum field size with emoji - 13
Maximum field size w/o emoji - 28

This is game of life with custom cells

Buttons:
:arrow_up: :arrow_left: :arrow_down: :arrow_right: - Move cursor
:white_medium_square: :package: :firecracker: - Creates or deletes a cell at the cursor position
:play_pause: - Next turn
Green button - Auto play
Red button - Stop game

Rules:
:black_large_square: - Empty cell. If the activity **equals** 3, **a classic cell is created**
:white_medium_square: - Classic cell. **Increases** activity by 1. **Dies** if activity does **not equal** 2 or 3
:package: - Wall cell. Does nothing and **not allow** a classical cell to appear on it. **Dies** if activity is **less than** 0
:firecracker: - Dangerous cell. **Increases** activity by 1. **Explodes** if activity is **equal to or greater** than 6. When exploded, creates an explosion cell in its place.
:boom: - Explosion cell. This cell appears when a dangerous cell explodes. **Reduces** activity by 8

Activity is the value that determines whether a cell will live or die the next turn.
When a cell creates an activity, that activity is counted by neighboring cells. A cell does not count its activity.""",

                   "ru": """**Использование:** игры игра-в-жизнь <размер-поля>
Стандартный размер поля - 5
Минимальный размер поля - 3
Максимальный размер поля с эмодзи - 13
Максимальный размер поля без эмодзи - 28

Это игра в жизнь с кастомными клетками

Кнопки:
:arrow_up: :arrow_left: :arrow_down: :arrow_right: - Перемещать курсор
:white_medium_square: :package: :firecracker: - Создавать или удалять клетки на позиции курсора
:play_pause: - Следующий ход
Green button - Автоматический ход
Red button - Остановить игру

Правила:
:black_large_square: - Пустая клетка. Если активность **больше** 3, **классическая клетка создается**
:white_medium_square: - Классическая клетка. **Увеличивает** активность на 1. **Умирает**, если активность **не равна** 2 или 3
:package: - Стена. Ничего не делает и **не позволяет** появляться классическим клеткам на ней. **Умерает**, если активность **меньше чем** 0
:firecracker: - Взрывоопасная клетка. **Увеличивает** активность на 1. **Взрывается**, если активность **больше или равна** 6. Когда взрывается, создает взрыв-клетку на своем месте.
:boom: - Взрыв-клетка. Появляется, только когда взрывоопасная клетка взрывается. **Уменьшает** активность на 8

Активность - это значение, которое определяет, будет ли клетка жить или умрет в следующий ход.
Когда клетка создает активность, эта активность подсчитывается соседними клетками. Клетка не считает свою активность."""}}

_docT = Tra(locale_dict=doc)


class Help:
    def __init__(self, BOT):
        def signatures(cmd_list, lang):
            to_return = []
            for cmd in cmd_list:
                to_return.append("%s - %s" % (BOT.tree.translator.stranslate(string=_ls(cmd.name), locale=lang),
                                              BOT.tree.translator.stranslate(string=_ls(cmd.description),
                                                                             locale=lang) or _ls("...")))
            return "\n".join(to_return)

        def get_commands(group, cmd_name):
            if type(group) is app_commands.CommandTree:
                if cmd := group.get_command(BOT.tree.translator.inverted_locale_dict.get(cmd_name)):
                    if is_hidden := cmd.extras.get("hidden"):
                        return
                    return cmd
                else:
                    return None
            elif type(group) is app_commands.Group:
                cmd = group.get_command(BOT.tree.translator.inverted_locale_dict.get(cmd_name))
                if is_hidden := cmd.extras.get("hidden"):
                    return
                return cmd
            elif type(group) is app_commands.Command:
                if is_hidden := group.extras.get("hidden"):
                    return
                return group
            else:
                return None

        def get_help(cmd, lang):
            desc = BOT.tree.translator.stranslate(string=_ls(cmd.description), locale=lang)
            if type(cmd) is app_commands.Group:
                parents = signatures([cmd for cmd in cmd.commands if not cmd.extras.get("hidden")], lang)
            else:
                parents = None
            help_doc = []
            if desc:
                help_doc.append(desc)
            if parents:
                help_doc.append(f"\n{_T.stranslate(string=_ls('sc'), locale=lang)}\n" + parents)
            return "\n".join(help_doc)

        @BOT.tree.command(name="help_n",
                          description="help_d", extras={"usage": "help_doc"})
        async def help_cmd(interaction: discord.Interaction, *, command: str = None):
            await interaction.response.defer(ephemeral=True, thinking=True)

            lang = interaction.locale

            embed = discord.Embed(title=_T.stranslate(string=_ls("help"), locale=lang))
            if not command:
                embed.add_field(name=_T.stranslate(string=_ls("ac"), locale=lang),
                                value=signatures(BOT.tree.get_commands(), lang) or None,
                                inline=False)
                await interaction.followup.send(embed=embed, ephemeral=True)
            else:
                sub = BOT.tree
                for arg in command.split():
                    sub = get_commands(sub, arg)
                    if not sub:
                        await interaction.followup.send(
                            _T.stranslate(string=_ls("cmd_notfound", extras={"format": {"cmd": arg}}), locale=lang))
                        return
                cmd_name = []
                for q_name in sub.qualified_name.split():
                    cmd_name.append(BOT.tree.translator.stranslate(string=_ls(q_name), locale=lang))
                cmd_name = " ".join(cmd_name)
                embed.add_field(
                    name=_T.stranslate(string=_ls("cmd_sig", extras={"format": {"cmd": cmd_name}}), locale=lang),
                    value=get_help(sub, lang),
                    inline=False)
                await interaction.followup.send(embed=embed, ephemeral=True)
                if usage := sub.extras.get("usage"):
                    await interaction.followup.send(_docT.stranslate(string=_ls(usage), locale=lang),
                                                    ephemeral=True)

                # if doc := sub.help:
                #    await interaction.followup.send(content=doc, ephemeral=True)
