import discord
from dang.embeds import ErrorEmbedNameNotFound
from dang.console import WarningDefer
from dang.models.mcuser import MCUser
VERSION = '0.1.3'
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)
# All Points Main Function #
async def main (message, name):
    try:
        await message.defer()
    except:
        WarningDefer('points')
    users = []
    if name == 'Self':
        users = MCUser.select(['dcid', 'name', 'uuid', 'points'], {"dcid": str(message.author.id)})
    else:
        users = MCUser.select(['dcid', 'name', 'uuid', 'points'], {"name": name})
    if len(users) == 0:
        await message.followup.send(content=None, embed=ErrorEmbedNameNotFound(name), ephemeral=True)
        return
    e_title = users[0][1] + '\'s general points'
    e_desc = str(users[0][3]) + ' Points'
    embed = discord.Embed(title=e_title, description=e_desc, color=0xffaa00)
    await message.followup.send(content=None, embed=embed)