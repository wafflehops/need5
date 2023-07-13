import discord
import os
from discord.ext import tasks
from collections import deque

MAX_LOBBY_SIZE = 5
PERRY_CHANNEL = 1110385416021999707
MY_CHANNEL = 989947070985162795

class MyClient(discord.Client):
    def __init__(self, intents):
        super().__init__(intents=intents)
        self._lobby = set()
        self._queue = deque([])


    async def on_ready(self):
        self.lobby_check.start()
        

    async def on_message(self, message):
        if message.content == '!val':
            await self.add_to_lobby(message)
        
        if message.content == '!cya':
            await self.remove_from_lobby(message)
        
        if message.content == '!clear':
            self._lobby.clear()
            self._queue.clear()
            await message.channel.send('team gone :(')
        
        if message.content == '!lobby':
            await self.print_lobby(message)
        
        if message.content.startswith('!add '):
            print(message.channel.members)
            await message.channel.send('still cookin this')
            # command_index = message.content.find("!")
            # user = message.content[command_index + 5:].strip()
            # await self.add_to_lobby(message, user)
        
        if message.content.startswith('!remove '):
            user = message.content[9:].strip()
            await self.remove_from_lobby(message, user)


    async def add_to_lobby(self, message, manually_added_user = None):
        async def add_to_waiting_room():
            if message.author not in self._queue:
                self._queue.append(message.author)
            else:
                await message.channel.send('keep waiting bud')

        if message.author in self._lobby:
                await message.channel.send('fuck you ur in')
                return

        if len(self._lobby) < MAX_LOBBY_SIZE:
            self._lobby.add(message.author)
        else:
            await add_to_waiting_room()
        
        await self.print_lobby(message)
    

    async def remove_from_lobby(self, message, manual_remove_user = None):
        user = message.author if manual_remove_user == None else \
            [author for author in self._lobby if author.name == manual_remove_user][0]
            # filter(lambda x: x.name == manual_remove_user, self._lobby)
    

        if message.author not in self._lobby and message.author not in self._queue:
            await message.channel.send('fuck off')
            return
        
        if message.author in self._lobby:
            self._lobby.remove(message.author)

            if len(self._queue) > 0:
                next_in_line = self._queue.popleft()
                await next_in_line.send('team')
                self._lobby.add(next_in_line)
        
        if message.author in self._queue:
            self._queue.remove(message.author)

        if len(self._lobby) == 0:
            await message.channel.send('team gone :(')
            return


        await self.print_lobby(message)
    
    async def print_lobby(self, message):
        lobby_formatted = '\n'.join(str(member) for member in self._lobby)
        
        queue_formatted = '\n'.join(f'{index}. {str(member)}' for index, member in enumerate(self._queue, 1))

        if len(self._lobby) > 0:
            await message.channel.send(f'TEAM\n{lobby_formatted}')
        else:
            await message.channel.send('no team :(')

        if len(self._queue) > 0:
            await message.channel.send(f'QUEUE\n{queue_formatted}')
    

    @tasks.loop(minutes=30.0)
    async def lobby_check(self):
        if 1 <= len(self._lobby) and len(self._lobby) < MAX_LOBBY_SIZE:
            channel = self.get_channel(PERRY_CHANNEL)
            
            if len(self._lobby) == MAX_LOBBY_SIZE - 1:
                await channel.send('NEED JUAN')
            else:
                await channel.send(f'{MAX_LOBBY_SIZE-len(self._lobby)} val ')


    @lobby_check.before_loop
    async def before_lobby_check(self):
        await self.wait_until_ready()  


    
intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run('MTEyODc2Mjg2MjAwNTkxMTY4Mw.GljYQP.T9CRHSkAGgqEiBfotc6TwpotH8vk9tVABpOjGk')

