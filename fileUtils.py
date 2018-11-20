from os.path import basename, splitext, dirname, getsize


###############################################################################
#
# General (get/save)
#
###############################################################################
def getBasename(ifile):
    bname = basename(ifile)
    return bname

def getDirname(ifile):
    dname = dirname(ifile)
    return dname

def getBaseFilename(ifile):
    bfname = splitext(getBasename(ifile))[0]
    return bfname

def getExt(ifile):
    ext = splitext(getBasename(ifile))[1]
    return ext

def getFileBasics(ifile):
    return getDirname(ifile),getBaseFilename(ifile),getExt(ifile)