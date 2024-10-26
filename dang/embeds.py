"""dang$$ Embeds

This module contains Embed Content Handling
Created by: DingoMC
Cores: akka, umbry

"""
import discord
VERSION = "0.4.0"
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)
def PageFooter (cmd : str, page : int, all_pages : int):
    r"""[ dang$$ akka-2.9.4 ]

    Set a Page footer for Embed

    Parameters
    -----------
    cmd: str
        Command that uses paging
    page: int
        Current page number
    all_pages: int
        Number of all pages
    
    Returns
    --------
    String: Page Embed Footer
    """
    e_footer = ''
    if page > 1:
        e_footer += '<< Previous - ' + cmd + ' ' + str(page-1) + ' | '
    e_footer += 'Page (' + str(page) + ' of ' + str(all_pages) + ')'
    if page < all_pages:
        e_footer += ' | ' + cmd + ' ' + str(page+1) + ' - Next >>'
    return e_footer
def ErrorEmbedNameNotFound (name : str):
    e_title = 'Error! Couldn\'t find member named ' + name
    embed = discord.Embed(title=e_title, description='Remember that name is case sensitive.', color=0xff5555)
    return embed
def ListenerEmbedMessagedeleted (listener : str, author : str, content : str, footer : str):
    e_title = 'dang$$#' + listener
    embed = discord.Embed(title=e_title, description="Message Deleted", color=0xff0000)
    embed.add_field(name="Message author", value=author, inline=True)
    embed.add_field(name="Message content", value=content, inline=True)
    embed.set_footer(text=footer)
    return embed
def MemberWarned (user : str, reason : str, warned_on : str, expires : str, warn_id : int, moderator : str):
    e_title = 'Discord Warning'
    e_desc = None
    footer = 'Warn ID: ' + str(warn_id) + '\nModerator: ' + moderator
    embed = discord.Embed(title=e_title, description=e_desc, color=0xdd9800)
    embed.add_field(name="User", value=user, inline=False)
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.add_field(name="Warned On", value=warned_on, inline=False)
    embed.add_field(name="Active Until", value=expires, inline=False)
    embed.set_footer(text=footer)
    return embed
def MemberMuted (user : str, reason : str, muted_on : str, expires : str, mute_id : int, moderator : str):
    e_title = 'Discord Mute'
    e_desc = None
    footer = 'Mute ID: ' + str(mute_id) + '\nModerator: ' + moderator
    embed = discord.Embed(title=e_title, description=e_desc, color=0x787878)
    embed.add_field(name="User", value=user, inline=False)
    embed.add_field(name="Reason", value=reason, inline=False)
    embed.add_field(name="Muted On", value=muted_on, inline=False)
    embed.add_field(name="Muted Until", value=expires, inline=False)
    embed.set_footer(text=footer)
    return embed
def PlayerJoined (player: str):
    e_title = player + ' joined'
    e_desc = None
    embed = discord.Embed(title=e_title, description=e_desc, color=0x55ff55)
    return embed
def PlayerLeft (player: str):
    e_title = player + ' left'
    e_desc = None
    embed = discord.Embed(title=e_title, description=e_desc, color=0xff5555)
    return embed
def PlayerDied (message: str):
    e_title = message
    e_desc = None
    embed = discord.Embed(title=e_title, description=e_desc, color=0x121212)
    return embed