import time
from datetime import datetime

# delete furnace object on logout
def delFurnaceState(obj):
    del obj

# TODO - move to helpers.py
def getTimeNow():
    tn = datetime.now()
    dt_str_format = '%H %M %S'
    return datetime.strftime(tn, dt_str_format)

def getFormattedTimeNow():
    tn = datetime.now()
    dt_str_format = '%H %M %S'
    return formatTime(datetime.strftime(tn, dt_str_format))

def formatTime(timeStr):
    return (timeStr[0:2] + ":" + timeStr[3:5] + ":" + timeStr[6:8])


def parseTime(timeStamp):
    '''
    Is this function even necesary???
    '''
    return timeStamp[10:19]