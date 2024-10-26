import discord
from dang.jconfig import GetObject
from dang.console import GetExternalIP, WarningDefer
VERSION = '0.1.2'
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)
# ip function #
async def main (message):
    try:
        await message.defer()
    except:
        WarningDefer('ip')
    embed = discord.Embed(title='MC.Dingolan.pl', description='Current IPs', color=0xffbb22)
    embed.add_field(name='For Internal Players', value=GetObject('iplocal'), inline=False)
    embed.add_field(name='For Everyone', value=GetExternalIP(), inline=False)
    await message.followup.send(content=None, embed=embed)