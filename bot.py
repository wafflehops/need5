import discord
import os
from discord.ext import tasks, commands
from collections import deque
from dotenv import load_dotenv
from discord.ui import Button, View

load_dotenv()

MAX_LOBBY_SIZE = 5

PERRY_CHANNEL = 1110385416021999707
UI_CHANNEL = 1129462597087924265

MY_CHANNEL = 989947070985162795
OTHER_CHANNEL = 1129428972715901102


# class MyClient(discord.Client):
#     def __init__(self, intents):
#         super().__init__(intents=intents)
#         self._lobby = set()
#         self._queue = deque([])

#     async def on_ready(self):
#         self.lobby_check.start()

#     async def on_message(self, message):
#         if message.content == '!val':
#             await self.add_to_lobby(message)

#         if message.content == '!cya':
#             await self.remove_from_lobby(message)

#         if message.content == '!clear':
#             self._lobby.clear()
#             self._queue.clear()
#             await message.channel.send('team gone :(')

#         if message.content == '!lobby':
#             await self.print_lobby(message)

#     async def add_to_lobby(self, message, manually_added_user=None):
#         async def add_to_waiting_room():
#             if message.author not in self._queue:
#                 self._queue.append(message.author)
#             else:
#                 await message.channel.send('keep waiting bud')

#         if message.author in self._lobby:
#             await message.channel.send('fuck you ur in')
#             return

#         if len(self._lobby) < MAX_LOBBY_SIZE:
#             self._lobby.add(message.author)
#         else:
#             await add_to_waiting_room()

#         await self.print_lobby(message)

#     async def remove_from_lobby(self, message, manual_remove_user=None):
#         if message.author not in self._lobby and message.author not in self._queue:
#             await message.channel.send('fuck off')
#             return

#         if message.author in self._lobby:
#             self._lobby.remove(message.author)

#             if len(self._queue) > 0:
#                 next_in_line = self._queue.popleft()
#                 await next_in_line.send('team')
#                 self._lobby.add(next_in_line)

#         if message.author in self._queue:
#             self._queue.remove(message.author)

#         if len(self._lobby) == 0:
#             await message.channel.send('team gone :(')
#             return

#         await self.print_lobby(message)

#     async def print_lobby(self, message):
#         lobby_formatted = '\n'.join(str(member) for member in self._lobby)

#         queue_formatted = '\n'.join(
#             f'{index}. {str(member)}' for index, member in enumerate(self._queue, 1))

#         if len(self._lobby) > 0:
#             await message.channel.send(f'TEAM\n{lobby_formatted}')
#         else:
#             await message.channel.send('no team :(')

#         if len(self._queue) > 0:
#             await message.channel.send(f'QUEUE\n{queue_formatted}')

#     @tasks.loop(minutes=30.0)
#     async def lobby_check(self):
#         if 1 <= len(self._lobby) and len(self._lobby) < MAX_LOBBY_SIZE:
#             channel = self.get_channel(MY_CHANNEL)

#             if len(self._lobby) == MAX_LOBBY_SIZE - 1:
#                 await channel.send('NEED JUAN')
#             else:
#                 await channel.send(f'{MAX_LOBBY_SIZE-len(self._lobby)} val ')

#     @lobby_check.before_loop
#     async def before_lobby_check(self):
#         await self.wait_until_ready()


intents = discord.Intents.default()
intents.message_content = True

# client = MyClient(intents=intents)


# client.run(os.getenv('TOKEN'))

bot = commands.Bot(command_prefix='suckme', intents=intents)

lobby = set()
queue = deque([])


async def add_to_lobby(interaction):
    user = interaction.user

    if len(lobby) < MAX_LOBBY_SIZE:
        lobby.add(user)

        channel = bot.get_channel(PERRY_CHANNEL)

        if len(lobby) < MAX_LOBBY_SIZE:
            await channel.send(f'need {MAX_LOBBY_SIZE - len(lobby)} val')

    await interaction.response.edit_message(embeds=generate_lobby(lobby))


async def remove_from_lobby(interaction):
    user = interaction.user

    if user in lobby:
        lobby.remove(user)

        channel = bot.get_channel(PERRY_CHANNEL)

        if len(lobby) > 0:
            await channel.send(f'need {MAX_LOBBY_SIZE - len(lobby)} val')

    await interaction.response.edit_message(embeds=generate_lobby(lobby))


def generate_lobby(lobby):
    if not lobby:
        return [discord.Embed(
            title=f'no team :(', colour=discord.Colour.random())]

    embeds = []

    for user in lobby:
        embed = discord.Embed(
            title=f'{user.display_name}', colour=discord.Colour.red())

        embed.set_thumbnail(url=user.display_avatar)

        embeds.append(embed)

    return embeds


async def clear_lobby(interaction):
    lobby.clear()
    await interaction.response.edit_message(embeds=generate_lobby(lobby))


async def kiss_the_homies(interaction):
    for homie in lobby:
        await homie.send(':kissing_heart:')

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

    view = View()

    view.add_item(join_button)
    view.add_item(leave_button)
    view.add_item(disband_button)
    view.add_item(kiss_homies_button)

    view.timeout = None

    return view


# @tasks.loop(minutes=30.0)
# async def lobby_check():
#     print('hey')
#     if 1 <= len(lobby) and len(lobby) < MAX_LOBBY_SIZE:
#         channel = bot.get_channel(MY_CHANNEL)
#         if len(lobby) == MAX_LOBBY_SIZE - 1:
#             await channel.send('NEED JUAN')
#         else:
#             await channel.send(f'{MAX_LOBBY_SIZE-len(lobby)} val ')


# @lobby_check.before_loop
# async def before_lobby_check():
#     await bot.wait_until_ready()


@bot.event
async def on_ready():
    def is_me(m):
        return m.author == bot.user

    channel = bot.get_channel(UI_CHANNEL)

    await channel.purge(limit=1, check=is_me)
    await channel.send(view=display_buttons())

    # lobby_check.start()


bot.run(os.getenv('TOKEN'))
