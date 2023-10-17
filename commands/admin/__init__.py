import discord
import pickle as pik

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
    "shopaddrole_cmd_name": {EN: "add-role-to-shop",
                             RU: "добавить-роль-в-магазин"},
    "shopaddrole_cmd_desc": {EN: "Add role to shop",
                             RU: "Добавить роль в магазин"},
    "role": {EN: "role",
             RU: "роль"},
    "cost": {EN: "cost",
             RU: "стоимость"},
    "stock": {EN: "stock",
              RU: "количество"},
    "visible": {EN: "visible",
                RU: "видимость"}
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

    await DB.insert_message_data(message_id=control_message.id, message_data=pik.dumps(data))

    await interaction.delete_original_response()


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
    name=namedesc("shopaddrole_cmd_name", _locale),
    description=namedesc("shopaddrole_cmd_desc", _locale),
    extras={IS_OWNER_ONLY: True}
)
@app_commands.rename(role=namedesc("role", _locale), cost=namedesc("cost", _locale), stock=namedesc("stock", _locale),
                     visible=namedesc("visible", _locale))
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
    role_data["cost"] = cost if cost >= 0 else None
    role_data["stock"] = stock if stock >= 0 else None
    role_data["visible"] = visible

    rts[str(role.id)] = role_data

    cfg_data["roles_to_sale"] = rts
    interaction.client.guilds_data[interaction.guild.id]["roles_to_sale"] = rts
    await DB.execute("UPDATE servers_config SET cfg_data = ? WHERE server_id IS ?;",
                     (pik.dumps(cfg_data), interaction.guild.id))
    await interaction.followup.send("d0ne", ephemeral=True)
