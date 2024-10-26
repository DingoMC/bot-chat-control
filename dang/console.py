"""dang$$ Console

This module contains Console handling
Created by: DingoMC
Cores: akka, umbry

"""
from datetime import datetime
from requests import get
from dang.jconfig import GetObject, GetVersion

VERSION = "0.1.23"
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)
def CS(text : str, color : str):
    final_text = "\033[0;3"
    if color == "red" or color == "r":
        final_text += "1m"
    elif color == "green" or color == "g":
        final_text += "2m"
    elif color == "yellow" or color == "y":
        final_text += "3m"
    elif color == "blue" or color == "b":
        final_text += "4m"
    elif color == "purple" or color == "p":
        final_text += "5m"
    elif color == "cyan" or color == "c":
        final_text += "6m"
    elif color == "gray":
        final_text += "7m"
    else:
        final_text += "9m"
    final_text += text
    final_text += "\033[0;39m"
    return final_text
# dang$$ Flags
DAT = CS(' > ', "cyan")     # at
DARR = CS(' -> ', "y")      # arrow
COL = CS(' : ',"cyan")      # subseq
ACK = CS('ACK ',"g")        # ACK
RST = CS('RST ',"r")        # Reset
ERR = CS('ERR ',"r")        # Error
WARN = CS('WARN', "y")      # Warning
SET = CS('SET ',"y")        # Setup
INI = CS('INIT',"r")        # Init
DCALL = CS('CALL',"y")      # Call
TASK = CS('TASK',"p")       # Task
LST = CS('LST ',"cyan")     # Listener
LOAD = CS('LOAD',"r")       # Imports
SQL = CS('SQL', "b")        # SQL
def prtime ():
    ctime = datetime.now()
    cts = ctime.strftime("[%d/%m/%Y][%H:%M:%S]")
    return CS(cts, 'gray')
def prefix ():
    return CS(' dang$$',"r") + DAT
def ACKCommandUsed (cmd : str, executor : str):
    return prtime() + prefix() + ACK + COL + executor + ' used command ' + GetObject('prefix') + cmd
def InitTitleBox ():
    lines : list[str] = [
        '\u250C\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2510',
        '\u2502\t\t\t\t\u2502',
        '\u2502\t' + CS('dang$$', "r") + ' ' + CS('Chat Control', "r") + '\t\u2502',
        '\u2502\t' + CS('Bot Version', "r") + ': ' + CS(GetVersion('Bot Version'), "y") + '\t\u2502',
        '\u2502\t' + CS('Bot Core', "c") + ': ' + CS(GetVersion('Bot Core'), "c") + '\t\t\u2502',
        '\u2502\t' + CS('dang$$ LWJGL', "r") + ': ' + CS(GetVersion('dang$$ LWJGL'), "r") + '\t\u2502',
        '\u2502\t' + CS('Python Version', "y") + ': ' + CS(GetVersion('Python Version'), "y") + '\t\u2502',
        '\u2502\t\t\t\t\u2502',
        '\u2514\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2500\u2518'
    ]
    return '\n'.join(lines)
def ACKCommandsEnabled (am : int):
    return prtime() + prefix() + ACK + COL + 'Successfully enabled ' + str(am)  + ' functions.'
def SetupCustomActivity ():
    return prtime() + prefix() + SET + COL + 'Setting up Custom Activity ...'
def BotOnReady ():
    return prtime() + prefix() + ACK + COL + 'Bot is ready !'
def ViolationMsg (author : str, content : str, listener : str):
    return prtime() + prefix() + LST + COL + DCALL + DAT + CS(listener,"c") + COL + 'AutoMod violation by '  + CS(author,"r") + CS(' -> ',"y") + CS(content,"r")
def GetExternalIP ():
    return get('https://api.ipify.org').text
def MissingPermission (author : str, content : str):
    return prtime() + prefix() + ERR + COL + CS(author, "r") + DARR + 'Permission violation' + DARR + CS(content, "r")
def WarningDMNotAllowed (dcid : str):
    return prtime() + prefix() + WARN + COL + 'Could not send a DM to ' + CS(dcid, "r")
def ErrorServerInfo ():
    return prtime() + prefix() + TASK + COL + ERR + DAT + CS('dang.tasks.external',"p") + COL + 'Error requesting data for ' + GetObject('dns') + ' - no further information.'
def ErrorReadingNBT():
    return prtime() + prefix() + ERR + COL + CS('dang.mccon',"b") + DARR + 'Error while reading NBT file!'
def ErrorAPI():
    return prtime() + prefix() + ERR + COL + CS('dang.mcapi', "b") + DARR + 'Error fetching data from Mojang API!'
def WarningDefer(command : str):
    return prtime() + prefix() + WARN + COL + 'Ignoring error while deferring ' + CS(command, "y") + ' command'
def DingormExec (sql : str):
    return prtime() + prefix() + SQL + DAT + CS('dingorm', "p") + COL + sql
def DingormErrorExecuteSQL(sql : str, err : str = None):
    if err is None:
        return prtime() + prefix() + ERR + DAT + CS('dingorm', "r") + COL + 'Unkown Error while executing SQL statement: ' + CS(sql, "r") + '.'
    return prtime() + prefix() + ERR + DAT + CS('dingorm', "r") + COL + 'SQL Error: ' + CS(err, "r")
def MCConErrNoPath(path : str):
    return prtime() + prefix() + ERR + DAT + CS('mccon', "r") + COL + 'Invalid path for NBT file: ' + CS(path, "r") + '.'
def MCConNoScore(name : str, objective : str):
    return prtime() + prefix() + WARN + DAT + CS('mccon', "y") + COL + 'No score found for player: ' + CS(name, "y") + ' in objective: ' + CS(objective, "y") + '.'
def MCConFoundScore(name : str, objective : str, score : int):
    return prtime() + prefix() + ACK + DAT + CS('mccon', "p") + COL + 'Name: ' + CS(name, "cyan") + ', Objective: ' + CS(objective, "cyan") + ', Score: ' + CS(str(score), "cyan") + '.'
