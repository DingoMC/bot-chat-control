import discord
import json
from datetime import datetime, timedelta
from dang.embeds import MemberMuted
from dang.jconfig import GetChannel
VERSION = "0.1.0"
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)
def getOldestExpiryDate (warn_list, user_id):
    c_date = datetime.now()
    latest_e_date = None
    for x in warn_list:
        if x['user_id'] == user_id:
            w_date = datetime.strptime(x['expires_at'], "%d/%m/%Y, %H:%M:%S")
            if c_date < w_date:
                if latest_e_date == None:
                    latest_e_date = w_date
                elif w_date < latest_e_date:
                    latest_e_date = w_date
    return latest_e_date
async def AutoMute (c_guild : discord.Guild, client, user, user_id):
    warn_list = json.load(open('warns.json'))
    exp_date = getOldestExpiryDate(warn_list, user_id)
    mute_length : timedelta = exp_date - datetime.now()
    mute_list = json.load(open('mutes.json'))
    mute_id = len(mute_list) + 1
    muted_on = datetime.now()
    mute_list.append({
        "id": mute_id,
        "user": user,
        "user_id": user_id,
        "type": 'auto',
        "reason": 'Reached 3 active warnings',
        "muted_on": muted_on.strftime("%d/%m/%Y, %H:%M:%S"),
        "expires_at": exp_date.strftime("%d/%m/%Y, %H:%M:%S"),
        "moderator": 'dang$$'
    })
    with open('mutes.json', 'w') as jf:
        json.dump(mute_list, jf, indent=4, separators=(',',': '))
    member : discord.Member = await c_guild.fetch_member(int(user_id))
    await member.timeout_for(mute_length)
    channel = client.get_channel(int(GetChannel('mutes')))
    await channel.send(content=None, embed=MemberMuted(user, 'Reached 3 active warnings', muted_on.strftime("%d/%m/%Y, %H:%M:%S"), exp_date.strftime("%d/%m/%Y, %H:%M:%S"), mute_id, 'dang$$'))