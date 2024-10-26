import discord
from dang.jconfig import GetCommandsList, GetObject, GetCommandDescription, GetCommandArgs, IsArgumentRequired, GetArgumentDescription
from dang.embeds import PageFooter
from dang.console import WarningDefer
VERSION = '0.1.2'
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)
# Bot Command Help Function #
async def main (message, help_page):
    try:
        await message.defer()
    except:
        WarningDefer('help')
    helplist = GetCommandsList()
    pages = len(helplist) // 5
    if len(helplist) % 5 != 0: pages += 1
    if help_page > pages: help_page = pages
    if help_page <= 0: help_page = 1
    embed = discord.Embed(title='dang$$ Bot', description='Command Help', color=0x5555ff)
    for i in range(0+((help_page-1)*5), help_page*5 if len(helplist) > help_page*5 else len(helplist), 1):
        ht_string = GetObject('prefix') + helplist[i]
        h_string = ''
        h_string += str(GetCommandDescription(helplist[i]))
        cmd_arg_names = GetCommandArgs(helplist[i])
        if cmd_arg_names is not None:
            for a in cmd_arg_names:
                h_string += ('\n' + a)
                if IsArgumentRequired(helplist[i], a):
                    h_string += ' (Required): '
                    ht_string += ' <' + a + '>'
                else:
                    h_string += ' (Optional): '
                    ht_string += ' [' + a + ']'
                h_string += GetArgumentDescription(helplist[i], a)
        embed.add_field(name=ht_string, value=h_string, inline=False)
    embed.set_footer(text=PageFooter('/help',help_page,pages))
    await message.followup.send(content=None, embed=embed)