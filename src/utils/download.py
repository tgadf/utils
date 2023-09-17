""" Basic download functions """

__all__ = ["getTT"]

from timeutils import TermTime, TermTimeTS
from pandas import Timestamp

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