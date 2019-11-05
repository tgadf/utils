from os.path import basename, splitext, dirname, getsize
from datetime import datetime, timedelta
from fsUtils import isFile, isDir


###############################################################################
#
# General (get/save)
#
###############################################################################
def getSize(ifile, units="MB", debug=False):
    if isFile(ifile) is False:
        return None, None
    
    fsize = getsize(ifile)
    units = "B"
    if fsize > 1e9:
        fsize /= 1e9
        units = "GB"
    elif fsize > 1e6:
        fsize /= 1e6
        units = "MB"
    elif fsize > 1e3:
        fsize /= 1e3
        units = "kB"
        
    if debug is True:
        print("  --> This file is {0}{1}.".format(round(fsize,1), units))
    return fsize, units


def getBasename(ifile):
    if ifile is None:
        return None
    bname = basename(ifile)
    return bname

def getDirname(ifile):
    if ifile is None:
        return None
    dname = dirname(ifile)
    return dname

def getBaseFilename(ifile):
    if ifile is None:
        return None
    bfname = splitext(getBasename(ifile))[0]
    return bfname

def getExt(ifile):
    if ifile is None:
        return None
    ext = splitext(getBasename(ifile))[1]
    return ext

def getFileBasics(ifile):
    if isFile(ifile):
        return getDirname(ifile),getBaseFilename(ifile),getExt(ifile)
    else:
        return [None,None,None]

def getDirBasics(idir):
    if isDir(idir):
        return idir.split('/')
    else:
        return []
    
def getCreatedTime(ifile):
    if isFile(ifile):
        return datetime.fromtimestamp(path.getctime(ifile))
    else:
        return None
    
def getModifiedTime(ifile):
    if isFile(ifile):
        return datetime.fromtimestamp(path.getmtime(ifile))
    else:
        return None