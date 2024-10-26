import discord
import json
from datetime import datetime, timedelta
from dang.jconfig import GetChannel
from dang.embeds import MemberMuted
from dang.console import WarningDefer
VERSION = '0.1.1'
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)

## Convert Duration String to Time Delta 
def ConvertDurationToDelta (duration : str):
    days = 0
    hours = 0
    minutes = 0
    seconds = 0
    chr = list(duration)
    num_str = ''
    for i in chr:
        if i.isdigit(): num_str += i
        elif i == 'd':
            days += int(num_str)
            num_str = ''
        elif i == 'h':
            hours += int(num_str)
            num_str = ''
        elif i == 'm':
            minutes += int(num_str)
            num_str = ''
        elif i == 's':
            seconds += int(num_str)
            num_str = ''
    return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)

# Bot Command Warn Function #
async def main (c_guild : discord.Guild, client, message : discord.Message, w_user : discord.User, duration : str, reason : str):
    try:
        await message.defer()
    except:
        WarningDefer('mute')
    mute_list = json.load(open('mutes.json'))
    mute_id = len(mute_list) + 1
    user_id = w_user.id
    user = str(w_user.name) + '#' + str(w_user.discriminator)
    mute_type = 'manual'
    muted_on = datetime.now()
    dlt = ConvertDurationToDelta(duration)
    expires_at = muted_on + dlt
    mute_list.append({
        "id": mute_id,
        "user": user,
        "user_id": user_id,
        "type": mute_type,
        "reason": 'Reached 3 active warnings',
        "muted_on": muted_on.strftime("%d/%m/%Y, %H:%M:%S"),
        "expires_at": expires_at.strftime("%d/%m/%Y, %H:%M:%S"),
        "moderator": str(message.author)
    })
    with open('mutes.json', 'w') as jf:
        json.dump(mute_list, jf, indent=4, separators=(',',': '))
    member : discord.Member = await c_guild.fetch_member(int(user_id))
    await member.timeout_for(dlt)
    channel = client.get_channel(int(GetChannel('mutes')))
    await channel.send(content=None, embed=MemberMuted(user, reason, muted_on.strftime("%d/%m/%Y, %H:%M:%S"), expires_at.strftime("%d/%m/%Y, %H:%M:%S"), mute_id, str(message.author)))
    msg = '{0.author.mention} Member muted successfully!'
    await message.followup.send(content=msg.format(message), ephemeral=True)

