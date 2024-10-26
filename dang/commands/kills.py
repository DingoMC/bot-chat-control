import discord
from dang.embeds import ErrorEmbedNameNotFound
from dang.console import WarningDefer
from dang.models.mcuser import MCUser
from dang.models.mcuser_kdr import MCUserKDR
from dang.utils import CurrentTime
VERSION = '0.2.2'
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)
# Kills command #
async def main (message, name):
    try:
        await message.defer()
    except:
        WarningDefer('kills')
    users = []
    if name == 'Self':
        users = MCUser.select(['dcid', 'name', 'uuid'], {"dcid": str(message.author.id)})
    else:
        users = MCUser.select(['dcid', 'name', 'uuid'], {"name": name})
    if len(users) == 0:
        await message.followup.send(content=None, embed=ErrorEmbedNameNotFound(name), ephemeral=True)
        return
    result = MCUserKDR.select(['kills', 'updated_on'], {"uuid": users[0][2], "server_id": 3})[0]
    e_title = users[0][1] + '\'s kills'
    e_desc = str(result[0]) + ' Kills'
    embed = discord.Embed(title=e_title, description=e_desc, color=0x00aa00)
    ef_text = 'Last Update: ' + CurrentTime(str(result[1]))
    embed.set_footer(text=ef_text)
    await message.followup.send(content=None, embed=embed)
