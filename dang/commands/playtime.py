import discord
from dang.embeds import ErrorEmbedNameNotFound
from dang.console import WarningDefer
from dang.models.mcuser import MCUser
from dang.models.playtime import Playtime
VERSION = '0.1.3'
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)
# Playtime command #
async def main (message, name):
    try:
        await message.defer()
    except:
        WarningDefer('playtime')
    users = []
    if name == 'Self':
        users = MCUser.select(['dcid', 'name', 'uuid'], {"dcid": str(message.author.id)})
    else:
        users = MCUser.select(['dcid', 'name', 'uuid'], {"name": name})
    if len(users) == 0:
        await message.followup.send(content=None, embed=ErrorEmbedNameNotFound(name), ephemeral=True)
        return
    result = Playtime.select(['hours'], {"uuid": users[0][2], "server_id": 3})[0]
    e_title = users[0][1] + '\'s Minigames playtime'
    e_desc = str(result[0]) + ' Hours'
    embed = discord.Embed(title=e_title, description=e_desc, color=0xefef22)
    await message.followup.send(content=None, embed=embed)