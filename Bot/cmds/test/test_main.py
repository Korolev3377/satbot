import asyncio
import time

import discord
from discord import app_commands
from discord.ext import commands

from discord.app_commands import locale_str as _ls
from Bot.translator import Translator

locale = {"st?": {"en": "Slap Tangakk?",
                  "ru": "Дать пощечину тангакку?"},

          "st!": {"en": "*slapped <@669906303912640532> in the face*",
                  "ru": "*Дает пощечину <@669906303912640532>*"},

          "st_confirm": {"en": "{user} confirms the action",
                         "ru": "{user} подтверждает действие"},

          "st_cancel": {"en": "{user} cancels the action",
                        "ru": "{user} отменяет действие"},

          "st_idle": {"en": "No one has chosen anything... Well, that's okay...",
                      "ru": "Никто ничего не выбрал... Ну и ладно..."},

          "view_confirm": {"en": "Confirm",
                           "ru": "Подтвердить"},

          "view_cancel": {"en": "Cancel",
                          "ru": "Отменить"},

          "ok_go": {"en": "Okay, lets goooooooooo!",
                    "ru": "Окей, летс гooooooooooу!"},

          "he_dead?": {"en": "It dead?",
                       "ru": "Оно мертво?"},

          "ol_rm_p": {"en": "Core cooling protocol initialized!",
                      "ru": "Инициализирован протокол охлаждения ядра!"},

          "ol_rm_p_done": {"en": "The core cooling protocol has been completed!",
                           "ru": "Протокол охлаждения ядра завершен!"},

          "current_ol": {"en": "Current grid load: {overload}%",
                         "ru": "Текущая нагрузка цепи: {overload}%"},

          "sure_cd?": {"en": "Are you sure you want to run core cooling? I will become unavailable for a few minutes!",
                       "ru": "Вы уверены, что хотите запустить охлаждение ядра? Я стану недоступна на несколько минут!"}
          }

T = Translator(locale_dict=locale)


class Test:
    def __init__(self, BOT):
        op_group = app_commands.Group(name="test_n", description="test_d")

        @op_group.command(name="cooldown_n", description="coolldown_d", extras={"owner_only": True})
        async def colddown_cmd(interaction: discord.Interaction):
            await interaction.response.defer()
            lang = interaction.locale
            view = self.ConfirmView(user=interaction.user, lang=lang)
            await interaction.followup.send(
                T.soft_translate(string=_ls("current_ol", extras={"format": {"overload": BOT.overload}}),
                                 locale=lang))
            await interaction.followup.send(
                T.soft_translate(string=_ls("sure_cd?"),
                                 locale=lang), view=view, ephemeral=True)
            await view.wait()
            if view.status is True:
                await interaction.followup.send(T.soft_translate(string=_ls("ol_rm_p"),
                                                                 locale=lang))
                time.sleep(BOT.overload/2)
                BOT.overload = 0
                await interaction.followup.send(T.soft_translate(string=_ls("ol_rm_p_done"),
                                                                 locale=lang))
                await interaction.followup.send(
                    T.soft_translate(string=_ls("current_ol", extras={"format": {"overload": BOT.overload}}),
                                     locale=lang))

        @op_group.command(name="self_destroy_n", description="self_destroy_d", extras={"owner_only": True})
        async def self_destroy_cmd(interaction: discord.Interaction):
            await interaction.response.defer()
            lang = interaction.locale

            await interaction.followup.send(T.soft_translate(string=_ls("ok_go"),
                                                             locale=lang))
            try:
                def check(m):
                    return m.author.id == 1006637604772515900

                ddos = "Edgy roll 9999"
                await interaction.channel.send(ddos)
                while True:
                    msg = await BOT.wait_for("message", check=check, timeout=10)
                    await msg.channel.send(ddos)
                    BOT.overload += 1
            except asyncio.TimeoutError:
                await interaction.channel.send(T.soft_translate(string=_ls("he_dead?"),
                                                                locale=lang))

        @op_group.command(name="st_n", description="st_d", extras={"owner_only": True})
        async def slap_tangakk_cmd(interaction: discord.Interaction):
            await interaction.response.defer()

            lang = interaction.locale
            view = self.ConfirmView(user=interaction.user, user_check=False, lang=lang)

            await interaction.followup.send(T.soft_translate(string=_ls("st?"),
                                                             locale=lang),
                                            view=view)
            await view.wait()

            if view.status is True:
                await interaction.followup.send(T.soft_translate(
                    string=_ls("st_confirm", extras={"format": {"user": view.user}}),
                    locale=lang))
                await interaction.followup.send(T.soft_translate(string=_ls("st!"), locale=lang))
            elif view.status is False:
                await interaction.followup.send(T.soft_translate(
                    string=_ls("st_cancel", extras={"format": {"user": view.user}}),
                    locale=lang))
            else:
                await interaction.followup.send(T.soft_translate(string=_ls("st_idle"), locale=lang))

        BOT.tree.add_command(op_group)

    class ConfirmView(discord.ui.View):
        def __init__(self, lang, user, user_check=True):
            super().__init__()
            self.status = None
            self.user_check = user_check
            self.user = user
            for child in self.children:
                child.label = T.soft_translate(string=_ls(child.label, extras={}), locale=lang)

        async def on_timeout(self):
            for child in self.children:
                child.disabled = True

        @discord.ui.button(style=discord.ButtonStyle.red, label="view_confirm")
        async def confirm(self, interaction, button):
            if interaction.user == self.user or not self.user_check:
                for child in self.children:
                    child.disabled = True
                button.label = '> ' + button.label + ' <'
                self.status = True
                await interaction.response.edit_message(view=self)
                self.stop()

        @discord.ui.button(style=discord.ButtonStyle.grey, label="view_cancel")
        async def cancel(self, interaction, button):
            if interaction.user == self.user or not self.user_check:
                for child in self.children:
                    child.disabled = True
                button.label = '> ' + button.label + ' <'
                self.status = False
                await interaction.response.edit_message(view=self)
                self.stop()
