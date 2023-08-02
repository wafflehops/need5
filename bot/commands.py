import os
import discord
import datetime
from data.lobby import lobby, join_times, MAX_LOBBY_SIZE
from utils.helper_functions import is_notification


async def add_to_lobby(interaction):
    user = interaction.user

    if len(lobby) < MAX_LOBBY_SIZE:
        lobby.add(user)
        join_times[user] = interaction.created_at

    await interaction.response.edit_message(embeds=generate_lobby(lobby))

    await interaction.channel.purge(limit=1, check=is_notification)

    if len(lobby) < MAX_LOBBY_SIZE:
        await interaction.channel.send(f'need {MAX_LOBBY_SIZE - len(lobby)} val')
    else:
        for homie in lobby:
            await homie.send(f'ASSEMBLE')



async def remove_from_lobby(interaction):
    user = interaction.user

    if user in lobby:
        lobby.remove(user)
        join_times.pop(user)

    await interaction.response.edit_message(embeds=generate_lobby(lobby))

    await interaction.channel.purge(limit=1, check=is_notification)

    if len(lobby) > 0:
            await interaction.channel.send(f'need {MAX_LOBBY_SIZE - len(lobby)} val')


def generate_lobby(lobby):
    if not lobby:
        return [discord.Embed(
            title=f'no team :(', colour=discord.Colour.random())]

    embeds = []

    for user in lobby:
        embed = discord.Embed(
            title=f'{user.display_name}', colour=discord.Colour.random())

        embed.set_thumbnail(url=user.display_avatar)
        

        embed.timestamp = join_times[user]
        embeds.append(embed)

    return embeds


async def clear_lobby(interaction):
    lobby.clear()

    await interaction.response.edit_message(embeds=generate_lobby(lobby))
    await interaction.channel.purge(limit=1, check=is_notification)


async def kiss_the_homies(interaction):
    from_user = interaction.user.display_name

    for homie in lobby:
        await homie.send(f'from {from_user}: :kissing_heart:')

    await interaction.response.defer()


async def notify(interaction):
    if len(lobby) != MAX_LOBBY_SIZE:
        await interaction.channel.purge(limit=1, check=is_notification)
        await interaction.channel.send(f'need {MAX_LOBBY_SIZE - len(lobby)} val')

    await interaction.response.defer()
    

