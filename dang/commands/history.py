import discord
from datetime import datetime
from dang.embeds import ErrorEmbedNameNotFound, PageFooter
from dang.console import WarningDefer
from dang.models.mcuser import MCUser
from dang.models.punishments import Punishments
VERSION = '0.1.2'
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)
def IsActiveStr (expires : datetime):
    c_date = datetime.now()
    dlt = c_date - expires
    if dlt.total_seconds() > 0:
        return ' (Expired)'
    return ' (Active)'

def IsActiveE (expires : datetime):
    c_date = datetime.now()
    dlt = c_date - expires
    if dlt.total_seconds() > 0:
        return '\nExpired on: '
    return '\nExpires on: '
    
def IsKick (p_type : str):
    return p_type == 'Kick'
    
# History Main Function #
async def main (message, name : str, page : int):
    try:
        await message.defer()
    except:
        WarningDefer('history')
    users = []
    if name == 'Self':
        users = MCUser.select(['dcid', 'name', 'uuid'], {"dcid": str(message.author.id)})
    else:
        users = MCUser.select(['dcid', 'name', 'uuid'], {"name": name})
    if len(users) == 0:
        await message.followup.send(content=None, embed=ErrorEmbedNameNotFound(name), ephemeral=True)
        return
    history = Punishments.select(where={"player": users[0][2]})
    p = 3
    pages = len(history) // p
    if len(history) % p != 0: pages += 1
    cur_page = page
    if page > pages: cur_page = pages
    if page <= 0: cur_page = 1
    e_desc = 'Punishments of ' + users[0][1]
    embed = discord.Embed(title='MC.Dingolan.pl', description=e_desc, color=0xff4423)
    if len(history) == 0:
        embed.add_field(name='Woah!', value='No punishments found!', inline=False)
        await message.followup.send(content=None, embed=embed)
        return
    for i in range (0+((cur_page-1)*p), cur_page*p if len(history) > cur_page*p else len(history), 1):
        ht_string = '#' + str(history[i][0]) + ' ' + history[i][1]
        if not IsKick(history[i][1]):
            if history[i][6] is not None:
                ht_string += IsActiveStr(history[i][6])
        h_string = 'Reason: ' + history[i][4] + '\nDate: ' + datetime.strftime(history[i][5], "%d.%m.%Y, %H:%M")
        if not IsKick(history[i][1]):
            if history[i][6] is not None:
                h_string += IsActiveE(history[i][6]) + datetime.strftime(history[i][6], "%d.%m.%Y, %H:%M")
                if history[i][8] is not None:
                    h_string += ' (Unbanned by ' + history[i][8] + ')'
            else:
                if history[i][7] == True:
                    h_string += '\nDuration: Permament'
                if history[i][8] is not None:
                    h_string += ' (Unbanned by ' + history[i][8] + ')'
        embed.add_field(name=ht_string, value=h_string, inline=False)
    embed.set_footer(text=PageFooter('/history ' + users[0][1],cur_page,pages))
    await message.followup.send(content=None, embed=embed)
    return