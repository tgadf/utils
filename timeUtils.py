
# coding: utf-8

from datetime import datetime as dt
import datetime
from datetime import timedelta, date
from calendar import monthrange
from pandas import Timestamp
import dateutil.parser
    
    
################################################################################
# Return datetime object
################################################################################
def getDateTime(dtval, dtformat='%Y-%m-%d'):
    if isPandas(dtval):
        dtval = convertPandasTimestamp(dtval)
        
    try:
        dtobj = dt.strptime(dtval, dtformat)
        return dtobj
    except:
        dtobj = None

    if dtobj is None:
        dtformats = ['%b %d, %Y', '%b %d %Y', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S']
        for dtformat in dtformats:
            try:
                dtobj = dt.strptime(dtval, dtformat)
                return dtobj
            except:
                dtobj = None
                
    if dtobj is None:
        try:
            dtobj = dateutil.parser.parse(dtval)
            return dtobj
        except:
            dtobj
                
    return dtobj


################################################################################
# Return string of datetime object
################################################################################
def printDateTime(dtval,dtformat="%Y-%m-%d"):
    if isinstance(dtval,str):
        dtobj = getDateTime(dtval)
    elif isPandas(dtval):
        dtobj = convertPandasTimestamp(dtval)
    else:
        dtobj = dtval

    if isDateTime(dtobj):
        dtstr = dt.strftime(dtobj, dtformat)
    elif isDate(dtobj):
        dtstr = dt.strftime(dtobj, dtformat)
    elif isPandas(dtobj):
        dtobj = getDateTime(dtobj)
        dtstr = dt.strftime(dtobj, dtformat)
    else:
        print("Can not print object {0}".format(dtval))
        dtstr = dtval
              
    return dtstr



def createDateFromDMY(day, month, year):
    try:
        dtobj = date(year, month, day)
    except:
        print("Could not create date from Day={0}, Month={1}, Year={2}".format(day, month, year))
              
    return dtobj


def getFirstLastDay(month, year):
    lastday   = monthrange(year, month)[1]
    lastdate  = printDateTime(createDateFromDMY(lastday, month, year))
    firstdate = printDateTime(createDateFromDMY(1, month, year))
    return firstdate, lastdate


def addDays(dtval, days):
    retobj = True
    if isinstance(dtval,str):
        dtobj = getDateTime(dtval)
        retobj = False
    else:
        dtobj = dtval

    dtobj = dtobj + timedelta(days=days)
    if retobj:
        return dtobj
    else:
        return printDateTime(dtobj)


def addMonths(dtval, months):
    from dateutil.relativedelta import relativedelta
    retobj = True
    if isinstance(dtval,str):
        dtobj = getDateTime(dtval)
        retobj = False
    else:
        dtobj = dtval

    dtobj = dtobj + relativedelta(months=months)
    if retobj:
        return dtobj
    else:
        return printDateTime(dtobj)
    
def isPandas(timeval):
    if isinstance(timeval, Timestamp):
        return True
    return False

def isDate(timeval):
    if isinstance(timeval, datetime.date):
        return True
    return False

def isDateTime(timeval):
    if isinstance(timeval, datetime.datetime):
        return True
    return False
    
def isFuture(dtval):
    dtobj = getDateTime(dtval)
    if dtobj is not None:
        if dtobj > dt.now():
            return True
    return False

def convertPandasTimestamp(timeval):
    if isPandas(timeval):
        return printDateTime(timeval.date()) #to_pydatetime()
    return timeval

def getTimeSuffix(tsval=None):
    if tsval is None:
        return printDateTime(clock(), "%Y%m%d")
    else:
        return printDateTime(tsval, "%Y%m%d")
              

def clock(comment=None, showTime=True):
    val = dt.now()
    if comment is None:
        comment = "Begin"
    if showTime is True:
        print("Current Time is {0} for {1}".format(printDateTime(val, "%a %b %d, %Y %H:%M:%S"), comment))
    return val, comment


def update(start, proc, total):
    if total > 0 and proc > 0:
        dtime = (dt.now() - start).seconds
        rate = proc / dtime
        estT = total / rate
        remT = estT - dtime
        
        remaining = round(remT/60.0,1)
        fullrate  = round(rate,0)

        print("  Processed {0}/{1}. There are {2} minutes remaining  (R={3} evt/sec)".format(proc, total, remaining, fullrate))
        

def elapsed(start, comment=None, showTime=True):
    if isinstance(start, tuple):
        try:
            comment=start[1]
            start=start[0]
        except:
            start=start[0]
            
    if comment is None:
        comment = "End"
    elif comment is not None:
        if not comment.startswith("Done with"):
            comment = "Done with {0}".format(comment)
          
                  
    end, _ = clock(comment=comment, showTime=showTime)
    dtime = end-start
    seconds, microseconds = dtime.seconds, dtime.microseconds
    
    
    print("Process [{0}] took ".format(comment), end="")
    ## Convert to minutes
    
    units = None
    if seconds > 60:
        result = round(seconds/60.0, 1)
        units  = "minutes"
    elif seconds > 0.5:
        result = round(seconds, 1)
        units  = "seconds"
    elif microseconds > 1e3:
        result = round(microseconds/1e3, 0)
        units  = "millseconds"
    else:        
        result = round(microseconds, 0)
        units  = "microseconds"

    print("{0} {1}.".format(result, units))