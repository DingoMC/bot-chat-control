"""dang$$ Bot Utilities

This module contains various util functions
Created by: DingoMC
Cores: akka

"""
from datetime import datetime
import pytz

VERSION = "0.1.0"
print('Loaded Python Module: ' + __name__ + ', using version: ' + VERSION)

def CurrentTime(utctime : str):
    utc_datetime = datetime.strptime(utctime, '%Y-%m-%d %H:%M:%S.%f')
    utc_datetime = utc_datetime.replace(tzinfo=pytz.UTC)
    curr_tz = pytz.timezone('Europe/Berlin')
    curr_datetime = utc_datetime.astimezone(curr_tz)
    return curr_datetime.strftime('%Y-%m-%d %H:%M:%S')