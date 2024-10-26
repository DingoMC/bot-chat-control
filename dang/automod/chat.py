import discord
import json
import os
from dang.embeds import ErrorEmbedNameNotFound
from dang.mcapi import GetNameByUUID
from dang.models.mcuser import MCUser
from dang.mccon import GetJSONColor

VERSION = "0.1.0"
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)

async def sendIngameMessage (c_guild : discord.Guild, client, message : discord.Message):
    user_data = MCUser.select(['dcid', 'mcuuid', 'prefix', 'staff_rank_id'], {"dcid": str(message.author.id)})[0]
    user_name = GetNameByUUID(user_data[1])
    if user_name not in list(map(GetNameByUUID, [row[0] for row in MCUser.select(['mcuuid'])])):
        await message.delete()
        return
    name_color = GetJSONColor(str(user_data[2]))
    staff_rank = str(user_data[3])
    msg_default_color = 'white'
    content = str(message.content)
    content = content.replace('\u000A', ' ') # Replace new line with space
    content = content.replace('\\', '')
    content = content.replace('$', '')
    content = content.replace('"', '\'')
    # Colored chat is only for staff
    if len(staff_rank) == 0:
        content = content.replace('§', '')
    if len(content) == 0:
        await message.delete()
        return
    if staff_rank == '4':
        msg_default_color = 'gold'
    if staff_rank == '3':
        msg_default_color = 'red'
    if staff_rank == '2':
        msg_default_color = 'aqua'
    if staff_rank == '1':
        msg_default_color = 'yellow'
    mc_cmd = 'tellraw @a [{"text":"\u00A78[\u00A79DC\u00A78]\u00A7r "},{"text":"' + user_name + '","color":"' + name_color + '"},{"text":" » "},{"text":"' + content + '","color":"' + msg_default_color + '"}]'
    fifo_cmd = 'echo "$(printf \'%s\' \'' + mc_cmd + '\')" > /root/minecraft_m/server_input'
    os.system(fifo_cmd)
    return
    