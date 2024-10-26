import discord
from dang.jconfig import GetVersion, GetVersionNames
from dang.console import WarningDefer
VERSION = '0.1.2'
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)
# Bot Command Version Function #
async def main (message):
    try:
        await message.defer()
    except:
        WarningDefer('version')
    verlist = GetVersionNames()
    embed = discord.Embed(title='dang$$ Bot', description='About...', color=0xff0000)
    for i in range(0, len(verlist), 1):
        embed.add_field(name=verlist[i], value=GetVersion(verlist[i]), inline=True)
    await message.followup.send(content=None, embed=embed)