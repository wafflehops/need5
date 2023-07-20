import discord
import os
from discord.ext import commands
from collections import deque
from dotenv import load_dotenv
from discord.ui import Button, View

load_dotenv()

MAX_LOBBY_SIZE = 5

PERRY_CHANNEL = 1110385416021999707
UI_CHANNEL = 1129462597087924265

MY_CHANNEL = 989947070985162795
OTHER_CHANNEL = 1129428972715901102


intents = discord.Intents.default()
intents.message_content = True


bot = commands.Bot(command_prefix='suckme', intents=intents)

lobby = set()
queue = deque([])


def is_me(m):
    return m.author == bot.user


async def add_to_lobby(interaction):
    user = interaction.user

    if len(lobby) < MAX_LOBBY_SIZE:
        lobby.add(user)

        channel = bot.get_channel(PERRY_CHANNEL)

        if len(lobby) < MAX_LOBBY_SIZE:
            # await channel.purge(limit=100, check=is_me)
            await channel.send(f'need {MAX_LOBBY_SIZE - len(lobby)} val')

    await interaction.response.edit_message(embeds=generate_lobby(lobby))


async def remove_from_lobby(interaction):
    user = interaction.user

    if user in lobby:
        lobby.remove(user)

        channel = bot.get_channel(PERRY_CHANNEL)

        if len(lobby) > 0:
            # await channel.purge(limit=100, check=is_me)
            await channel.send(f'need {MAX_LOBBY_SIZE - len(lobby)} val')

    await interaction.response.edit_message(embeds=generate_lobby(lobby))


def generate_lobby(lobby):
    if not lobby:
        return [discord.Embed(
            title=f'no team :(', colour=discord.Colour.random())]

    embeds = []

    for user in lobby:
        embed = discord.Embed(
            title=f'{user.display_name}', colour=discord.Colour.random())

        embed.set_thumbnail(url=user.display_avatar)

        embeds.append(embed)

    return embeds


async def clear_lobby(interaction):
    lobby.clear()
    await interaction.response.edit_message(embeds=generate_lobby(lobby))


async def kiss_the_homies(interaction):
    from_user = interaction.user.display_name
    for homie in lobby:
        await homie.send(f'from {from_user}: :kissing_heart:')

    await interaction.response.defer()


async def notify(interaction):
    channel = bot.get_channel(PERRY_CHANNEL)

    await channel.send(f'need {MAX_LOBBY_SIZE - len(lobby)} val')

    await interaction.response.defer()


def display_buttons():
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


@bot.event
async def on_ready():
    channel = bot.get_channel(UI_CHANNEL)

    await channel.purge(limit=1, check=is_me)
    await channel.send(view=display_buttons())


bot.run(os.getenv('TOKEN'))
