import discord
import json
from datetime import datetime, timedelta
from dang.automod.automute import AutoMute
from dang.jconfig import GetChannel
from dang.embeds import MemberWarned
from dang.console import WarningDefer
VERSION = '0.1.2'
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

def countActiveWarnings (warn_list, user_id):
    cnt = 0
    c_date = datetime.now()
    for x in warn_list:
        if x['user_id'] == user_id:
            w_date = datetime.strptime(x['expires_at'], "%d/%m/%Y, %H:%M:%S")
            if c_date < w_date:
                cnt += 1
    return cnt

# Bot Command Warn Function #
async def main (c_guild : discord.Guild, client, message : discord.Message, w_user : discord.User, duration : str, reason : str):
    try:
        await message.defer()
    except:
        WarningDefer('warn')
    warn_list = json.load(open('warns.json'))
    warn_id = len(warn_list) + 1
    user_id = w_user.id
    user = str(w_user.name) + '#' + str(w_user.discriminator)
    warn_type = 'manual'
    warned_on = datetime.now()
    dlt = ConvertDurationToDelta(duration)
    expires_at = warned_on + dlt
    warn_list.append({
        "id": warn_id,
        "user": user,
        "user_id": user_id,
        "type": warn_type,
        "reason": reason,
        "warned_on": warned_on.strftime("%d/%m/%Y, %H:%M:%S"),
        "expires_at": expires_at.strftime("%d/%m/%Y, %H:%M:%S"),
        "moderator": str(message.author)
    })
    with open('warns.json', 'w') as jf:
        json.dump(warn_list, jf, indent=4, separators=(',',': '))
    channel = client.get_channel(int(GetChannel('warnings')))
    await channel.send(content=None, embed=MemberWarned(user, reason, warned_on.strftime("%d/%m/%Y, %H:%M:%S"), expires_at.strftime("%d/%m/%Y, %H:%M:%S"), warn_id, str(message.author)))
    if countActiveWarnings(warn_list, user_id) >= 3:
        await AutoMute(c_guild, client, user, user_id)
    msg = '{0.author.mention} Member warned successfully!'
    await message.followup.send(content=msg.format(message), ephemeral=True)

