import discord
from random import randint
from dang.models.mcfacts import MCFacts
from dang.console import WarningDefer
VERSION = '0.2.1'
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)
facts = MCFacts.select()
# Get Fact
async def main (message):
    try:
        await message.defer()
    except:
        WarningDefer('fact')
    idx = randint(0,len(facts)-1)
    picked = facts[idx][1]
    e_footer = 'Fact No. ' + str(facts[idx][0])
    embed = discord.Embed(title="Fact", description="Totally a fact", color=0x55ffff)
    embed.add_field(name="Fact", value=str(picked), inline=False)
    embed.set_footer(text=e_footer)
    await message.followup.send(content=None, embed=embed)