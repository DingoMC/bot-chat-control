import discord
from dang.console import WarningDefer
VERSION = '0.1.2'
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)
# uwu function #
async def main (message : discord.Message, text):
    try:
        await message.defer()
    except:
        WarningDefer('uwu')
    chg = list(text)
    rz = False
    for m in range(0, len(chg), 1):
        if chg[m] == 'R':
            if m < len(chg) - 1:
                if chg[m+1] == 'z': rz = True
            if not rz: chg[m] = '\u0141'
            rz = False
        if chg[m] == 'r':
            if m < len(chg) - 1:
                if chg[m+1] == 'z': rz = True
            if not rz: chg[m] = '\u0142'
            rz = False
        if chg[m] == 'l': chg[m] = '\u0142'
        if chg[m] == 'L': chg[m] = '\u0141'
    final = '**' + str(message.author) + ' said:** ' + ''.join(chg) + ' uwu'
    await message.followup.send(content=final.format(message))