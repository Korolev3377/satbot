import discord

from discord import app_commands
from discord.app_commands import locale_str as _ls

from translator.main import T
from environment.variable import *

CHNL = "chnl"
MSG = "msg"
_ = ""
EXAMPLE_CMD_ANSWER = "1"
FORMAT_STRING = "2"
FUNNYTN = "ftn"
FUNNYTD = "ftd"
CRC = "crc"
ADMINGN = "opn"
ADMINGD = "opd"
CRCN = "crcn"
CRCD = "crcd"
ROLES = "roles"
CR = "cr"
TEST = "t"

_locale: dict = {
    _: {EN: "",
        RU: ""},

    EXAMPLE_CMD_ANSWER: {EN: "Clownfish. {_}",
                         RU: "Рыба-клоун. {_}"},
    FORMAT_STRING: {EN: "Smile!",
                    RU: "Улыбнись!"},
    FUNNYTN: {EN: "funny-thing",
              RU: "забавный-ништяг"},
    FUNNYTD: {EN: "Idk. This command only for odmens!",
              RU: "Чзх. Эта комманда только для одменов!"},
    ADMINGN: {EN: "opa",
              RU: "опа"},
    ADMINGD: {EN: "Admins thing.",
              RU: "Шняги для одменов."},
    MSG: {EN: "message",
          RU: "сообщение"},
    CHNL: {EN: "channel",
           RU: "канал"},
    CRCN: {EN: "create-role-selection",
           RU: "создание-выборки-ролей"},
    CRCD: {EN: "This command only for admins!",
           RU: "Эта комманда только для админов!"},
    ROLES: {EN: "roles",
            RU: "роли"},
    TEST: {EN: "t1",
           RU: "t2"}
}

_T = T(locale_dict=_locale)

admingrp = create_group(ADMINGN, ADMINGD, _locale)
admingrp.default_permissions = discord.Permissions.none()


@admingrp.command(
    name=namedesc(FUNNYTN, _locale),
    description=namedesc(FUNNYTD, _locale),
    extras={IS_OWNER_ONLY: True}
)
@app_commands.rename(msg=namedesc(MSG, _locale),
                     chnl=namedesc(CHNL, _locale))
async def botsay(interaction: discord.Interaction, msg: str, chnl: str = None):
    await interaction.response.defer(thinking=True, ephemeral=True)
    if chnl:
        chnl = await interaction.client.fetch_channel(int(chnl))
    else:
        chnl = interaction.channel
    await interaction.followup.send("Бэклог - сделать управление сообщением.")
    # view с удалением, редактированием сообщением
    # contex menu с возможностью создать view выше
    await chnl.send(msg)


@botsay.autocomplete(CHNL)
async def channel_autocomplite(interaction: discord.Interaction, current: str):
    return [app_commands.Choice(name=str(_.name), value=str(_.id))
            for _ in interaction.client.get_all_channels()
            if _.name in current and _.type.value in (0,)][:25]


@admingrp.command(
    name=namedesc(CRCN, _locale),
    description=namedesc(CRCD, _locale),
    extras={IS_ADMIN_ONLY: True}
)
@app_commands.rename(rls=namedesc(ROLES, _locale))
async def crc(interaction: discord.Interaction, rls: str):
    await interaction.response.defer(thinking=True, ephemeral=False)
    roles: list = [interaction.guild.get_role(r) for r in map(int, rls.split())]
    # create view with button (choice role)
    # ephemeral view with view.select role and two buttons (add and remove role)
    view = CrcView(lang=interaction.locale)
    await interaction.followup.send(view=view)


class CrcView(discord.ui.View):
    lang = discord.Locale.american_english

    def __init__(self, lang=None):
        super().__init__(timeout=None)
        if lang:
            self.lang = lang

    @discord.ui.button(label=_T.stranslate(_ls(TEST), lang), custom_id="crcb")
    async def crcbutton(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message('View', ephemeral=True)
