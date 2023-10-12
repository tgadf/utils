""" A simple utility class for measuring timing of processes """

__all__ = ["FileInfo", "DirInfo"]

from pathlib import Path, PurePosixPath, PosixPath
from datetime import datetime
from shutil import move, copy, rmtree


###############################################################################
# File System Posix Path
###############################################################################
class FSPath:
    def __repr__(self):
        return f"FSPath(path={self.path})"

    def __init__(self, path):
        self.path = Path(path)
        self.isPath = None
        self.stat = None

    def isPath(self):
        return self.access()

    def access(self):
        if self.isPath is False:
            return False
        if self.isPath is None:
            try:
                self.path.exists()
                self.isPath = True
            except:
                self.isPath = False
        return self.isPath
            
    def exists(self):
        if self.access():
            return self.path.exists()
        return None
    
    def time(self):
        if self.stat is not None: return self.stat.getModTime()
        if self.access():
            self.stat = FileStat(self.path)
            return self.stat.getModTime()
        return None
    
    def stat(self):
        if self.stat is not None: return self.stat.stat
        if self.access():
            self.stat = FileStat(self.path)
            return self.stat.stat
        return None
        
    def size(self):
        if self.stat is not None: return self.stat.getSize()
        if self.access():
            self.stat = FileStat(self.path)
            return self.stat.getSize()
        return None
    
    def isFile(self):
        if self.access():
            return self.path.is_file()
        return None
    
    def isDir(self):
        if self.access():
            return self.path.is_dir()
        return None
    
    
    ##################################################################################################
    # Path() I/O
    ##################################################################################################
    def touchFile(self, debug=True):
        if self.access():
            if not self.path.is_file():
                if debug: print("  ==> Touching File: {0}".format(self.path))
                self.path.touch()

    def rmFile(self, debug=True):
        if self.access():            
            if debug: print("  ==> Removing {0}".format(self.path))

            #remove(self.path)
            self.path.unlink(missing_ok=True)
            
    def mvFile(self, dstPath, debug=True):
        if self.access():
            dstPath = dstPath.dirpath.path if isinstance(dstPath, FileInfo) else Path(dstPath)
            if debug: print("  ==> Moving {0} to {1}".format(self.path, dstPath))
            move(self.path, dstPath)
            #self.path.rename(dstPath)
            
    def cpFile(self, dstPath, debug=True):
        if self.access():
            dstPath = dstPath.dirpath.path if isinstance(dstPath, FileInfo) else Path(dstPath)
            if debug: print("  ==> Copying {0} to {1}".format(self.path, dstPath))
            copy(self.path, dstPath)
            #self.path.rename(dstPath)
            
    def mkDir(self, debug=True):
        if self.access():
            if not self.path.is_dir():
                if debug: print("  ==> Making Directory: {0}".format(self.path))
                self.path.mkdir()
            
    def rmDir(self, debug=True):
        if self.access():
            if debug: print("  ==> Removing Directory: {0}".format(self.path))
            rmtree(self.path)
            
    def mvDir(self, dstPath, debug=True):
        if self.access():
            dstPath = dstPath.dirpath.path if isinstance(dstPath, DirInfo) else Path(dstPath)
            if dstPath.exists():
                raise ValueError(f"  ==> {dstPath} already exists.")
            if debug: print("  ==> Moving {0} to {1}".format(self.path, dstPath))
            move(self.path, dstPath)
                        
    def glob(self, pattern="*", lazy=True, debug=True):
        if self.access():
            if debug: print("Running glob({0}/{1})".format(self.path, pattern))
            globVal = self.path.glob(pattern)
            retval = globVal if lazy is True else list(globVal)
            return retval
        return None
    


#######################################################################################################################
# File System Base Class
#######################################################################################################################
class FSBase:
    def __repr__(self):
        return f"FSBase(path={self.path})"
        
    def __init__(self, fsValue):
        if isinstance(fsValue, (str,Path,PurePosixPath)):
            self.path     = PurePosixPath(fsValue)
        elif isinstance(fsValue, (FileInfo,DirInfo)):
            self.path     = fsValue.path
        elif fsValue is None:
            raise ValueError("fsInfo input is None")
        else:
            raise ValueError("fsInfo does not accept the object [{0}]".format(type(fsValue)))
            
        self.name     = self.path.name
        self.basename = self.path.stem
        self.ext      = self.path.suffix
        self.str      = str(self.path)
        self.dirpath  = FSPath(self.path)
        self.parent   = self.path.parent
    
        self.isPath   = self.dirpath.isPath
        self.exists   = self.dirpath.exists
    
    
    ##################################################################################################
    # PosixPath() Information
    ##################################################################################################    
    def getJoinStr(self, joinValue):
        try:
            retval = str(joinValue)
        except:
            raise TypeError("Trying to join path with something [{0}] that can't be a string".format(joinValue))
        return retval
            
    def join(self, jValues):
        path = self.path
        jValues = jValues if isinstance(jValues,(list,tuple)) else [jValues]
        for jValue in jValues:
            path = path.joinpath(self.getJoinStr(jValue))
        retval = DirInfo(path) if len(path.suffix) == 0 else FileInfo(path)
        return retval
    
    def joinDir(self, jValues):
        return DirInfo(self.join(jValues).path)
    
    def joinFile(self, jValues):
        return FileInfo(self.join(jValues).path)

                
    def parents(self):
        return {i: pval.name for i,pval in enumerate(list(self.path.parents)) if len(pval.name) > 0}
        
        
        
#######################################################################################################################
# Dir Info Class
#######################################################################################################################
class DirInfo(FSBase):
    def __repr__(self):
        return f"DirInfo(path={self.path})"
    
    def __init__(self, fsValue):
        super().__init__(fsValue)
        self.glob     = self.dirpath.glob
        self.mkDir    = self.dirpath.mkDir
        self.mvDir    = self.dirpath.mvDir
        self.isDir    = self.dirpath.isDir
        self.rmDir    = self.dirpath.rmDir
        
    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, DirInfo):
            return self.path == other.path
        return False
        
    def get(self):
        return self
    
    def getFiles(self):
        return self.glob("*.*", debug=False, lazy=False)
    
    def getDirs(self):
        retval   = [dinfo for dinfo in [DirInfo(dirItem) for dirItem in self.glob("*", debug=False, lazy=False)] if dinfo.isDir()]
        return retval
            
        
#######################################################################################################################
# File Info Class
#######################################################################################################################
class FileInfo(FSBase):
    def __repr__(self):
        return f"FileInfo(path={self.path})"
    
    def __init__(self, fsValue):
        super().__init__(fsValue)
        self.time     = self.dirpath.time
        self.stat     = self.dirpath.stat
        self.size     = self.dirpath.size
        self.touch    = self.dirpath.touchFile
        self.isFile   = self.dirpath.isFile
        self.rmFile   = self.dirpath.rmFile
        self.mvFile   = self.dirpath.mvFile
        self.cpFile   = self.dirpath.cpFile

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, FileInfo):
            return self.path == other.path
        return False
        
    def get(self):
        return self        


#######################################################################################################################
# File Stat Class
#######################################################################################################################
class FileStat:
    def __init__(self, fsValue):
        if isinstance(fsValue,(PosixPath,Path)):
            self.path = fsValue
        elif isinstance(fsValue, FileInfo):
            self.path = fsValue.path
        else:
            self.path = Path(fsValue)
            
        if self.path.is_file():
            self.stat = self.path.stat()
            self.mod  = datetime.fromtimestamp(self.stat.st_mtime)
            self.size = self.stat.st_size
        else:
            self.stat = None
            self.mod  = None
            self.size = None

    def getModTime(self):
        return self.mod
    
    def getSize(self):
        mag   = self.size
        unit  = "B"
        units = [('B', 1), ('kB', 1024), ('MB', 1048576), ('GB', 1073741824)]
        for exp in range(1,len(units)):
            if mag/units[exp][1] < 1:
                mag  = mag/units[exp-1][1]
                unit = units[exp-1][0]
                break
                
        if mag >= 100:
            return (int(round(mag,0)),unit)
        elif mag >= 10:
            return (round(mag,1),unit)
        else:
            return (round(mag,2),unit)
