import discord
from typing import Union

from discord import app_commands
from discord.app_commands import locale_str as _ls

from translator.__init__ import T
from environment.variable import *

_locale = {
    SHOP_GROUP: {EN: "inventory",
                 RU: "инвентарь"},
    SHOP_GROUP_D: {EN: "inventory",
                   RU: "инвентарь"},
    BUY_ROLES: {EN: "buy-roles",
                RU: "купить-роли"},
    BUY_ROLES_D: {EN: "Check roles to buy",
                  RU: "Просмотреть покупаемые роли"},
    ROLES_INV: {EN: "yours-roles",
                RU: "ваши-роли"},
    ROLES_INV_D: {EN: "Personal roles control",
                  RU: "Управление персональными ролями"},
    ROLE: {EN: ROLE,
           RU: "роль"},
    COST: {EN: " - Cost: {val}",
           RU: " - Цена: {val}"},
    FREE: {EN: "FREE",
           RU: "БЕСПЛАТНО"}
}

_T = T(locale_dict=_locale)

shopgrp = create_group(SHOP_GROUP, SHOP_GROUP_D, _locale)


@shopgrp.command(
    name=namedesc(BUY_ROLES, _locale),
    description=namedesc(BUY_ROLES_D, _locale),
    extras={IS_OWNER_ONLY: True}
)
async def cmd1(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True, ephemeral=True)
    i = interaction.client.guilds_data.get(interaction.guild.id).get("roles_to_sale")
    stout = "\n".join([f"{k} - {v}" for k, v in i.items()])
    await interaction.followup.send(stout, ephemeral=True)


class ShopView(discord.ui.View):
    roles = None

    def __init__(self, rts):
        super().__init__()
        self.roles_pages = [list(rts.keys())[r:r + 10] for r in range(0, len(list(rts.keys())), 10)]


class PagesEngine:
    pages = []
    current_page = 0
    current_selection = 0

    def __init__(self, items):
        self.pages = [items[r:r + 10] for r in range(0, len(items), 10)]

    def render(self):
        ...


@shopgrp.command(
    name=namedesc(ROLES_INV, _locale),
    description=namedesc(ROLES_INV_D, _locale),
    extras={IS_OWNER_ONLY: True}
)
@app_commands.rename(role=namedesc(ROLE, _locale))
async def cmd2(interaction: discord.Interaction, role: str):
    await interaction.response.defer(thinking=True, ephemeral=True)
    real_role = interaction.guild.get_role(int(role))
    if interaction.user.get_role(int(role)):
        await interaction.user.remove_roles(real_role)
    else:
        await interaction.user.add_roles(real_role)
    await interaction.followup.send("D0ne", ephemeral=True)


@cmd2.autocomplete(ROLE)
async def channel_autocomplite(interaction: discord.Interaction, current: str):
    if rl := interaction.client.guilds_data.get(interaction.guild.id)["users_role_inv"].get(str(interaction.user.id)):
        les = []
        for val in sorted(rl):
            if current in interaction.guild.get_role(int(val)).name:
                les.append(app_commands.Choice(name="@" + interaction.guild.get_role(int(val)).name,
                                               value=val))
        return les[:25]
