import sys

import discord
import pickle as pik
import json

from discord import app_commands
from discord import ui
from discord.app_commands import locale_str as _ls
from commands.database import DB

from translator.__init__ import T
from environment.variable import *

_locale: dict = {
    ADMIN_GRP_NAME: {EN: "opa",
                     RU: "опа"},
    ADMIN_GRP_DESC: {EN: "Admins thing",
                     RU: "Штуки для админов"},
    BOTSAY_CMD_NAME: {EN: "speak-for-bot",
                      RU: "говорить-за-бота"},
    BOTSAY_CMD_DESC: {EN: "Sends a message on behalf of the bot",
                      RU: "Отправляет сообщение от имени бота"},
    MSG: {EN: "message",
          RU: "сообщение"},
    CHNL: {EN: "channel",
           RU: "канал"},
    EDIT: {EN: "Edit",
           RU: "Редактировать"},
    DELETE: {EN: "Delete",
             RU: "Удалить"},
    MODAL_TITLE: {EN: "Message editor",
                  RU: "Редактирования сообщения"},
    MODAL_TEXT_LABEL: {EN: "Message content",
                       RU: "Содержание сообщения"},
    SHOPADDROLE_CMD_NAME: {EN: "add-role-to-shop",
                           RU: "добавить-роль-в-магазин"},
    SHOPADDROLE_CMD_DESC: {EN: "Add role to shop",
                           RU: "Добавить роль в магазин"},
    ROLE: {EN: ROLE,
           RU: "роль"},
    COST: {EN: COST,
           RU: "стоимость"},
    STOCK: {EN: STOCK,
            RU: "количество"},
    VISIBLE: {EN: VISIBLE,
              RU: "видимость"},
    BOT_TERM_NAME: {EN: "shutdown-bot",
                    RU: "выключить-бота"},
    BOT_TERM_DESC: {EN: "Shutdwon bot",
                    RU: "Запустить процедуру отключения бота"},
    SHUTING_DOWN: {EN: "Shuting down...",
                   RU: "Прощай, жестокий мир..."},
    CFG_GET_CMD_NAME: {EN: "get-config-data",
                       RU: "получить-конфиг"},
    CFG_GET_CMD_DESC: {EN: "Returns configuration file.",
                       RU: "Просмотреть конфиг-фаил."},
    CFG_FOR_SERVER: {EN: "Here {new?}config file for server \"{serv_name}\":\n",
                     RU: "Вот {new?}конфигурация сервера \"{serv_name}\":\n"},
    CFG_LOAD_CMD_NAME: {EN: "edit-config-data",
                        RU: "редактировать-конфиг"},
    CFG_LOAD_CMD_DESC: {EN: "Returns config edit message in PM.",
                        RU: "Запускает редактирование конфига."},
    DETALS_IN_PM: {EN: "Details sent to PM.\n{msg_link}",
                   RU: "Детали отправлены в личку.\n{msg_link}"},
    GIMME_CONFIG: {
        EN: "Send the following message with the configuration file to change the server settings \"{serv_name}\".",
        RU: "Отправьте следующее сообщение с файлом конфигурации, чтобы изменить настройки сервера \"{serv_name}\"."},
    NEW: {EN: "**new** ",
          RU: "**новая** "},
    NO_FILE_DETECTED: {EN: "No file was detected in your message. Action canceled.",
                       RU: "В вашем сообщении не обнаружен файл. Действие отменено."},
    ASYNCIO_TIMEOUT_ERROR: {EN: "The waiting time has expired.",
                            RU: "Время ожидания истекло."}
}

_T = T(locale_dict=_locale)

admingrp = create_group(ADMIN_GRP_NAME, ADMIN_GRP_DESC, _locale)
admingrp.default_permissions = discord.Permissions.none()


@admingrp.command(
    name=namedesc(BOTSAY_CMD_NAME, _locale),
    description=namedesc(BOTSAY_CMD_DESC, _locale),
    extras={IS_OWNER_ONLY: True}
)
@app_commands.rename(msg=namedesc(MSG, _locale),
                     chnl=namedesc(CHNL, _locale))
async def botsay(interaction: discord.Interaction, msg: str, chnl: str = None):
    await interaction.response.defer(ephemeral=True, thinking=True)
    _T.set_language(interaction.locale)
    if not chnl:
        chnl = interaction.channel
    else:
        chnl = interaction.client.get_channel(int(chnl))

    message = await chnl.send(msg)

    view = BotsayView(interaction.locale)

    control_message = await interaction.user.send(content=message.jump_url, view=view)

    data = {
        "message_id": message.id,
        "channel_id": message.channel.id,
        "content": message.content,
        "language": interaction.locale.value
    }


@admingrp.command(
    name=namedesc(BOT_TERM_NAME, _locale),
    description=namedesc(BOT_TERM_DESC, _locale)
)
async def bottermcmd(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True, thinking=True)
    _T.set_language(language=interaction.locale)
    _T.set_string(string=_ls(SHUTING_DOWN))
    await interaction.followup.send(_T.stranslate())
    interaction.client.logger.critical(
        f"Пользователь {interaction.user.name} ({interaction.user.id}) запустил команду отключения бота!")
    sys.exit(0)


class BotsayView(discord.ui.View):
    def __init__(self, locale=None):
        super().__init__(timeout=None)
        self.add_item(self.EditMessageButton(locale))
        self.add_item(self.DeleteMessageButton(locale))

    class EditMessageButton(discord.ui.Button):
        def __init__(self, locale=None):
            super().__init__(label=_T.stranslate(_ls(EDIT), locale), style=discord.ButtonStyle.blurple,
                             custom_id="editmessage")

        async def callback(self, interaction: discord.Interaction):
            i = await DB.select_message_data(interaction.message.id)
            if i:
                data = pik.loads(i[0])
                modal = self.EditModal(data.get("content"), data.get("language"))
                await interaction.response.send_modal(modal)
                await modal.wait()
                data["content"] = modal.data
                await DB.update_message_data(interaction.message.id, pik.dumps(data))
                try:
                    channel = await interaction.client.fetch_channel(data.get("channel_id"))
                    message = await channel.fetch_message(data.get("message_id"))
                    await message.edit(content=modal.data)
                except:
                    await interaction.message.delete()
            else:
                await interaction.message.delete()

        class EditModal(discord.ui.Modal):
            data = None

            def __init__(self, data, locale):
                _T.set_language(locale)
                super().__init__(title=_T.stranslate(_ls(MODAL_TITLE), locale))
                self.add_item(ui.TextInput(label=_T.stranslate(_ls(MODAL_TEXT_LABEL), locale), default=data,
                                           style=discord.TextStyle.paragraph))

            async def on_submit(self, interaction: discord.Interaction):
                await interaction.response.defer(ephemeral=True)
                self.data = self.children[0].value

    class DeleteMessageButton(discord.ui.Button):
        def __init__(self, locale=None):
            _T.set_language(locale)
            super().__init__(label=_T.stranslate(_ls(DELETE), locale), style=discord.ButtonStyle.red,
                             custom_id="deletemessage")

        async def callback(self, interaction: discord.Interaction):
            i = await DB.select_message_data(interaction.message.id)
            if i:
                data = pik.loads(i[0])
                await DB.delete_message_data(interaction.message.id)
                channel = await interaction.client.fetch_channel(data.get("channel_id"))
                message = await channel.fetch_message(data.get("message_id"))
                await message.delete()
            await interaction.message.delete()


@botsay.autocomplete(CHNL)
async def channel_autocomplite(interaction: discord.Interaction, current: str):
    return [app_commands.Choice(name=str(channel.name), value=str(channel.id))
            for channel in interaction.guild.channels
            if current in channel.name and channel.type.value in (0,)][:25]


@admingrp.command(
    name=namedesc(SHOPADDROLE_CMD_NAME, _locale),
    description=namedesc(SHOPADDROLE_CMD_DESC, _locale),
    extras={IS_OWNER_ONLY: True}
)
@app_commands.rename(role=namedesc(ROLE, _locale), cost=namedesc(COST, _locale), stock=namedesc(STOCK, _locale),
                     visible=namedesc(VISIBLE, _locale))
async def shopaddrolecmd(interaction: discord.Interaction, role: discord.Role, cost: app_commands.Range[int, -1],
                         stock: app_commands.Range[int, -1], visible: bool = True):
    await interaction.response.defer(thinking=True, ephemeral=True)
    cfg_data = interaction.client.guilds_data.get(interaction.guild.id)
    if cfg_data:
        rts = cfg_data.get("roles_to_sale") or {}
    else:
        cfg_data["roles_to_sale"] = {}
        rts = cfg_data.get("roles_to_sale") or {}

    role_data = rts.get(str(role.id)) or {}

    role_data["id"] = str(role.id)
    role_data["name"] = role.name
    role_data[COST] = cost if cost >= 0 else None
    role_data[STOCK] = stock if stock >= 0 else None
    role_data[VISIBLE] = visible

    rts[str(role.id)] = role_data

    cfg_data["roles_to_sale"] = rts
    interaction.client.guilds_data[interaction.guild.id]["roles_to_sale"] = rts
    await DB.execute("UPDATE servers_config SET cfg_data = ? WHERE server_id IS ?;",
                     (pik.dumps(cfg_data), interaction.guild.id))
    await interaction.followup.send("d0ne", ephemeral=True)


@admingrp.command(
    name=namedesc(CFG_GET_CMD_NAME, _locale),
    description=namedesc(CFG_GET_CMD_DESC, _locale)
)
async def cfggcmd(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True, thinking=True)
    _T.set_language(language=interaction.locale)
    with open("config.json", "w") as f:
        json.dump(interaction.client.guilds_data[str(interaction.guild_id)], fp=f, indent="  ", ensure_ascii=False)
    _T.set_string(string=ls(CFG_FOR_SERVER, {"new?": "", "serv_name": interaction.guild.name}))
    det_msg = await interaction.user.send(_T.stranslate(), file=discord.File(r"config.json"))
    await interaction.followup.send(_T.stranslate(st=ls(DETALS_IN_PM, {"msg_link": det_msg.jump_url})))


@admingrp.command(
    name=namedesc(CFG_LOAD_CMD_NAME, _locale),
    description=namedesc(CFG_LOAD_CMD_DESC, _locale)
)
async def cfglcmd(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True, thinking=True)
    _T.set_language(language=interaction.locale)
    det_msg = await interaction.user.send(_T.stranslate(st=ls(GIMME_CONFIG, {"serv_name": interaction.guild.name})))
    await interaction.followup.send(_T.stranslate(st=ls(DETALS_IN_PM, {"msg_link": det_msg.jump_url})))

    def check(msg):
        return msg.channel == interaction.user.dm_channel

    try:
        message = await interaction.client.wait_for("message", timeout=300, check=check)
    except asyncio.TimeoutError:
        _T.set_string(string=ls(ASYNCIO_TIMEOUT_ERROR))
        await det_msg.reply(_T.stranslate())
    else:
        if len(message.attachments) > 0:
            file = await message.attachments[0].read()
            cfg = json.loads(file.decode("utf-8"))
            interaction.client.guilds_data[str(interaction.guild_id)] = cfg
            await DB.execute("UPDATE servers_config SET cfg_data = ? WHERE server_id = ?;",
                             (pik.dumps(cfg), str(interaction.guild_id)))

            with open("config.json", "w") as f:
                json.dump(interaction.client.guilds_data[str(interaction.guild_id)], fp=f, indent="  ",
                          ensure_ascii=False)
            _T.set_string(
                string=ls(CFG_FOR_SERVER, {"new?": _T.stranslate(st=ls(NEW)), "serv_name": interaction.guild.name}))
            await message.reply(_T.stranslate(), file=discord.File(r"config.json"))
        else:
            _T.set_string(string=ls(NO_FILE_DETECTED))
            await message.reply(_T.stranslate())
