import discord
from datetime import datetime, timedelta
from dang.console import WarningDMNotAllowed, WarningDefer
from dang.mcapi import GetUUIDByName, GetNameByUUID
from dang.models.mcuser import MCUser
from dang.models.punishments import Punishments

VERSION = '0.2.1'
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
async def main (guild : discord.Guild, message : discord.Message, w_user : str, duration : str, reason : str):
    try:
        await message.defer()
    except:
        WarningDefer('mcwarn')
    user = MCUser.select(['uuid', 'dcid'], {"mcuuid": GetUUIDByName(w_user)})[0]
    p_mod = GetNameByUUID(MCUser.select(['mcuuid'], {"dcid": str(message.author.id)})[0][0])
    user_dm = await guild.fetch_member(user[1])
    c_date = datetime.now()
    p_date = c_date.strftime("%d.%m.%Y, %H:%M")
    exp_date = c_date + ConvertDurationToDelta(duration)
    warn_id = Punishments.insert('Warn', user[0], p_mod, reason, c_date, 'MC.Dingolan Minigames', expires=exp_date)[0][0]
    p_exp = exp_date.strftime("%d.%m.%Y, %H:%M")
    msg = '{0.author.mention} Player warned successfully! Warning ID: ' + str(warn_id)
    await message.followup.send(content=msg.format(message), ephemeral=True)
    embed = discord.Embed(title='MC.Dingolan.pl', description="Minecraft Warning", color=0xff4423)
    try:
        embed.add_field(name='#' + str(warn_id) + ' Warn by ' + p_mod, value='Reason: ' + reason + '\nWarned on: ' + p_date + '\nExpires on: ' + p_exp, inline=False)
        await user_dm.send(content=None, embed=embed)
    except:
        WarningDMNotAllowed(user[1])
    return
