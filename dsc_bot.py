# Code made originally by Elektroteleinformatyko master v.4
# Import neccessary libraries
import os
import sys
try:
    # import necessary libs
    import discord
    from discord.ext import commands
    import asyncio
    from dotenv import load_dotenv
    from random import seed
    from random import randint
    # import dang$$ basic modules
    import dang.commands
    import dang.console as dcon
    import dang.jconfig as djc
    # import automods
    from dang.automod import *
    # import commands
    from dang.commands import *
except ImportError or ModuleNotFoundError:
    print("dang$$ > ERR  : Python -> At least 1 required module could not be found! Exiting...")
    sys.exit(1)
# Discord Token and Discord Server Name is located in .env file
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
GUILD_ID = 571982328759582741
# Login as a discord user
intents = discord.Intents.all()
client = commands.Bot(intents=intents)
### MAIN BOT PART ###
# Slash commands
@client.slash_command(name='help', description=djc.GetCommandDescription('help'))
async def help (message,
    page : discord.Option(int, description=djc.GetArgumentDescription('help', 'Page'), required=False, default=1)):
    await dang.commands.help.main(message, page)
    print(dcon.ACKCommandUsed('help', str(message.author)))

@client.slash_command(name='fact', description=djc.GetCommandDescription('fact'))
async def fact (message):
    await dang.commands.fact.main(message)
    print(dcon.ACKCommandUsed('fact', str(message.author)))

@client.slash_command(name='points', description=djc.GetCommandDescription('points'))
async def points (message,
    name : discord.Option(str, description=djc.GetArgumentDescription('points', 'Name'), required=False, default='Self')):
    await dang.commands.points.main(message, name)
    print(dcon.ACKCommandUsed('points', str(message.author)))

@client.slash_command(name='score', description=djc.GetCommandDescription('score'))
async def score (message,
    game : discord.Option(str, description=djc.GetArgumentDescription('score', 'Game'), required=True),
    name : discord.Option(str, description=djc.GetArgumentDescription('score', 'Name'), required=False, default='Self')):
    await dang.commands.score.main(message, game, name)
    print(dcon.ACKCommandUsed('score', str(message.author)))

@client.slash_command(name='kills', description=djc.GetCommandDescription('kills'))
async def kills (message,
    name : discord.Option(str, description=djc.GetArgumentDescription('kills', 'Name'), required=False, default='Self')):
    await dang.commands.kills.main(message, name)
    print(dcon.ACKCommandUsed('kills', str(message.author)))

@client.slash_command(name='deaths', description=djc.GetCommandDescription('deaths'))
async def deaths (message,
    name : discord.Option(str, description=djc.GetArgumentDescription('deaths', 'Name'), required=False, default='Self')):
    await dang.commands.deaths.main(message, name)
    print(dcon.ACKCommandUsed('deaths', str(message.author)))

@client.slash_command(name='kdr', description=djc.GetCommandDescription('kdr'))
async def kdr (message,
    name : discord.Option(str, description=djc.GetArgumentDescription('kdr', 'Name'), required=False, default='Self')):
    await dang.commands.kdr.main(message, name)
    print(dcon.ACKCommandUsed('kdr', str(message.author)))

@client.slash_command(name='playtime', description=djc.GetCommandDescription('playtime'))
async def playtime (message,
    name : discord.Option(str, description=djc.GetArgumentDescription('playtime', 'Name'), required=False, default='Self')):
    await dang.commands.playtime.main(message, name)
    print(dcon.ACKCommandUsed('playtime', str(message.author)))

@client.slash_command(name='where', description=djc.GetCommandDescription('where'))
async def where (message,
    name : discord.Option(str, description=djc.GetArgumentDescription('where', 'Name'), required=False, default='Self')):
    await dang.commands.where.main(message, name)
    print(dcon.ACKCommandUsed('where', str(message.author)))

@client.slash_command(name='leaderboard', description=djc.GetCommandDescription('leaderboard'))
async def leaderboard (message,
    game : discord.Option(str, description=djc.GetArgumentDescription('leaderboard', 'Game'), required=False, default='General')):
    await dang.commands.leaderboard.main(message, game)
    print(dcon.ACKCommandUsed('leaderboard', str(message.author)))

@client.slash_command(name='version', description=djc.GetCommandDescription('version'))
async def version (message):
    await dang.commands.version.main(message)
    print(dcon.ACKCommandUsed('version', str(message.author)))

@client.slash_command(name='ranklist', description=djc.GetCommandDescription('ranklist'))
async def ranklist (message,
    page : discord.Option(int, description=djc.GetArgumentDescription('ranklist', 'Page'), required=False, default=1)):
    await dang.commands.ranklist.main(message, page)
    print(dcon.ACKCommandUsed('ranklist', str(message.author)))

@client.slash_command(name='ip', description=djc.GetCommandDescription('ip'))
async def ip (message):
    await dang.commands.ip.main(message)
    print(dcon.ACKCommandUsed('ip', str(message.author)))

@client.slash_command(name='uwu', description=djc.GetCommandDescription('uwu'))
async def uwu (message,
    text : discord.Option(str, description=djc.GetArgumentDescription('uwu', 'Message'), required=True)):
    await dang.commands.uwu.main(message, text)
    print(dcon.ACKCommandUsed('uwu', str(message.author)))

@client.slash_command(name='history', description=djc.GetCommandDescription('history'))
async def history (message,
    name : discord.Option(str, description=djc.GetArgumentDescription('history', 'Name'), required=False, default='Self'),
    page : discord.Option(int, description=djc.GetArgumentDescription('history', 'Page'), required=False, default=1)):
    await dang.commands.history.main(message, name, page)
    print(dcon.ACKCommandUsed('history', str(message.author)))

@client.slash_command(name='warn', description=djc.GetCommandDescription('warn'), guild_ids=[GUILD_ID])
async def warn (message,
    user : discord.Option(discord.User, description=djc.GetArgumentDescription('warn', 'User'), required=True),
    duration : discord.Option(str, description=djc.GetArgumentDescription('warn', 'Duration'), required=True),
    reason : discord.Option(str, description=djc.GetArgumentDescription('warn', 'Reason'), required=False, default='<No reason provided>')):
    staff = djc.GetList('mod')
    if str(message.author.id) in staff:
        for guild in client.guilds:
            g_id = guild.id
        c_guild = client.get_guild(g_id)
        await dang.commands.warn.main(c_guild, client, message, user, duration, reason)
        print(dcon.ACKCommandUsed('warn', str(message.author)))
        return
    print(dcon.MissingPermission(str(message.author), str(message.content)))
    msg = '{0.author.mention} You do not have permission to use this command!'
    await message.respond(content=msg.format(message), ephemeral=True)
    return

@client.slash_command(name='mute', description=djc.GetCommandDescription('mute'), guild_ids=[GUILD_ID])
async def mute (message,
    user : discord.Option(discord.User, description=djc.GetArgumentDescription('mute', 'User'), required=True),
    duration : discord.Option(str, description=djc.GetArgumentDescription('mute', 'Duration'), required=True),
    reason : discord.Option(str, description=djc.GetArgumentDescription('mute', 'Reason'), required=False, default='<No reason provided>')):
    staff = djc.GetList('mod')
    if str(message.author.id) in staff:
        for guild in client.guilds:
            g_id = guild.id
        c_guild = client.get_guild(g_id)
        await dang.commands.mute.main(c_guild, client, message, user, duration, reason)
        print(dcon.ACKCommandUsed('mute', str(message.author)))
        return
    print(dcon.MissingPermission(str(message.author), str(message.content)))
    msg = '{0.author.mention} You do not have permission to use this command!'
    await message.respond(content=msg.format(message), ephemeral=True)
    return

@client.slash_command(name='mcwarn', description=djc.GetCommandDescription('mcwarn'), guild_ids=[GUILD_ID])
async def mcwarn (message,
    player : discord.Option(str, description=djc.GetArgumentDescription('mcwarn', 'Player'), required=True),
    duration : discord.Option(str, description=djc.GetArgumentDescription('mcwarn', 'Duration'), required=True),
    reason : discord.Option(str, description=djc.GetArgumentDescription('mcwarn', 'Reason'), required=False, default='-')):
    staff = djc.GetList('mod')
    if str(message.author.id) in staff:
        for guild in client.guilds:
            g_id = guild.id
        c_guild = client.get_guild(g_id)
        await dang.commands.mcwarn.main(c_guild, message, player, duration, reason)
        print(dcon.ACKCommandUsed('mcwarn', str(message.author)))
        return
    print(dcon.MissingPermission(str(message.author), str(message.content)))
    msg = '{0.author.mention} You do not have permission to use this command!'
    await message.respond(content=msg.format(message), ephemeral=True)
    return

@client.slash_command(name='sudo', description=djc.GetCommandDescription('sudo'), guild_ids=[GUILD_ID])
async def sudo (message,
    text : discord.Option(str, description=djc.GetArgumentDescription('sudo', 'Text'), required=True)):
    staff = djc.GetList('admin')
    if str(message.author.id) in staff:
        channel = client.get_channel(571982328759582743)
        await channel.send(content=text.format(message))
        msg = '{0.author.mention} Message sent successfully!'
        await message.respond(content=msg.format(message), ephemeral=True)
        print(dcon.ACKCommandUsed('sudo', str(message.author)))
        return
    print(dcon.MissingPermission(str(message.author), str(message.content)))
    msg = '{0.author.mention} You do not have permission to use this command!'
    await message.respond(content=msg.format(message), ephemeral=True)
    return

@client.slash_command(name='restart', description=djc.GetCommandDescription('restart'), guild_ids=[GUILD_ID])
async def restart (message):
    staff = djc.GetList('admin')
    if str(message.author.id) in staff:
        print(dcon.ACKCommandUsed('restart', str(message.author)))
        msg = '{0.author.mention} Restarting...'
        await message.respond(content=msg.format(message), ephemeral=True)
        os.execv(sys.executable, ['python'] + sys.argv)
    print(dcon.MissingPermission(str(message.author), str(message.content)))
    msg = '{0.author.mention} You do not have permission to use this command!'
    await message.respond(content=msg.format(message), ephemeral=True)
    return

@client.slash_command(name='updatename', description=djc.GetCommandDescription('updatename'), guild_ids=[GUILD_ID])
async def updatename (message,
    old_name : discord.Option(str, description=djc.GetArgumentDescription('updatename', 'Old'), required=True),
    new_name : discord.Option(str, description=djc.GetArgumentDescription('updatename', 'New'), required=True)):
    staff = djc.GetList('admin')
    if str(message.author.id) in staff:
        await dang.commands.updatename.main(message, old_name, new_name)
        print(dcon.ACKCommandUsed('updatename', str(message.author)))
        return
    print(dcon.MissingPermission(str(message.author), str(message.content)))
    msg = '{0.author.mention} You do not have permission to use this command!'
    await message.respond(content=msg.format(message), ephemeral=True)
    return

@client.slash_command(name='addplayer', description=djc.GetCommandDescription('addplayer'), guild_ids=[GUILD_ID])
async def addplayer (message,
    playername : discord.Option(str, description=djc.GetArgumentDescription('addplayer', 'Name'), required=True),
    prefix : discord.Option(str, description=djc.GetArgumentDescription('addplayer', 'Prefix'), required=True),
    dc_user : discord.Option(discord.User, description=djc.GetArgumentDescription('addplayer', 'User'), required=True),
    descriptor : discord.Option(str, description=djc.GetArgumentDescription('addplayer', 'Descriptor'), required=True)):
    staff = djc.GetList('admin')
    if str(message.author.id) in staff:
        await dang.commands.addplayer.main(message, playername, prefix, dc_user, descriptor)
        print(dcon.ACKCommandUsed('addplayer', str(message.author)))
        return
    print(dcon.MissingPermission(str(message.author), str(message.content)))
    msg = '{0.author.mention} You do not have permission to use this command!'
    await message.respond(content=msg.format(message), ephemeral=True)
    return

# Start listening to the chat ...
@client.event
async def on_message (message : discord.Message):
    for guild in client.guilds:
        g_id = guild.id
    c_guild = client.get_guild(g_id)
    # Prevent bot from responding to his own messages
    if message.author == client.user or str(message.author.id) == '1210935966743662622': return
    # Chat listeners part
    ignore = False
    # Ignore Whitelisted Channels
    for i in djc.GetList('whitelisted_channels'):
        if message.channel.id == int(i):
            ignore = True
            break
    # Ignore Users with bypass filter
    for i in djc.GetList('admin'):
        if message.author.id == int(i):
            ignore = True
            break
    # Otherwise run filters
    if not ignore:
        await dang.automod.swears.main(c_guild, client, message)
        await dang.automod.ads.main(c_guild, client, message)
        await dang.automod.flood.main(c_guild, client, message)
    if str(message.channel.id) == djc.GetChannel("ingame_chat"):
        await dang.automod.chat.sendIngameMessage(c_guild, client, message)

# Run when bot is initializing ...
@client.event
async def on_ready():
    # Stop tasks if there were any
    init_tasks = asyncio.all_tasks()
    for task in init_tasks:
        name = task.get_name()
        if not 'pycord' in name and name != 'Task-1':
            print(dcon.AutoUpdaterCancelled())
            task.cancel()
    seed(randint(0,255))
    for guild in client.guilds:
        if guild.name == GUILD:
            break
    print(dcon.InitTitleBox())
    print(dcon.prtime() + dcon.prefix() + dcon.INI + dcon.COL + f'Server found: {guild.name} (id: {guild.id})')
    reg_functions = djc.GetCommandsList()
    print(dcon.ACKCommandsEnabled(len(reg_functions)))
    print(dcon.SetupCustomActivity())
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="chat all the time"))
    print(dcon.BotOnReady())
client.run(TOKEN)