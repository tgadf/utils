""" A simple utility class for measuring timing of processes """

__all__ = ["RecentFiles"]

import re
from datetime import datetime, timedelta
from pandas import Timedelta, Timestamp
from fileutils import FileInfo

class fileTimeDelta:
    def __init__(self, debug=False):
        self.debug = debug
        
        self.pattern = re.compile(r"\d+ \w+")
        self.ogexpr  = None
        self.expr    = None
        self.td      = None        
        self.opr     = None
        
        
    ############################################################################################
    ## Set Operator
    ############################################################################################
    def setOperator(self, operator):
        if operator in ['=', '>=', '<=', '>', '<']:
            self.opr = operator
        else:
            raise ValueError("Operator [{0}] is not known".format(operator))
            
        
    ############################################################################################
    ## Set TimeDelta
    ############################################################################################
    def setTimeAndUnit(self, timeUnit):
        timeval,unit = timeUnit.split()
        try:
            timeval = int(timeval)
        except:
            raise ValueError("Could not create integer of {0}".format(timeval))

        ## Convert To Days/Seconds
        days,seconds,microseconds = 0,0,0
        if unit in ["hour", "hours", "hrs"]:
            seconds = timeval * 3600
        elif unit in ["minute", "minutes", "min"]:
            seconds = timeval * 60
        elif unit in ["second", "seconds", "sec", "s"]:
            seconds = timeval * 1
        elif unit in ["day", "days", "d"]:
            days = timeval * 1
        else:
            raise ValueError("Unit [{0}] is not known".format(unit))


        self.td = Timedelta(timedelta(days = days, seconds=seconds, microseconds=microseconds))
        
        
    ############################################################################################
    ## Parse Expression
    ############################################################################################
    def parseExpr(self):        
        self.expr = self.expr.lower()
        timeUnits = re.findall(self.pattern, self.expr)
        if len(timeUnits) == 1:
            timeUnit = timeUnits[0]
            operator = re.sub(pattern=timeUnit, repl="", string=self.expr).strip()
        else:
            raise ValueError("Could not find time units in {0}".format(self.ogexpr))
            
        return timeUnit, operator
        
        
    ############################################################################################
    ## Master Getter Function
    ############################################################################################
    def getDelta(self, expr):
        self.ogexpr = expr
        self.expr   = expr
        
        ################################################
        ## Parse Expression
        ################################################
        timeUnit, operator = self.parseExpr()
            
            
        ################################################
        ## Set Operator
        ################################################
        self.setOperator(operator)
            
            
        ################################################
        ## Convert Time/Unit To TimeDelta
        ################################################
        self.setTimeAndUnit(timeUnit)
        
        
    ############################################################################################
    ## isTrue()
    ############################################################################################
    def isTrue(self, td):
        if td is None:
            return True
        return {'<': td < self.td, '<=': td <= self.td,
                    '=': td == self.td,
                    '>': td > self.td, '>=': td >= self.td}[self.opr]


    ############################################################################################
    ## Debug/Show
    ############################################################################################
    def show(self):
        print("="*5,"FileTimeDelta Results","="*5)
        print("Original Expression: '{0}'".format(self.ogexpr))
        print("Operator:            {0}".format(self.opr))
        print("TimeDelta:           {0}".format(self.td))


class fileModTimeDelta:
    def __init__(self, ifile, now=None, lastModified=None):
        self.lastModified = lastModified
        self.err = False
        self.now = Timestamp.today().round('s') if now is None else now
            
        
        ###########################################################################
        # Find Mod Times
        ###########################################################################
        #modTime      = datetime.fromtimestamp(getmtime(ifile))
        modTime = FileInfo(ifile).time()
        modTime = Timestamp(modTime) if modTime is not None else None
        
        ###########################################################################
        # Compute Time Deltas
        ###########################################################################
        if modTime is None:
            deltaLastMod = None
            deltaNow     = None
        else:
            deltaLastMod = self.lastModified - modTime if self.lastModified is not None else None
            deltaNow = self.now - modTime        
        
        
        ###########################################################################
        # Set Variables
        ###########################################################################
        self.modTime      = modTime
        self.deltaLastMod = Timedelta(deltaLastMod).round('s') if deltaLastMod is not None else None
        self.deltaNow     = Timedelta(deltaNow).round('s') if deltaNow is not None else None
        
        
    def getLastModTime(self):
        return self.modTime
    
    def getDeltaNow(self):
        return self.deltaNow
    
    def getDeltaLastMod(self):
        return self.deltaLastMod
    
    def getErr(self):
        return self.err
    

class RecentFiles:
    def __init__(self, files=None, debug=False):
        self.debug        = debug
        self.files        = files
        self.fileModTimes = None
        self.ftd          = None
        self.lastModified = None
        self.now          = Timestamp.today().round('s')

        
    #################################################################################
    # File Utils
    #################################################################################
    def setFiles(self, files):
        self.files = files
        if self.debug:
            print("Setting {0} files".format(len(self.files)))

    def setLastModTimeFromFile(self, ifile):
        self.lastModified = FileInfo(ifile).time()
        self.lastModified = Timestamp(self.lastModified) if self.lastModified is not None else None
            
    def setFileModTimes(self):
        self.fileModTimes = {ifile: fileModTimeDelta(ifile, now=self.now, lastModified=self.lastModified) for ifile in self.files}
    
    def setFileTimeDelta(self, expr):
        self.ftd = fileTimeDelta()
        self.ftd.getDelta(expr)
        if self.debug:
            self.ftd.show()


    #################################################################################
    # Get Files By Recency From Now
    #################################################################################    
    def getFilesByRecency(self, expr, debug=False):
        self.setFileTimeDelta(expr)
        self.setFileModTimes()
        if debug:
            self.ftd.show()
            N = len(self.fileModTimes)
            for i,(ifile, fmtd) in enumerate(self.fileModTimes.items()):
                print("{0}/{1}\t{2: <60}{3}  {4}  {5}".format(i, N, FileInfo(ifile).basename, fmtd.modTime, fmtd.getDeltaNow(),
                                                              self.ftd.isTrue(fmtd.getDeltaNow())))
        retval = [ifile for ifile, fmtd in self.fileModTimes.items() if self.ftd.isTrue(fmtd.getDeltaNow())]
        return retval


    #################################################################################
    # Get Recent Files
    #################################################################################    
    def getFilesByModTime(self, expr, ifile, debug=False):
        self.setFileTimeDelta(expr)
        self.setLastModTimeFromFile(ifile)
        self.setFileModTimes()
        if debug:
            self.ftd.show()
            N = len(self.fileModTimes)
            for i,(ifile, fmtd) in enumerate(self.fileModTimes.items()):
                print("{0}/{1}\t{2: <60}{3}  {4}  {5}".format(i, N, FileInfo(ifile).basename, fmtd.modTime, fmtd.getDeltaLastMod(),
                                                              self.ftd.isTrue(fmtd.getDeltaLastMod())))
        retval = [ifile for ifile, fmtd in self.fileModTimes.items() if self.ftd.isTrue(fmtd.getDeltaLastMod())]
        return retval