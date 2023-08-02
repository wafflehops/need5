import discord
import os
from discord.ext import tasks
from bot.views import need5_view
from data.lobby import lobby, join_times

def setup_events(bot):
    @bot.event
    async def on_ready():
        channel = bot.get_channel(int(os.getenv('GUI_CHANNEL')))

        await channel.purge(limit=100, check=lambda message: message.author == bot.user)
        await channel.send(view=need5_view())
    
    # @tasks.loop(seconds=5.0)
    # async def auto_kick():
    #     channel = bot.get_channel(int(os.getenv('GUI_CHANNEL')))
    #     await channel.send('1111')
    
    # @auto_kick.before_loop
    # async def before_auto_kick():
    #     print('waiting...')
    #     await bot.wait_until_ready()
    
    
    






