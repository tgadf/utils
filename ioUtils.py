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
import pickle
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
    if fsize > 1e9:
        fsize /= 1e9
        units = "BB"
    elif fsize > 1e6:
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

def getYaml(yfile, version=3, debug=False):
    if debug:
        print("Loading {0}".format(yfile))
    ydata = yaml.load(open(yfile), Loader=yaml.FullLoader)
    return ydata





###############################################################################
#
# HTML
#
###############################################################################
def saveHTML(yfile, ydata):
    raise ValueError("Don't do this!!")
    yaml.dump(ydata, open(yfile, "w"), default_flow_style=False, allow_unicode = True)

def getHTML(hfile, version=3, debug=False):
    if debug:
        print("Loading {0}".format(hfile))
    hdata = open(hfile).read()
    return hdata



###############################################################################
#
# Txt
#
###############################################################################
def saveTxt(tfile, tdata):
    f = open(tfile, "w+")
    f.write("\n".join(tdata))
    f.close()
    
def getTxt(tfile, version=3, debug=False):
    if debug:
        print("Loading {0}".format(tfile))
    tdata = open(tfile).read()
    return tdata



###############################################################################
#
# JSON
#
###############################################################################
def saveJSON(jfile, jdata):
    json.dump(jdata, open(jfile, "w"))

def getJSON(jfile, version=3, debug=False):
    if debug:
        print("Loading {0}".format(jfile))
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
    savePICKLE(filename, data, compress)
    
def savePICKLE(pfile, pdata, compress=True):
    """
    Save data using joblib
    
    Inputs:
      > pfile: the saved filename
      > pdata: anything that can be pickled
      > compress (True by default): compress the output file?
      
    Output:
      > None
    """
    joblib.dump(pdata, pfile, compress=compress)
    showSize(pfile)

def loadJoblib(filename, version=3, debug=False):
    """
    Load data using joblib
    
    Inputs:
      > filename: the saved filename
      
    Output:
      > None
    """
    return getPICKLE(filename, version)
    
def getPICKLE(pfile, version=3, debug=False):
    """
    Load data using joblib
    
    Inputs:
      > filename: the saved filename
      > debug (optional)
      
    Output:
      > None
    """
    if debug:
        print("Loading {0}".format(pfile))

    if version == 2:
        data = pickle.load(open(pfile, 'rb'), encoding='latin1')
    else:
        data = joblib.load(pfile)
    return data



###############################################################################
#
# General
#
###############################################################################
def saveFile(ifile, idata, debug=False):
    if debug:
        print("Saving data to {0}".format(ifile))
    ext = splitext(basename(ifile))[1]
    if ext == ".p":
        savePICKLE(pfile=ifile, pdata=idata)
    elif ext == ".json":
        saveJSON(jfile=ifile, jdata=idata)
    elif ext == ".yaml":
        saveYaml(yfile=ifile, ydata=idata)
    elif ext == ".txt" or ext == ".dat":
        saveTxt(yfile=ifile, ydata=idata)
    else:
        raise ValueError("Did not recognize extension format {0}".format(ext))
    if debug:
        print("Saved data to {0}".format(ifile))
        showSize(ifile)

        
        
def getFile(ifile, version=3, debug=False):
    if debug:
        print("Loading data from {0}".format(ifile))
        showSize(ifile)
    ext = splitext(basename(ifile))[1]
    if ext == ".p":
        return getPICKLE(pfile=ifile, version=version, debug=debug)
    elif ext == ".json":
        return getJSON(jfile=ifile, version=version, debug=debug)
    elif ext == ".yaml":
        return getYaml(yfile=ifile, version=version, debug=debug)
    elif ext == ".html" or ext == ".htm":
        return getHTML(hfile=ifile, version=version, debug=debug)
    elif ext == ".txt" or ext == ".dat":
        return getTxt(tfile=ifile, version=version, debug=debug)
    else:
        raise ValueError("Did not recognize extension {0}".format(ext))
