from os.path import basename, splitext, dirname, getsize
from fsUtils import isFile, isDir


###############################################################################
#
# General (get/save)
#
###############################################################################
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