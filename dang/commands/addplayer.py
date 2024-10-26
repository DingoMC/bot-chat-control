from sys import prefix
import discord
from random import seed
from random import randint
from dang.mcapi import GetUUIDByName, dashedUUID
from dang.console import WarningDefer
from dang.models.mcuser import MCUser

VERSION = '0.1.1'
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)

def CreateUUIDPart ():
    num = randint(0, 9999)
    if num < 10: return '000' + str(num)
    if num < 100: return '00' + str(num)
    if num < 1000: return '0' + str(num)
    return str(num)

def CreatePassword ():
    chars = []
    for i in range (48, 58): chars.append(chr(i))
    for i in range (65, 91): chars.append(chr(i))
    for i in range (97, 123): chars.append(chr(i))
    pass_len = 6
    char_len = len(chars)
    password = ''
    for i in range (0, pass_len):
        password += chars[randint(0, char_len - 1)]
    return password

def AppendTeamSettings (descriptor : str):
    file_path = '../../../../../../root/minecraft_m/minigames/datapacks/dang/data/y_subfunc/functions/sc-tm-sync.mcfunction'
    lines = ['# Add new team - ' + descriptor + ' (dang$$) #',
    'spawnpoint @a[team=' + descriptor + '] -40 11 92',
    'execute if entity @p[tag=' + descriptor + ',x=-72,y=0,z=60,dx=64,dy=255,dz=64,team=!' + descriptor + '] run team join ' + descriptor + ' @p[tag=' + descriptor + ']']
    with open(file_path, 'a') as f:
        f.write('\n'.join(lines))

def AppendDescriptor (descriptor : str, mcuuid : str):
    file_path = '../../../../../../root/minecraft_m/minigames/datapacks/dang/data/y_subfunc/functions/set-descriptors.mcfunction'
    lines = ['# Add new descriptor - ' + descriptor + ' (dang$$) #',
    'tag ' + mcuuid + ' add ' + descriptor,
    'tag ' + mcuuid + ' add ' + descriptor + 'bb']
    with open(file_path, 'a') as f:
        f.write('\n'.join(lines))

sc_pl_add_p_r = lambda points, descriptor: 'scoreboard players add @p[tag=' + str(descriptor) + '] points-rank ' + str(points)
sc_pl_rem_p_r = lambda points, descriptor: 'scoreboard players remove @p[tag=' + str(descriptor) + '] points-rank ' + str(points)

def exif_match (descriptor : str, mn : int, mx : int):
    r = ''
    if mn <= -30: r = '..'
    else: r = str(mn) + '..'
    if mx < 20000: r += str(mx)
    return 'execute if score @p[tag=' + descriptor + '] Points matches ' + r + ' run '

def tm_prefix (descriptor : str, team : str, rname : str):
    prf = 'team modify ' + descriptor + ' prefix {"text":"'
    prf += rname
    prf += ' \\u00A7' + team + '"}'
    return prf

def bb_name (descriptor : str, rname : str, bbpcolor : str, rmin : int):
    name = 'bossbar set minecraft:' + descriptor + ' name '
    name += '[{"text":"\\u00A76Rank: ' + rname + ' \\u00A7aRankup: "},'
    name += '{"color":"' + bbpcolor + '","score":{"name":"@p[tag=' + descriptor + ']","objective":"Points"}},'
    name += '{"text":"\\u00A7f/'
    if rmin >= 20000: name += '\\u00A74???'
    else: name += '\\u00A7a' + str(rmin)
    name += '"}]'
    return name

def GenereateRankup (descriptor : str, team : str):
    rnames = ["\\u00A7d[NOOB]", "\\u00A7f[NONE]", "\\u00A7b[MVP]", "\\u00A7b[MVP\\u00A7c+\\u00A7b]", "\\u00A7b[MVP\\u00A74++\\u00A7b]",
    "\\u00A75<\\u00A7aVIP\\u00A75>", "\\u00A75<\\u00A7aVIP\\u00A75>\\u00A7b[MVP]", "\\u00A75<\\u00A7aVIP\\u00A75>\\u00A7b[MVP\\u00A7c+\\u00A7b]", "\\u00A75<\\u00A7aVIP\\u00A75>\\u00A7b[MVP\\u00A74++\\u00A7b]",
    "\\u00A75<x\\u00A7aVIP\\u00A75>", "\\u00A75<x\\u00A7aVIP\\u00A75>\\u00A7b[MVP]", "\\u00A75<x\\u00A7aVIP\\u00A75>\\u00A7b[MVP\\u00A7c+\\u00A7b]", "\\u00A75<x\\u00A7aVIP\\u00A75>\\u00A7b[MVP\\u00A74++\\u00A7b]",
    "\\u00A75<\\u00A7bPRO\\u00A75>", "\\u00A7a<\\u00A7bMASTER\\u00A7a>", "\\u00A76<\\u00A7bLEGEND\\u00A76>",
    "\\u00A7c<\\u00A77IRON 4\\u00A7c>", "\\u00A75<\\u00A77IRON 3\\u00A75>", "\\u00A7a<\\u00A77IRON 2\\u00A7a>", "\\u00A76<\\u00A77IRON 1\\u00A76>",
    "\\u00A7c<\\u00A76GOLD 4\\u00A7c>", "\\u00A75<\\u00A76GOLD 3\\u00A75>", "\\u00A7a<\\u00A76GOLD 2\\u00A7a>", "\\u00A76<\\u00A76GOLD 1\\u00A76>",
    "\\u00A7c<\\u00A7aEMERALD 4\\u00A7c>", "\\u00A75<\\u00A7aEMERALD 3\\u00A75>", "\\u00A7a<\\u00A7aEMERALD 2\\u00A7a>", "\\u00A76<\\u00A7aEMERALD 1\\u00A76>",
    "\\u00A7c<\\u00A7bDIAMOND 4\\u00A7c>", "\\u00A75<\\u00A7bDIAMOND 3\\u00A75>", "\\u00A7a<\\u00A7bDIAMOND 2\\u00A7a>", "\\u00A76<\\u00A7bDIAMOND 1\\u00A76>",
    "\\u00A79[\\u00A74MHF\\u00A79]"]
    bbcolors = ["pink", "white", "blue", "blue", "blue", "green", "green", "green", "green", "purple", "purple", "purple", "purple",
    "purple", "green", "yellow", "white", "white", "white", "white", "yellow", "yellow", "yellow", "yellow", "green", "green", "green", "green",
    "blue", "blue", "blue", "blue", "purple"]
    bbpcolors = ["light_purple", "white", "aqua", "aqua", "aqua", "green", "green", "green", "green",
    "dark_purple", "dark_purple", "dark_purple", "dark_purple", "dark_purple", "green", "gold", "gray", "gray", "gray", "gray",
    "gold", "gold", "gold", "gold", "green", "green", "green", "green", "aqua", "aqua", "aqua", "aqua", "blue"]
    rmin = [-30, 0, 51, 100, 200, 300, 400, 450, 550, 650, 750, 800, 900, 1000, 1100, 1200, 1500, 1700, 2000, 2400, 2900, 3200, 3600, 4100,
    4700, 5100, 5600, 6200, 6900, 7400, 8000, 8700, 10000]
    rmax = []
    for i in range (0, 32, 1): rmax.append(int(rmin[i+1] - 1))
    rmax.append(20000)
    file_path = '../../../../../../root/minecraft_m/minigames/datapacks/dang/data/y_subfunc/functions/rankup-bb-' + descriptor + '.mcfunction'
    lines = []
    lines.append('# Bossbar Sync (Desc: ' + descriptor + ', Team: ' + team + ') #')
    lines.append('execute store result bossbar minecraft:' + descriptor + ' value run ' + sc_pl_add_p_r(0, descriptor))
    lines.append('scoreboard players operation @p[tag=' + descriptor + '] points-rank = @p[tag=' + descriptor + '] Points')
    lines.append('bossbar set minecraft:' + descriptor + ' players @a[tag=' + descriptor + 'bb]')
    lines.append('# Setting rank prefixes #')
    for i in range (0, 33): lines.append(exif_match(descriptor, rmin[i], rmax[i]) + tm_prefix(descriptor, team, rnames[i]))
    lines.append('# Setting points-rank values #')
    for i in range (0, 33):
        if i == 0: lines.append(exif_match(descriptor, rmin[i], rmax[i]) + sc_pl_add_p_r(30, descriptor))
        elif i == 1: lines.append(exif_match(descriptor, rmin[i], rmax[i]) + sc_pl_add_p_r(0, descriptor))
        else: lines.append(exif_match(descriptor, rmin[i], rmax[i]) + sc_pl_rem_p_r(rmin[i], descriptor))
    lines.append('# Setting bossbar colors #')
    for i in range (0, 33): lines.append(exif_match(descriptor, rmin[i], rmax[i]) + 'bossbar set minecraft:' + descriptor + ' color ' + bbcolors[i])
    lines.append('# Setting bossbar maxes #')
    for i in range (0, 33):
        if i == 0: lines.append(exif_match(descriptor, rmin[i], rmax[i]) + 'bossbar set mineacrft:' + descriptor + ' max 29')
        else: lines.append(exif_match(descriptor, rmin[i], rmax[i]) + 'bossbar set mineacrft:' + descriptor + ' max ' + str(rmax[i] - rmin[i] + 1))
    lines.append('# Setting bossbar names #')
    for i in range (0, 33):
        if i == 32: lines.append(exif_match(descriptor, rmin[i], rmax[i]) + bb_name(descriptor, rnames[i], bbpcolors[i], 20000))
        else: lines.append(exif_match(descriptor, rmin[i], rmax[i]) + bb_name(descriptor, rnames[i], bbpcolors[i], rmin[i+1]))
    with open(file_path, 'w') as f:
        f.write('\n'.join(lines))
    main_path = '../../../../../../root/minecraft_m/minigames/datapacks/dang/data/y_subfunc/functions/rankup-main.mcfunction'
    with open(main_path, 'a') as f:
        f.write('function y_subfunc:rankup-bb-' + descriptor)

def PrefixToColor (prf : str):
    if prf == '0': return 'black'
    if prf == '1': return 'dark_blue'
    if prf == '2': return 'dark_green'
    if prf == '3': return 'dark_aqua'
    if prf == '4': return 'dark_red'
    if prf == '5': return 'dark_purple'
    if prf == '6': return 'gold'
    if prf == '7': return 'gray'
    if prf == '8': return 'black'
    if prf == '9': return 'dark_blue'
    if prf == 'a': return 'green'
    if prf == 'b': return 'aqua'
    if prf == 'c': return 'red'
    if prf == 'd': return 'light_purple'
    if prf == 'e': return 'yellow'
    return 'white'

def GenerateSetupFunction (playername : str, prf : str, descriptor : str):
    file_path = '../../../../../../root/minecraft_m/minigames/datapacks/dang/data/y_subfunc/functions/set-new-player.mcfunction'
    setup_objectives = ['SCU', 'SCF', 'Kx1000', 'timer', 'Hours', 'points-rank',
    'Additional', 'HourlyCrate', 'Kills', 'Deaths', 'Points', 'NLPoints', 'SWPoints',
    'SPPoints', 'BOPoints', 'HSPoints', 'SCB_Points', 'SCB_Timers', 'EWPoints',
    'ETVScore', 'ETVEscapes', 'EtVTierB', 'EtVTierL', 'EtVTierC', 'EtVTierH', 'PA_Black',
    'PA_Blue', 'PA_Slime', 'PA_Cyan', 'PA_Brown', 'PA_Amethyst', 'PA_Orange', 'PA_Gray',
    'PA_DGray', 'PA_Magenta', 'PA_Green', 'PA_Aqua', 'PA_Red', 'PA_Pink', 'PA_Yellow', 'PA_White']
    lines = []
    lines.append('# Team setup #')
    lines.append('team add ' + descriptor)
    lines.append('team modify ' + descriptor + ' collisionRule never')
    lines.append('team modify ' + descriptor + ' color ' + PrefixToColor(prf))
    lines.append('# Bossbar setup #')
    lines.append('bossbar add ' + descriptor + ' {"text":""}')
    lines.append('bossbar set minecraft:' + descriptor + ' style notched_10')
    lines.append('# Create new scores #')
    for o in setup_objectives: lines.append('scoreboard players set ' + playername + ' ' + o + ' 0')
    lines.append('# Autogenerated by dang$$ #')
    with open(file_path, 'w') as f:
        f.write('\n'.join(lines))

async def main (message : discord.Message, playername : str, prf : str, dc_user : discord.User, descriptor : str):
    try:
        await message.defer()
    except:
        WarningDefer('addplayer')
    seed(randint(0,255))
    # Create dang$$ uuid
    data = MCUser.select(['uuid'])
    dang_uuid = CreateUUIDPart() + '-' + CreateUUIDPart()
    while dang_uuid in data[0]:
        dang_uuid = CreateUUIDPart() + '-' + CreateUUIDPart()
    mcuuid = GetUUIDByName(playername)
    # Add to database
    MCUser.insert(dang_uuid, mcuuid, str(dc_user.id), prf)
    # Add new lines in sc-tm-sync.mcfunction
    AppendTeamSettings(descriptor)
    # Add new uuid descriptors / tags in set-descriptors.mcfunction
    AppendDescriptor(descriptor, dashedUUID(mcuuid))
    # Create rankup-bb-<dsc>.mcfunction and hook it to rankup-main.mcfunction
    GenereateRankup(descriptor, prf)
    # Create Setup function to be executed once set-new-player.mcfunction
    GenerateSetupFunction(playername, prf, descriptor)
    msg = '{0.author.mention} Added new player!'
    msg += '\nRun **/reload** -> To load new generated functions'
    msg += '\nRun **/function y_subfunc:set-new-player** -> To setup new player'
    await message.followup.send(content=msg.format(message), ephemeral=True)
