import discord
import json
from datetime import datetime, timedelta
from dang.automod.automute import AutoMute
from dang.console import ViolationMsg
from dang.embeds import MemberWarned
from dang.jconfig import GetChannel, GetList
VERSION = "0.5.1"
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)
### Anti Swear ###
def countViolations (warn_list, user_id, warn_type):
    cnt = 0
    for x in warn_list:
        if x['user_id'] == user_id and x['type'] == warn_type:
            cnt += 1
    return cnt
def countActiveWarnings (warn_list, user_id):
    cnt = 0
    c_date = datetime.now()
    for x in warn_list:
        if x['user_id'] == user_id:
            w_date = datetime.strptime(x['expires_at'], "%d/%m/%Y, %H:%M:%S")
            if c_date < w_date:
                cnt += 1
    return cnt
async def main (c_guild : discord.Guild, client, message):
    s = GetList('swears')
    for i in range (0, len(s), 1):
        if str(s[i]) in str(message.content).lower():
            warn_list = json.load(open('warns.json'))
            warn_id = len(warn_list) + 1
            user_id = message.author.id
            user = str(message.author)
            warn_type = 'asw'
            cnt = countViolations(warn_list, user_id, warn_type) + 1
            reason = 'Swearing (' + str(cnt) + ')'
            warned_on = datetime.now()
            duration_mins = 15 * (2 ** (cnt - 1))
            dlt = timedelta(minutes=duration_mins)
            expires_at = warned_on + dlt
            warn_list.append({
                "id": warn_id,
                "user": user,
                "user_id": user_id,
                "type": warn_type,
                "reason": reason,
                "warned_on": warned_on.strftime("%d/%m/%Y, %H:%M:%S"),
                "expires_at": expires_at.strftime("%d/%m/%Y, %H:%M:%S"),
                "moderator": 'dang$$ # ASW'
            })
            with open('warns.json', 'w') as jf:
                json.dump(warn_list, jf, indent=4, separators=(',',': '))
            print(ViolationMsg(user, str(message.content), 'ASW'))
            channel = client.get_channel(int(GetChannel('warnings')))
            await channel.send(content=None, embed=MemberWarned(user, reason, warned_on.strftime("%d/%m/%Y, %H:%M:%S"), expires_at.strftime("%d/%m/%Y, %H:%M:%S"), warn_id, 'dang$$ # ASW'))
            if countActiveWarnings(warn_list, user_id) >= 3:
                await AutoMute(c_guild, client, user, user_id)
            await message.delete()
            msg = 'Do not swear {0.author.mention}!'
            await message.channel.send(content=msg.format(message))