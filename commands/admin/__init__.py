import discord
import pickle as pik
import json

from discord import app_commands
from discord import ui
from discord.app_commands import locale_str as _ls

import commands
import environment
from commands.database import DB

from translator.__init__ import T
from environment.variable import *

RESTORE_BTN = "restore_btn"
SAVE_BTN = "save_btn"
CANCEL_BTN = "cancel_btn"
BACK_BTN = "back_btn"
ENTER_BTN = "enter_btn"
MAINA_BTN = "maina_btn"
VIRA_BTN = "vira_btn"

MODAL_FIELD_EDITING = "modal_field_editing"
NONE = "none"
MENU = "menu"
ACT_CAREFULLY = "act_carefully"
MAIN_MENU = "main_menu"
BOT_SETTINGS = "bot_settings"
CONFIG_EMBED_CMD_DESC = "config_embed_cmd_desc"
CONFIG_EMBED_CMD_NAME = "config_embed_cmd_name"

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
  CONFIG_EMBED_CMD_NAME: {EN: "bot-settings",
                          RU: "настройка-бота"},
  CONFIG_EMBED_CMD_DESC: {EN: "Opens bot config embed",
                          RU: "Открывает окно конфигурации бота"},
  BOT_SETTINGS: {EN: "Bot settings",
                 RU: "Настройки бота"},
  MAIN_MENU: {EN: "Main menu",
              RU: "Главное меню"},
  ACT_CAREFULLY: {EN: "Act carefully. There will NOT be a confirmation of  `Are you sure you want to do this?`!",
                  RU: "Нажимайте аккуратнее. Подтверждения  `Вы уверены что хотите сделать то-то то-то?`  НЕ будет!"},
  MENU: {EN: "Menu",
         RU: "Меню"},
  NONE: {EN: "No value",
         RU: "Нет значения"},
  MODAL_FIELD_EDITING: {EN: "Field editing",
                        RU: "Редактирование поля"},
  VIRA_BTN: {EN: "↑ Vira ↑",
             RU: "↑ Вира ↑"},
  MAINA_BTN: {EN: "↓ Maina ↓",
              RU: "↓ Майна ↓"},
  ENTER_BTN: {EN: "Enter",
              RU: "Ввод"},
  BACK_BTN: {EN: "Back",
             RU: "Назад"},
  CANCEL_BTN: {EN: "Cancel",
               RU: "Галя, у нас отмена"},
  SAVE_BTN: {EN: "Save",
             RU: "Спаси и сохрани"},
  RESTORE_BTN: {EN: "Restore default",
                RU: "Сбросить к заводским"},
  YES: {EN: "Yes",
        RU: "Да"},
  NO: {EN: "No",
       RU: "Нет"},
  #
  "wealth_name": {EN: "Wealth name",
                  RU: "Название валюты"},
  EN: {EN: "English",
       RU: "Английское"},
  RU: {EN: "Russian",
       RU: "Русское"},
  # Regular Commands
  "commands_to_declare": {EN: "Commands to declare",
                          RU: "Команды для регистрации на сервере"},
  "facts": {EN: "Add a command to output fun facts?",
            RU: "Добавить команду на вывод забавных фактов?"},
  "facts_ignore": {EN: "Add a command to add to the ignore list on the word `fact'?",
                   RU: "Добавить команду на добавление в список игнорирования на слово `факт`?"},
  "facts_count": {EN: "Add a command to output the number of facts?",
                  RU: "Добавить команду на вывод количества фактов?"},
  "cults": {EN: "Add a command to output a list of cults?",
            RU: "Добавить команду на вывод списка культов?"},
  "rolldice": {EN: "Add a dice roll command?",
               RU: "Добавить команду на бросок кубика?"},
  # Fun Commands Group
  "fungrp": {EN: "Add a group of comms for fun (GameOfLife, TicTacToe, Brainfuck)?",
             RU: "Добавить группу комманд на развлечение (GameOfLife, TicTacToe, Brainfuck)?"},
  # Wealth Commands
  "wealthgrp": {EN: "Add a group command to manage a personal wallet?",
                RU: "Добавить группу команду на управление личным кошельком?"},
  "wealthopagrp": {EN: "Add a group command to administer server economics?",
                   RU: "Добавить группу команду на администрирование экономики сервера?"},
  "fact_word_react": {EN: "React to the word `fact'?",
                      RU: "Реагировать на слово `факт`?"},
  "server_member_join_leave": {EN: "Configuring behavior when members joins in and leaves of the server",
                               RU: "Настройка поведение при входе выходе участников с сервера"},
  "enable": {EN: "Enable sending a notification of a member's joins/leaves to the server",
             RU: "Включить отправку уведомление о входе/выходе участника?"},
  "on_join": {EN: "Message when logging in to the server",
              RU: "Сообщение при входе на сервер"},
  "on_leave": {EN: "Message when leaving the server ",
               RU: "Сообщение при выходе с сервера"},
  "channel_id": {EN: "Channel where messages will be sent when a member joins/leaves from the server",
                 RU: "Канал куда будут отправляться сообщения в входе/выходе"}
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
  await interaction.client.close()


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
  name=namedesc(CONFIG_EMBED_CMD_NAME, _locale),
  description=namedesc(CONFIG_EMBED_CMD_DESC, _locale)
)
async def configembedcmd(interaction: discord.Interaction):
  await interaction.response.defer(thinking=True, ephemeral=True)
  _T.set_language(language=interaction.locale)
  # _T.set_string(string=ls(EXAMPLE_CMD_ANSWER, {"_": _T.stranslate(st=_ls(FORMAT_STRING))}))
  # await interaction.followup.send(_T.stranslate())
  configview = ConfigView(interaction.client.guilds_data[str(interaction.guild_id)], interaction)
  embed = discord.Embed(title=_T.stranslate(st=_ls(BOT_SETTINGS)), description=_T.stranslate(st=_ls(MAIN_MENU)))
  embed = configview.update_embed(embed)
  await interaction.followup.send(
    _T.stranslate(st=_ls(ACT_CAREFULLY)),
    embed=embed,
    view=configview
  )


class ConfigView(discord.ui.View):
  def __init__(self, original_config_dict, interaction):
    super().__init__()
    self.page = 0
    self.selected = 0
    self.embed = None
    self.path_to_menu = []
    self.menu_dict = dict(original_config_dict)  # сделать разделение на страницы тут
    self.interaction = interaction

    self.add_item(ConfigViraButton(_T.stranslate(_ls(VIRA_BTN))))
    self.add_item(ConfigMainaButton(_T.stranslate(_ls(MAINA_BTN))))
    self.add_item(ConfigEnterButton(_T.stranslate(_ls(ENTER_BTN))))
    self.add_item(ConfigBackButton(_T.stranslate(_ls(BACK_BTN))))
    # self.add_item(ConfigPrevButton("prev_btn"))
    # self.add_item(ConfigNextButton("next_btn"))
    self.add_item(ConfigCancelButton(_T.stranslate(_ls(CANCEL_BTN))))
    self.add_item(ConfigSaveButton(_T.stranslate(_ls(SAVE_BTN))))
    self.add_item(ConfigRestoreButton(_T.stranslate(_ls(RESTORE_BTN))))

  async def on_timeout(self):
    for child in self.children:
      child.disabled = True
    await self.interaction.edit_original_response(embed=self.update_embed(self.embed), view=self)
    self.stop()

  def update_embed(self, original_embed):
    embed = original_embed.copy()

    _T.set_language(language=self.interaction.locale)

    embed.clear_fields()
    if len(self.path_to_menu) == 0:
      embed.description = _T.stranslate(_ls(MAIN_MENU))
    else:
      embed.description = _T.stranslate(_ls(self.path_to_menu[-1]))

    i = 0

    selected_menu = dict(self.menu_dict)
    for path in self.path_to_menu:
      selected_menu = selected_menu.get(path)

    for k, v in selected_menu.items():
      embed_field_name = []
      if i == self.selected:
        embed_field_name.append("---> ")
      embed_field_name.append(_T.stranslate(st=_ls(k)))

      embed_field_value = []
      if type(v) is dict:
        embed_field_value.append("= " + _T.stranslate(st=_ls(MENU)))
      elif type(v) is bool:
        embed_field_value.append("- " + [_T.stranslate(st=_ls(NO)), _T.stranslate(st=_ls(YES))][bool(v)])
      elif v is None or len(v) == 0:
        embed_field_value.append("- " + _T.stranslate(st=_ls(NONE)))
      else:
        embed_field_value.append("- `" + v + "`")
      embed.add_field(name="".join(embed_field_name), value="".join(embed_field_value), inline=False)
      i += 1
    self.embed = embed
    return embed


class ConfigViraButton(discord.ui.Button):
  def __init__(self, name):
    super().__init__(label=name, disabled=False, row=0, custom_id="vira")

  async def callback(self, interaction):
    if self.view.selected > 0:
      self.view.selected -= 1
    await interaction.response.edit_message(embed=self.view.update_embed(self.view.embed))


class ConfigMainaButton(discord.ui.Button):
  def __init__(self, name):
    super().__init__(label=name, disabled=False, row=0, custom_id="maina")

  async def callback(self, interaction):
    if self.view.selected < len(self.view.embed.fields) - 1:
      self.view.selected += 1
    await interaction.response.edit_message(embed=self.view.update_embed(self.view.embed))


class ConfigEnterButton(discord.ui.Button):
  def __init__(self, name):
    super().__init__(label=name, disabled=False, style=discord.ButtonStyle.blurple, row=0, custom_id="enter")

  async def callback(self, interaction):
    selected_menu = dict(self.view.menu_dict)
    for path in self.view.path_to_menu:
      selected_menu = selected_menu.get(path)
    if type(selected_menu.get(list(selected_menu.keys())[self.view.selected])) is dict:
      self.view.path_to_menu.append(list(selected_menu.keys())[self.view.selected])
      self.view.selected = 0
      await interaction.response.edit_message(embed=self.view.update_embed(self.view.embed))
    elif type(selected_menu.get(list(selected_menu.keys())[self.view.selected])) is bool:
      keys = list(self.view.path_to_menu)
      keys.append(list(selected_menu.keys())[self.view.selected])
      new_value = not selected_menu.get(list(selected_menu.keys())[self.view.selected])
      edited_menu_dict = self.view.menu_dict

      for key in keys[:-1]:
        edited_menu_dict = edited_menu_dict[key]

      edited_menu_dict[keys[-1]] = new_value
      await interaction.response.edit_message(embed=self.view.update_embed(self.view.embed))
    else:
      keys = list(self.view.path_to_menu)
      keys.append(list(selected_menu.keys())[self.view.selected])

      class TextEditModal(discord.ui.Modal):
        def __init__(self, view):
          super().__init__(title=_T.stranslate(_ls(MODAL_FIELD_EDITING)))
          self.view = view
          self.add_item(discord.ui.TextInput(label=list(selected_menu.keys())[self.view.selected],
                                             default=list(selected_menu.values())[self.view.selected], required=False))

        async def on_submit(self, interaction):
          new_value = str(self.children[0])
          edited_menu_dict = self.view.menu_dict
          for key in keys[:-1]:
            edited_menu_dict = edited_menu_dict[key]
          edited_menu_dict[keys[-1]] = new_value
          await interaction.response.edit_message(embed=self.view.update_embed(self.view.embed))

      await interaction.response.send_modal(TextEditModal(self.view))


class ConfigBackButton(discord.ui.Button):
  def __init__(self, name):
    super().__init__(label=name, disabled=False, row=0, custom_id="back")

  async def callback(self, interaction):
    if len(self.view.path_to_menu) > 0:
      self.view.path_to_menu.pop(-1)
    self.view.selected = 0
    await interaction.response.edit_message(embed=self.view.update_embed(self.view.embed))


class ConfigPrevButton(discord.ui.Button):  # перелистывания страниц
  def __init__(self, name):
    super().__init__(label=name, disabled=True, row=1, custom_id="prev")


class ConfigNextButton(discord.ui.Button):  # перелистывание страниц
  def __init__(self, name):
    super().__init__(label=name, disabled=True, row=1, custom_id="next")


class ConfigCancelButton(discord.ui.Button):
  def __init__(self, name):
    super().__init__(label=name, disabled=False, style=discord.ButtonStyle.red, row=2,
                     custom_id="cancel")

  async def callback(self, interaction):
    for child in self.view.children:
      child.disabled = True
    await interaction.response.edit_message(embed=self.view.update_embed(self.view.embed), view=self.view)
    self.view.stop()


class ConfigSaveButton(discord.ui.Button):
  def __init__(self, name):
    super().__init__(label=name, disabled=False, style=discord.ButtonStyle.green, row=2, custom_id="save")

  async def callback(self, interaction):
    for child in self.view.children:
      child.disabled = True
    await interaction.response.edit_message(embed=self.view.update_embed(self.view.embed), view=self.view)
    interaction.client.guilds_data[str(interaction.guild_id)] = self.view.menu_dict
    await DB.execute("UPDATE servers_config SET cfg_data = ? WHERE server_id = ?;",
                     (pik.dumps(self.view.menu_dict), str(interaction.guild_id)))
    self.view.stop()
    await commands.declare_commands(interaction.client)


class ConfigRestoreButton(discord.ui.Button):
  def __init__(self, name):
    super().__init__(label=name, disabled=False, row=2, custom_id="restore")

  async def callback(self, interaction):
    self.view.menu_dict = environment.CONFIG.DEFAULT_CFG
    await interaction.response.edit_message(embed=self.view.update_embed(self.view.embed), view=self.view)
