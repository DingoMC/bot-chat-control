import discord
from dang.embeds import PageFooter
from dang.console import WarningDefer
from dang.models.mcrank import MCRank
VERSION = '0.1.2'
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)
curlist = MCRank.select(['id', 'full_name', 'min', 'max'], order_by={"id": 1})
# Rank list function #
async def main (message, page):
    try:
        await message.defer()
    except:
        WarningDefer('score')
    pages = len(curlist) // 5
    if len(curlist) % 5 != 0: pages += 1
    cur_page = page
    if page > pages: cur_page = pages
    if page <= 0: cur_page = 1
    embed = discord.Embed(title='MC.Dingolan.pl', description='Ranks list', color=0x5555ff)
    for i in range(0+((cur_page-1)*5), cur_page*5 if len(curlist) > cur_page*5 else len(curlist), 1):
        ht_string = '#' + str(curlist[i][0]) + '. ' + str(curlist[i][1])
        h_string = 'Points: ' + str(curlist[i][2]) + ' - ' + str(curlist[i][3])
        embed.add_field(name=ht_string, value=h_string, inline=False)
    embed.set_footer(text=PageFooter('/ranklist',cur_page,pages))
    await message.followup.send(content=None, embed=embed)