# coding: utf-8

from sklearn.externals import joblib
from os.path import getsize, exists, join, dirname, basename, splitext
from os import listdir
from sklearn.model_selection import train_test_split
from glob import glob, glob1
from numpy import ndarray, reshape
from pandas import DataFrame, Series, read_csv
import json
import yaml
from timeUtils import clock, elapsed
from pandasUtils import dropColumns


    
##########################################################################################
#
# Spark Data Helpers
#
##########################################################################################   
def saveSparkData(spdf, dbname, tablename):
    start, cmt = clock("Saving spark dataframe to {0}.{1}".format(dbname, tablename))
    spdf.write.mode('overwrite').format('parquet').saveAsTable("{0}.{1}".format(dbname, tablename))
    elapsed(start, cmt)
    
def appendSparkData(spdf, dbname, tablename):
    start, cmt = clock("Appending spark dataframe to {0}.{1}".format(dbname, tablename))
    spdf.write.mode('append').format('parquet').saveAsTable("{0}.{1}".format(dbname, tablename))
    elapsed(start, cmt)
        
    
    

def getBasename(name):
    bname = basename(name)
    return bname

def getDirname(name):
    dname = dirname(name)
    return dname


def findPattern(basedir, pattern, debug = False):
    if basedir == None: return []
    files = [x for x in listdir(basedir) if x.find(pattern) != -1]
    files = glob(join(basedir, "*"+pattern+"*"))
    return files
     
def findPatternExt(basedir, pattern, ext, debug = False):
    if basedir == None: return []
    files = findExt(basedir, ext)
    files = [x for x in files if x.find(pattern) != -1]
    return files 
    
def findExt(basedir, ext, debug = False):
    if basedir == None: return []
    if isinstance(ext, list):
        files = []
        for exten in ext:
            files += [join(basedir,x) for x in glob1(basedir, "*"+exten)]
    else:
        files = [join(basedir,x) for x in glob1(basedir, "*"+ext)]
    return files






##########################################################################################
#
# Generic file io functions
#
##########################################################################################
def showSize(filename):
    """
    Show file size
    
    Inputs: filename
    Outputs: None
    """
    fsize = getsize(filename)
    units = "B"
    if fsize > 1e6:
        fsize /= 1e6
        units = "MB"
    elif fsize > 1e3:
        fsize /= 1e3
        units = "kB"
    print("  --> This file is {0}{1}.".format(round(fsize,1), units))



###############################################################################
#
# YAML
#
###############################################################################
def saveYaml(yfile, ydata):
    yaml.dump(ydata, open(yfile, "w"), default_flow_style=False, allow_unicode = True)

def getYaml(yfile):
    ydata = yaml.load(open(yfile))
    return ydata



###############################################################################
#
# JSON
#
###############################################################################
def saveJSON(jfile, jdata):
    json.dump(jdata, open(jfile, "w"))

def getJSON(jfile):
    jdata = json.load(open(jfile))
    return jdata



###############################################################################
#
# PICKLE
#
###############################################################################
def saveJoblib(data, filename, compress=True):
    """
    Save data using joblib
    
    Inputs:
      > data: anything that can be pickled
      > filename: the saved filename
      > compress (True by default): compress the output file?
      
    Output:
      > None
    """
    savePICKLE(data, filename, compress)
    
def savePICKLE(pdata, pfile, compress=True):
    """
    Save data using joblib
    
    Inputs:
      > pdata: anything that can be pickled
      > pfile: the saved filename
      > compress (True by default): compress the output file?
      
    Output:
      > None
    """
    joblib.dump(pdata, pfile, compress=compress)
    showSize(pfile)

def loadJoblib(filename):
    """
    Load data using joblib
    
    Inputs:
      > filename: the saved filename
      
    Output:
      > None
    """
    return getPICKLE(filename)
    
def getPICKLE(pfile):
    """
    Load data using joblib
    
    Inputs:
      > filename: the saved filename
      
    Output:
      > None
    """
    data = joblib.load(pfile)
    return data



###############################################################################
#
# General
#
###############################################################################
def saveFile(ifile, idata):
    if isinstance(idata, pickle):
        savePICKLE(pfile=ifile, pdata=idata)
    elif isinstance(idata, json):
        saveJSON(jfile=ifile, jdata=idata)
    elif isinstance(idata, yaml):
        saveYaml(yfile=ifile, ydata=idata)
    else:
        raise ValueError("Did not recognize format {0}".format(type(idata)))
        
        
def getFile(ifile):
    ext = splitext(basename(ifile))[1]
    if ext == ".p":
        return getPICKLE(pfile=ifile)
    elif ext == ".json":
        return getJSON(jfile=ifile)
    elif ext == ".yaml":
        return getYaml(yfile=ifile)
    else:
        raise ValueError("Did not recognize extension {0}".format(ext))
