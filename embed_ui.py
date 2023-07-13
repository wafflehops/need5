import discord


async def embed(ctx):
    embed = discord.Embed(title="Sample Embed", url="https://realdrewdata.medium.com/",
                          description="This is an embed that will show how to build an embed and the different components", color=0xFF5733)
    await ctx.send(embed=embed)
