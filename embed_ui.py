import discord

view = discord.ui.View()


@discord.ui.button(label="join", style=discord.ButtonStyle.green)
async def join_lobby(self, button: discord.ui.Button, interaction: discord.Interaction):
    await interaction.response.send_message('fuck')


# class Menu(discord.ui.View):
#     def __init__(self):
#         super().__init__()
#         self.value = None

#     @discord.ui.button(label="join", style=discord.ButtonStyle.green)
#     async def join_lobby(self, button: discord.ui.Button, interaction: discord.Interaction):
#         await interaction.response.send_message('fuck')
