""" I/O Utility """

__all__ = ["YAMLIO", "JSONIO", "PickleIO", "HTMLIO", "XMLIO",
           "CSVIO", "FileIO", "getFile", "getHTML"]


###############################################################################
# File Types
###############################################################################
import joblib
import json
import yaml
import h5py
from pathlib import PosixPath, Path
from io import StringIO
from xml.etree import ElementTree
from bs4 import BeautifulSoup
from pandas import read_csv

###############################################################################
# Utils
###############################################################################
from .fsinfo import FileInfo


class IOBase:
    def __init__(self, ifile, debug=False):
        self.ifile = ifile
        self.debug = debug
        
    def getDebug(self):
        if self.debug:
            print("")
            
            
class HD5IO:
    def __init__(self, debug=False):
        self.debug = debug
        
    def get(self, ifile):
        return h5py.File(ifile, 'r')
    
    def save(self, ifile, idata):
        h5py.File(ifile, 'w')
        yaml.dump(idata, open(ifile, "w"), default_flow_style=False, allow_unicode=True)
        
        
class YAMLIO:
    def __init__(self, debug=False):
        self.debug = debug
        
    def get(self, ifile):
        return yaml.load(open(ifile), Loader=yaml.FullLoader)
    
    def save(self, ifile, idata):
        yaml.dump(idata, open(ifile, "w"), default_flow_style=False, allow_unicode=True)

        
class JSONIO:
    def __init__(self, debug=False):
        self.debug = debug
        
    def get(self, ifile):
        return json.load(open(ifile, "r+"))
    
    def save(self, ifile, idata):
        json.dump(obj=idata, fp=open(ifile, "w+"))
        

class PickleIO:
    def __init__(self, debug=False):
        self.debug = debug
        
    def get(self, ifile):
        return joblib.load(ifile)
    
    def save(self, ifile, idata):
        joblib.dump(idata, ifile, compress=True)
        

class HTMLIO:
    def __init__(self, debug=False):
        self.debug = debug
        
    def get(self, ifile):
        self.bsdata = ifile
        if isinstance(ifile, FileInfo):
            self.bsdata = BeautifulSoup(open(ifile.path).read(), features="lxml")
        elif isinstance(ifile, (PosixPath, Path)):
            self.bsdata = BeautifulSoup(open(ifile).read(), features="lxml")
        elif isinstance(ifile, str):
            finfo = FileInfo(ifile)
            if finfo.isFile():
                if finfo.ext == ".p":
                    self.bsdata = BeautifulSoup(PickleIO().get(ifile), features="lxml")
                elif finfo.ext in [".html", ".htm"]:
                    self.bsdata = BeautifulSoup(open(ifile).read(), features="lxml")
                else:
                    raise ValueError("File extention [{0}] is not recognized".format(finfo.ext))
            else:
                self.bsdata = BeautifulSoup(StringIO(ifile), features="lxml")
        elif isinstance(ifile, bytes):
            self.bsdata = BeautifulSoup(ifile, features="lxml")
        else:
            raise ValueError("Can't create BeautifulSoup() from [{0}] input".format(type(ifile)))
            
        return self.bsdata
    
    def save(self, ifile, idata):
        raise ValueError("Saving html/bs4 data doesn't work yet.")
        

class XMLIO:
    def __init__(self, debug=False):
        self.debug = debug
        
    def get(self, ifile):
        return ElementTree.parse(ifile)

    def save(self, ifile, idata):
        with open(ifile, 'wb') as f:
            f.write(idata)
        

class CSVIO:
    def __init__(self, debug=False):
        self.debug = debug
        
    def get(self, ifile, **kwargs):
        return read_csv(ifile, **kwargs)

    def save(self, ifile, idata):
        
        raise ValueError("Saving csv doesn't work yet!")
        with open(ifile, 'wb') as f:
            f.write(idata)
        
        
class FileIO:
    def __init__(self, **kwargs):
        self.debug = kwargs.get('debug', kwargs.get('verbose', False))
        self.extIO = {".p": PickleIO(), ".pickle": PickleIO(), ".json": JSONIO(), ".yaml": YAMLIO(),
                      ".html": HTMLIO(), ".htm": HTMLIO(), ".xml": XMLIO(), ".csv": CSVIO()}

    def getIO(self, finfo):
        ext = finfo.ext
        return self.extIO[ext] if ext in self.extIO else None
                
    def get(self, ifile, **kwargs):
        finfo = FileInfo(ifile)
        extIO = self.getIO(finfo)
        assert extIO is not None, f"Unknown file extension: [{ifile}] [{finfo.ext}]"
        if finfo.exists():
            retval = extIO.get(finfo.str, **kwargs)
            return retval
        else:
            if self.debug:
                print(f"[{ifile}] does not exist. Returning None")
            return None
    
    def save(self, ifile, idata):
        finfo = FileInfo(ifile)
        extIO = self.getIO(finfo)
        extIO.save(finfo.str, idata)
        
        
def getFile(ifile: str) -> 'bytes':
    io = FileIO()
    return io.get(ifile)


def getHTML(ifile: str | bytes) -> 'BeautifulSoup':
    hio = HTMLIO()
    if isinstance(ifile, bytes):
        return hio.get(ifile)
    elif isinstance(ifile, str):
        if ifile.startswith("/"):
            return hio.get(getFile(ifile))
        else:
            return hio.get(ifile)