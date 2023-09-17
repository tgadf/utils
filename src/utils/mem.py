""" Utilities For Memory Allocation """

__all__ = ["TraceMemory"]

import tracemalloc

class TraceMemory:
    def __init__(self, **kwargs):
        self.verbose  = kwargs.get('verbose', False)
        self.start    = tracemalloc.start
        self.stop     = tracemalloc.stop
        self.shaphots = []
    
    def snap(self):
        self.snapshots.append(tracemalloc.take_snapshot())

    def compare(self):
        if len(self.snapshots) >= 2:
            top_stats = self.snapshots[-1].compare_to(self.snapshots[0], 'lineno')
            return top_stats
        return None
    
    
    def traced(self, reset=False, ret=False):
        size,peak = tracemalloc.get_traced_memory()
        size = self.getSize(size)
        size = f"{size[0]}{size[1]}"
        peak = self.getSize(peak)
        peak = f"{peak[0]}{peak[1]}"
        if reset is True:
            tracemalloc.reset_peak()
        if ret:
            return (size,peak)
        print(f"  TraceMemory  ==> Size = {size: <7}   |   Peak = {peak: <7}")
        

    def getSize(self, size):
        mag   = size
        unit  = "B"
        units = [('B', 1), ('kB', 1024), ('MB', 1048576), ('GB', 1073741824), ('TB', 1099511627776)]
        for exp in range(1,len(units)+1):
            if size/units[exp][1] < 1:
                mag  = size/units[exp-1][1]
                unit = units[exp-1][0]
                break
                
        if mag >= 100:
            return (int(round(mag,0)),unit)
        elif mag >= 10:
            return (round(mag,1),unit)
        else:
            return (round(mag,2),unit)
