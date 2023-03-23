import discord
from discord import app_commands
from discord.app_commands import locale_str as _ls

from translator.main import T

locale = {
    'ping': {
        'en': 'Pong',
        'ru': 'Понг'
    },
    'user': {
        'en': 'User',
        'ru': 'Пользователь'
    },
    'zeroload': {
        'en': 'No load',
        'ru': 'Нет нагрузки'
    },
    'cycle': {
        'en': 'Cycle',
        'ru': 'Цикл'
    },
    'load': {
        'en': 'Load',
        'ru': 'Нагрузка'
    },
    'overloaded': {
        'en': 'Overloaded',
        'ru': 'Перегружен'
    },
    'yes': {
        'en': 'Yes',
        'ru': 'Да'
    },
    'no': {
        'en': 'No',
        'ru': 'Нет'
    }
}

_T = T(locale_dict=locale)

grp_lc = {
    'test_name': {
        'en': 'test',
        'ru': 'тест'
    },
    'test_desc': {
        'en': 'Experemental commands!',
        'ru': 'Эксперементальные комманды!'
    }
}

test_grp = app_commands.Group(
    name=_ls(
        'test_name',
        extras={
            'dict': grp_lc.get('test_name'),
            'type': 'cmd'
        }
    ),
    description=_ls(
        'test_desc',
        extras={
            'dict': grp_lc.get('test_desc'),
            'type': 'cmd'
        }
    )
)

test_lc = {
    'ping_name': {
        'en': 'ping',
        'ru': 'пинг'
    },
    "ping_desc": {
        'en': 'Checks if the bot is running.',
        'ru': 'Проверяет, работает ли бот.'
    }
}


@test_grp.command(
    name=_ls(
        'ping_name',
        extras={
            'dict': test_lc.get('ping_name'),
            'type': 'cmd'
        }
    ),
    description=_ls(
        'ping_desc',
        extras={
            'dict': test_lc.get('ping_desc'),
            'type': 'cmd'
        }
    )
)
async def ping(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    _T.set_locale(locale=interaction.locale)
    _T.set_string(string=_ls("ping"))
    await interaction.followup.send(_T.stranslate())


chk_engine_lc = {
    'chk_engine_name': {
        'en': 'check_status',
        'ru': 'проверить_статус'
    },
    "chk_engine_desc": {
        'en': 'Check current cycle and load.',
        'ru': 'Проверить текущий цикл и нагрузку.'
    }
}


@test_grp.command(
    name=_ls(
        'chk_engine_name',
        extras={
            'dict': chk_engine_lc.get('chk_engine_name'),
            'type': 'cmd'
        }
    ),
    description=_ls(
        'chk_engine_desc',
        extras={
            'dict': chk_engine_lc.get('chk_engine_desc'),
            'type': 'cmd'
        }
    ),
    extras={'system': True}
)
async def chk_engine(interaction: discord.Interaction):
    await interaction.response.defer(thinking=True)
    # Я сделал отдельные функции для усатновки языка и строки для перевода, что бы это было удобнее читать.
    # Нечитаемо, но компактно или читаемо, но громоздко? Я выбрал второе.
    _T.set_locale(locale=interaction.locale)
    _T.set_string(string=_ls("zeroload"))
    _zeroload = _T.stranslate()
    _T.set_string(string=_ls("user"))
    _user_lc = _T.stranslate()
    _T.set_string(string=_ls("cycle"))
    _cycle = _T.stranslate()
    _T.set_string(string=_ls("load"))
    _load = _T.stranslate()
    _T.set_string(string=_ls("overloaded"))
    _overl = _T.stranslate()
    _T.set_string(string=_ls("yes"))
    _y = _T.stranslate()
    _T.set_string(string=_ls("no"))
    _n = _T.stranslate()
    stout = []
    for _id, _user in interaction.client.antispam.items():
        stout.append(
            f'({_user_lc}: {_id}) '
            f'({_cycle}: {round(interaction.client.heart.cycle, 1)}) '
            f'({_load}: {round(_user.get("overload"))}) '
            f'({_overl}: {f"{_y})" if _user.get("overloaded") else f"{_n})"}'
        )
    if stout:
        await interaction.followup.send("\n".join(stout))
    else:
        await interaction.followup.send(f'({_zeroload}!) '
                                        f'({_cycle}: {round(interaction.client.heart.cycle, 1)})')
