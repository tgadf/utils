""" A simple utility class for measuring timing of processes """

__all__ = ["Timestat"]

from time import perf_counter
from .timeutil import Now
from .timeconv import TimeConv
    
        
###############################################################################
# Process Timer
###############################################################################
class Timestat:
    def __init__(self, cmt, ind=0, showTime=True, verbose=True):
        assert isinstance(cmt, str), f"cmt [{cmt}] must be a str"
        assert isinstance(ind, int), f"ind {ind} must be a int"
        assert isinstance(showTime, bool), f"showTime {showTime} must be a bool"
        assert isinstance(verbose, bool), f"verbose {verbose} must be a bool"
        
        self.cmt = cmt
        self.ind = " " * ind
        self.prefix = f"{self.ind} [{self.cmt}]"
        self.showTime = showTime
        self.verbose = verbose
        self.now = Now()
        self.tc = TimeConv()
        self.start()
        
    def start(self):
        if self.verbose is True:
            print(f"{self.prefix} | StartTime {self.now.get()}")
        self.start = perf_counter()
        
    def stop(self, cmt=None):
        self.end = perf_counter()
        if self.verbose is True:
            runtime = self.tc.get(self.end - self.start)
            print(f"{self.prefix} | RunTime {runtime}.", end="")
            term = f"  >> {cmt} <<" if isinstance(cmt, str) else ""
            print(f"{term}  {self.now.get()}")
        
    def init(self, n=None, N=None):
        def getStatus(n, N):
            denom = N if isinstance(N, (str, int)) else "?"
            numer = n if isinstance(n, (str, int)) else "?"
            return f"{numer}/{denom}"
        if self.verbose is True:
            print(f"{self.prefix} | {getStatus(n,N): <10} ... ", end="")

    def comment(self, cmt):
        term = f"{self.prefix} | {cmt}"
        print(term)        

    def update(self, n=None, N=None, cmt=None, init=True):
        def getRemaining(deltaT, n, N):
            if deltaT < 1 or n == 0:
                return "? Seconds"
            elif n == N:
                return "0 Seconds"
            ETR = deltaT * (N / n - 1)
            retval = self.tc.get(ETR)
            return retval

        def getStatus(n, N):
            denom = N if isinstance(N, (str, int)) else "?"
            numer = n if isinstance(n, (str, int)) else "?"
            return f"{numer}/{denom}"

        self.end = perf_counter()
        if self.verbose is True:
            deltaT = self.end - self.start
            runtime = self.tc.get(deltaT)
            
            updateStr = f"{self.prefix} | {getStatus(n,N): <10} : RunTime {runtime}." if init is True else f"RunTime {runtime}."
            print(f"{updateStr}", end="")
                
            if all([isinstance(x, int) for x in [n, N]]):
                print(f"  (ETR {getRemaining(deltaT, n, N)})", end="")
            term = f"  >> {cmt} <<" if isinstance(cmt, str) else ""
            print(term)