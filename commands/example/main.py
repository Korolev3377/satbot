import discord

from discord import app_commands
from discord.app_commands import locale_str as _ls

from translator.main import T
from environment.variable import *

_ = ""
EXAMPLE_CMD_ANSWER = "examplecmd_answer"
FORMAT_STRING = "format_string"
EXAMPLE_CMD_NAME = "examplecmd_name"
EXAMPLE_CMD_DESC = "examplecmd_desc"
EXAMPLE_GRP_NAME = "examplegrp_name"
EXAMPLE_GRP_DESC = "examplegrp_desc"

_locale = {
    _: {EN: "",
        RU: ""},

    EXAMPLE_CMD_ANSWER: {EN: "command_answer {_}",
                         RU: "ответ-комманды {_}"},
    FORMAT_STRING: {EN: "format-string",
                    RU: "отформатированная-строка"},
    EXAMPLE_CMD_NAME: {EN: "command-name",
                       RU: "название-комманды"},
    EXAMPLE_CMD_DESC: {EN: "command-description",
                       RU: "описание-комманды"},
    EXAMPLE_GRP_NAME: {EN: "group-name",
                       RU: "название-группы"},
    EXAMPLE_GRP_DESC: {EN: "group-description",
                       RU: "описание-группы"}
}

_T = T(locale_dict=_locale)

examplegrp = create_group(EXAMPLE_GRP_NAME, EXAMPLE_GRP_DESC, _locale)


@examplegrp.command(
    name=namedesc(EXAMPLE_CMD_NAME, _locale),
    description=namedesc(EXAMPLE_CMD_DESC, _locale)
)
async def examplecmd(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    _T.set_language(language=interaction.locale)
    _T.set_string(
        string=_ls(
            EXAMPLE_CMD_ANSWER,
            extras={
                FORMAT: {
                    "_": _T.stranslate(st=_ls(FORMAT_STRING))
                }
            }
        )
    )
    await interaction.followup.send(_T.stranslate())
