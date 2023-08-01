import discord
from discord.ui import Button, View
from bot.commands import (
    add_to_lobby,
    remove_from_lobby,
    clear_lobby,
    kiss_the_homies,
    notify,
)


def need5_view():
    join_button = Button(label='Join', style=discord.ButtonStyle.green)
    join_button.callback = add_to_lobby

    leave_button = Button(label='Leave', style=discord.ButtonStyle.red)
    leave_button.callback = remove_from_lobby

    disband_button = Button(label='Disband', style=discord.ButtonStyle.grey)
    disband_button.callback = clear_lobby

    kiss_homies_button = Button(
        label='Kiss the homies', style=discord.ButtonStyle.blurple)
    kiss_homies_button.callback = kiss_the_homies

    notify_button = Button(label='notify', style=discord.ButtonStyle.blurple)
    notify_button.callback = notify

    view = View()

    view.add_item(join_button)
    view.add_item(leave_button)
    view.add_item(disband_button)
    view.add_item(kiss_homies_button)
    view.add_item(notify_button)

    view.timeout = None

    return view