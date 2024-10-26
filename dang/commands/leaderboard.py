import discord
from dang.mccon import GetColor
from dang.models.mcuser import MCUser
from dang.models.minigames import Minigames
VERSION = '0.2.1'
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)
minigames = Minigames.select(orderBy={"id": 1})
# Points Top Main Function
async def main (message : discord.Message, game : str):
    await message.defer()
    game_sel = game.lower()
    player_data : list[dict] = []
    gname = ''
    e_color = 0x000000
    if game_sel == 'general':
        data = MCUser.select(['u.name', 'r.full_name', 'u.points'], join=['MCRank'], orderBy={"u.points": 0})
        player_data = [{'name': i[0], 'rank': i[1], 'score': i[2]} for i in data]
        gname = 'General Table'
        e_color = 0x5555ff
    elif game_sel == 'kills':
        data = MCUser.select(['u.name', 'r.full_name', 'muk.kills'], join=['MCRank', 'MCUserKDR'], orderBy={"muk.kills": 0})
        player_data = [{'name': i[0], 'rank': i[1], 'score': i[2]} for i in data]
        gname = 'Kills'
        e_color = 0x55ff55
    elif game_sel == 'deaths':
        data = MCUser.select(['u.name', 'r.full_name', 'muk.deaths'], join=['MCRank', 'MCUserKDR'], orderBy={"muk.deaths": 0})
        player_data = [{'name': i[0], 'rank': i[1], 'score': i[2]} for i in data]
        gname = 'Deaths'
        e_color = 0xff5555
    elif game_sel == 'kdr':
        data = MCUser.select(['u.name', 'r.full_name', 'muk.kdr'], join=['MCRank', 'MCUserKDR'], orderBy={"muk.kdr": 0})
        player_data = [{'name': i[0], 'rank': i[1], 'score': round(float(i[2]),3)} for i in data]
        gname = 'KDR'
        e_color = 0xff55ff
    else:
        game_idx = 0
        game_found = False
        for game in minigames:
            if game_sel == game[1].lower() or game_sel == game[2].lower() or game_sel == game[3].lower():
                game_found = True
                game_idx = minigames.index(game)
                break
        if not game_found:
            e_title = 'Error! Couldn\'t find a game named ' + game_sel
            embed = discord.Embed(title=e_title, description='It is better to type full name of a game.', color=0xff5555)
            await message.followup.send(content=None, embed=embed, ephemeral=True)
            return
        gname = minigames[game_idx][2]
        e_color = GetColor(minigames[game_idx][4])
        data = MCUser.select(['u.name', 'r.full_name', 'mp.points'], where={"mp.minigame_id": game_idx}, join=['MCRank', 'MinigamesPoints'], orderBy={"mp.points": 0})
        player_data = [{'name': i[0], 'rank': i[1], 'score': i[2]} for i in data]
    e_desc = 'Top 3 Players - ' + gname
    embed = discord.Embed(title='MC.Dingolan.pl', description=e_desc, color=e_color)
    for i in range (0, 3, 1):
        if i < len(player_data):
            ef_title = '#' + str(i+1)
            ef_content = player_data[i]['rank'] + ' ' + player_data[i]['name'] + ' --> ' + str(player_data[i]['score'])
            if gname == 'Kills': ef_content += ' Kills'
            elif gname == 'Deaths': ef_content += ' Deaths'
            elif gname == 'KDR': ef_content += ''
            else: ef_content += ' Points'
            embed.add_field(name=ef_title, value=ef_content, inline=False)
    await message.followup.send(content=None, embed=embed)