""" A simple utility class for measuring timing of processes """

__all__ = ["TimeConv"]

from datetime import timedelta

##############################################################################################################
# Convert Seconds Into Human Readable
##############################################################################################################
class TimeConv:
    def __init__(self):
        self.days = None
        self.hrs  = None
        self.min  = None
        self.sec  = None
        
    def get(self, tval):
        self.tval = tval
        td = str(timedelta(seconds=tval))
        if "days, " in td:
            splitvals = td.split("days, ")
            if len(splitvals) == 2:
                try:
                    days = int(splitvals[0])
                    td = splitvals[1]
                except:
                    print(f"Could not split time [{td}]")
        else:
            days = 0
                    
        try:
            hours,minutes,seconds = [int(round(float(x),0)) for x in td.split(":")]
        except:
            print(f"Could not parse time [{td}]")
            days    = 0
            hours   = 0
            minutes = 0
            seconds = 0
        
        
        retval = []
        if days > 0:
            cmt = f"{days} Days" if days > 1 else f"{days} Day" 
            retval.append(cmt)
            
        if hours > 0:
            cmt = f"{hours} Hours" if days > 1 else f"{hours} Hour" 
            retval.append(cmt)
            
        if minutes > 0:
            cmt = f"{minutes} Minutes" if days > 1 else f"{minutes} Minute" 
            retval.append(cmt)
            
        if seconds > 0:
            cmt = f"{seconds} Seconds" if days > 1 else f"{seconds} Second" 
            retval.append(cmt)
            
        self.days    = days
        self.hours   = hours
        self.minutes = minutes
        self.seconds = seconds
            
        return " and ".join(retval[:2])