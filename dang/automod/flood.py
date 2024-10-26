import discord
import json
from datetime import datetime, timedelta
from dang.automod.automute import AutoMute
from dang.console import ViolationMsg
from dang.embeds import MemberWarned
from dang.jconfig import GetChannel
VERSION = "0.2.0"
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
    l = 1
    maxl = 1
    for i in range (1, len(str(message.content)), 1):
        chk = str(message.content).lower()
        if chk[i] == chk[i-1]:
            l += 1
            if l > maxl: maxl = l
        else: l = 1
        if maxl >= 7: break
    if maxl >= 7:
        warn_list = json.load(open('warns.json'))
        warn_id = len(warn_list) + 1
        user_id = message.author.id
        user = str(message.author)
        warn_type = 'afl'
        cnt = countViolations(warn_list, user_id, warn_type) + 1
        reason = 'Spamming (' + str(cnt) + ')'
        warned_on = datetime.now()
        duration_mins = 5 * (2 ** (cnt - 1))
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
            "moderator": 'dang$$ # AFL'
        })
        with open('warns.json', 'w') as jf:
            json.dump(warn_list, jf, indent=4, separators=(',',': '))
        print(ViolationMsg(user, str(message.content), 'AFL'))
        channel = client.get_channel(int(GetChannel('warnings')))
        await channel.send(content=None, embed=MemberWarned(user, reason, warned_on.strftime("%d/%m/%Y, %H:%M:%S"), expires_at.strftime("%d/%m/%Y, %H:%M:%S"), warn_id, 'dang$$ # AFL'))
        if countActiveWarnings(warn_list, user_id) >= 3:
            await AutoMute(c_guild, client, user, user_id)
        await message.delete()
        msg = 'Do not flood {0.author.mention}!'
        await message.channel.send(content=msg.format(message))