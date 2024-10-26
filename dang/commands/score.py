import discord
from dang.mccon import GetColor
from dang.embeds import ErrorEmbedNameNotFound
from dang.console import WarningDefer
from dang.models.mcuser import MCUser
from dang.models.minigames import Minigames
from dang.models.minigames_points import MinigamesPoints
VERSION = '0.2.3'
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)
minigames = Minigames.select(orderBy={"id": 1})
# Games Scores #
async def main (message, game, name):
    try:
        await message.defer()
    except:
        WarningDefer('score')
    game_idx = 0
    game_sel = game.lower()
    game_found = False
    for g in minigames:
        if game_sel == g[1].lower() or game_sel == g[2].lower() or game_sel == g[3].lower():
            game_found = True
            game_idx = minigames.index(g)
            break
    if not game_found:
        e_title = 'Error! Couldn\'t find a game named ' + game_sel
        embed = discord.Embed(title=e_title, description='It is better to type full name of a game.', color=0xff5555)
        await message.followup.send(content=None, embed=embed, ephemeral=True)
        return
    gname = minigames[game_idx][2]
    e_color = GetColor(minigames[game_idx][4])
    users = []
    if name == 'Self':
        users = MCUser.select(['dcid', 'name', 'uuid'], {"dcid": str(message.author.id)})
    else:
        users = MCUser.select(['dcid', 'name', 'uuid'], {"name": name})
    if len(users) == 0:
        await message.followup.send(content=None, embed=ErrorEmbedNameNotFound(name), ephemeral=True)
        return
    result = MinigamesPoints.select(['points'], {"uuid": users[0][2], "minigame_id": game_idx})
    e_desc = 'No score found'
    e_title = users[0][1] + '\'s ' + gname + ' score'
    if len(result) > 0:
        e_desc = str(result[0][0]) + ' Points'
    embed = discord.Embed(title=e_title, description=e_desc, color=e_color)
    await message.followup.send(content=None, embed=embed)