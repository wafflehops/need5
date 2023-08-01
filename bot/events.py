import discord
import os
from bot.views import need5_view

def setup_events(bot):
    @bot.event
    async def on_ready():
        channel = bot.get_channel(int(os.getenv('GUI_CHANNEL')))

        await channel.purge(limit=2, check=lambda message: message.author == bot.user)
        await channel.send(view=need5_view())
