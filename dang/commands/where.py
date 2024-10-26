from dang.embeds import ErrorEmbedNameNotFound
from dang.console import ErrorServerInfo, WarningDefer
from dang.models.mcuser import MCUser
from dang.models.minigames_subserver import MinigamesSubServer
from dang.models.mcserverinfo import MCServerInfo
from dang.models.mcuser_location import MCUserLocation

VERSION = '0.2.1'
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)

# Where Main Function #
async def main (message, name):
    try:
        await message.defer()
    except:
        WarningDefer('where')
    users = []
    if name == 'Self':
        users = MCUser.select(['dcid', 'name', 'uuid'], {"dcid": str(message.author.id)})
    else:
        users = MCUser.select(['dcid', 'name', 'uuid'], {"name": name})
    if len(users) == 0:
        await message.followup.send(content=None, embed=ErrorEmbedNameNotFound(name), ephemeral=True)
        return
    location = MCUserLocation.select(['subserver', 'updated_on'], {"uuid": users[0][2], "server_id": 3})
    if len(location) == 0:
        msg = 'Couldn\'t find location data for player ' + users[0][1]
        await message.followup.send(content=msg.format(message))
        return
    if int(location[0][0]) == -2147483647:
        msg = 'Couldn\'t find location data for player ' + users[0][1]
        await message.followup.send(content=msg.format(message))
        return
    srv_info = MCServerInfo.select(['sample'], {"dns": 'dingo-mc.net'})
    is_online = False
    is_online_str = ''
    if len(srv_info) == 0:
        print(ErrorServerInfo())
    else:
        sample = str(srv_info[0][0]).split(',')
        if str(users[0][1]) in sample:
            is_online = True
    if int(location[0][0]) == -1:
        if is_online:
            msg = 'Player ' + users[0][1] + ' is nowhere. Maybe fell into void.'
        else:
            msg = 'Player ' + users[0][1] + ' last time logged off from nowhere. Maybe fell into void.'
        await message.followup.send(content=msg.format(message))
        return
    if is_online:
        is_online_str = ' is on '
    else:
        is_online_str = ' last time logged off from '
    server_name = MinigamesSubServer.select(['name'], {"id": int(location[0][0])})[0][0]
    msg = 'Player ' + users[0][1] + is_online_str + '**' + server_name + '** (03M_' + str(location[0][0]) + ')'
    await message.followup.send(content=msg.format(message))
    return
        