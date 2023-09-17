""" A simple utility class for measuring timing of processes """

__all__ = ["TermTime", "TermTimeTS", "getTT"]

from datetime import timedelta, date
from pandas import to_datetime, Timestamp
from .timeconv import TimeConv

                    
##############################################################################################################
# Tool To Terminate Process At A Future Time
##############################################################################################################
class TermTimeTS:
    def __init__(self, day = "tomorrow", time = "7am"):
        #print("{0} {1} {2}".format("="*25,"termTime(day={0},time={1})".format(day,time),"="*25))
        today    = date.today()
        tomorrow = today + timedelta(days=1)
        if day.lower() == "tomorrow":
            dayStr = tomorrow.strftime("%m/%d/%Y")
        elif day.lower() == "today":
            dayStr = today.strftime("%m/%d/%Y")
        else:
            try:
                dayStr = to_datetime(day).strftime("%m/%d/%Y")
            except:
                raise ValueError("Could not get date from [{0}]".format(day))

        timeStr  = "--".join([dayStr, time])
        try:
            self.ts = to_datetime(timeStr)
        except:
            self.ts = None
            raise ValueError("Could not set terminate time for [{0}/{1}]=[{2}]".format(dayStr,time,timeStr))
            
    def get(self):
        return self.ts


def getTT(skipEOD=False, manualTime=None, vacation=False):
    today = Timestamp.today()
    dow   = today.dayofweek
    if vacation is True:
        ttTom = TermTimeTS("tomorrow", "10:50am").get()
        ttTod = TermTimeTS("today", "7:00pm").get()
    elif dow in [6,0,1,2,3]:  ## Tomorrow is a school day
        ttTom = TermTimeTS("tomorrow", "6:50am").get()
        ttTod = TermTimeTS("today", "7:00pm").get()
    else: ## Tomorrow is the weekend
        ttTom = TermTimeTS("tomorrow", "9:50am").get()
        ttTod = TermTimeTS("today", "7:00pm").get()
        
    endTime = ttTod if ((ttTod < ttTom) & (ttTod > today)) else ttTom
    endTime = ttTom if skipEOD is True else endTime
    endTime = TermTimeTS(manualTime[0], manualTime[1]).get() if (isinstance(manualTime,(list,tuple)) and len(manualTime) == 2) else endTime
    tt = TermTime(endTime=endTime)
    return tt


class TermTime:
    def __init__(self, day = "tomorrow", time = "7am", endTime=None):
        if isinstance(day,str) and isinstance(time,str) and endTime is None:
            print("{0} {1} {2}".format("="*25,"termTime(day={0},time={1})".format(day,time),"="*25))
            ts = TermTimeTS(day, time)
            self.endTime = ts.get()
            print("   ====> Terminate Time Set To {0} <====".format(self.endTime))
        elif isinstance(endTime,Timestamp):
            self.endTime = endTime
            print("   ====> Terminate Time Set To {0} <====".format(self.endTime))
        
        tc   = TimeConv()
        print("   ====> Will Terminate Process {0} From Now".format(tc.get((self.endTime - Timestamp.today()).seconds)))
        
        
    def isFinished(self):
        retval = Timestamp.today() > self.endTime
        if retval is True:
            print("   ====> Terminate Time [{0}] Is Reached <====".format(self.endTime))
        return retval