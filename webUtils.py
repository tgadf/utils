# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 17:43:30 2017

@author: tgadfort
"""

from urllib.request import urlopen, pathname2url
from urllib.parse import urljoin
#from urllib import pathname2url
from os.path import getsize
from os import remove
from ioUtils import saveJoblib, getFile
from fsUtils import isFile
import subprocess
from bs4 import BeautifulSoup, element



            

################################################################################
#
# Download Web Data
#
################################################################################
def makeURL(baseURL, extraURL):
    url = urljoin(baseURL, extraRef)
    return url


def getURL(url, savename, debug = False):
    if debug:
        print("Downloading {0}".format(url))
    content = urlopen(url).read()
    saveJoblib(content, savename)
    #pickle.dump(content, open(savename, "w"))
    size = round(getsize(savename)/1e3)
    if size < 1:
        if debug:
            print("There is likely a problem with",savename)
        return False
    print(savename,'size ->',size,"kB")
    return True    



def asrun(ascript):
    "Run the given AppleScript and return the standard output and error."
    osa = subprocess.Popen(['osascript', '-'],
                           stdin=subprocess.PIPE,
                           stdout=subprocess.PIPE)

    return osa.communicate(ascript)[0]



def getSafariURL(url, savename, dtime = 5, debug = False):
    dscript =  '''
    tell application "Safari"
    activate
    set URL of document 1 to "{0}"
    delay {1}
    set myString to source of document 1
    end tell
    '''.format(url, dtime).encode()
    
    if False:
        dscript = '''
        tell application "Safari"
        activate
        set URL of document 1 to "{0}"
        delay {2}
        set myString to source of document 1
        end tell
        set newFile to POSIX file "{1}"
        open for access newFile with write permission
        write myString to newFile
        close access newFile
        '''.format(url, savename, dtime)

    content = asrun(dscript)    
    saveJoblib(content, savename)
    size = round(getsize(savename)/1e3)
    if size < 1:
        if debug:
            print("There is likely a problem with",savename)
        return False
    print(savename,'size ->',size,"kB")
    return True    

    
def getWebData(base = None, suburl = None, extra = None, savename = None, dtime = 5, useSafari = True, debug = False):
    if debug and False:
        print("Base  :",base,'\t',type(base))
        print("Artist:",suburl,'\t',type(suburl))
        if extra:
            print("Extra :",extra,'\t',type(extra))


    if base == None:
        print("Need a base url")
        return
        
    if savename == None:
        print("Need a savename")
        return

    if suburl:
        url = base + pathname2url(suburl.encode("utf-8"))
    else:
        url = base
        
    if extra:
        url += extra

    if useSafari:
        retval = getSafariURL(url, savename, dtime, debug)
    else:
        retval = getURL(url, savename, debug)
    
    return retval
    

def checkFileSize(ifile, minSize = 1000):
    if getsize(ifile) < minSize:
        print(" --> Removing due to low size:",ifile)
        remove(ifile)
    




################################################################################
#
# Download Web Data
#
################################################################################
def getHTML(htmldata, allowError = False, debug = False):
    if isFile(htmldata):
        try:
            htmldata = getFile(htmldata)
        except:
            raise ValueError("Could not read from",htmldata)

    try:
        bsdata = BeautifulSoup(htmldata, "lxml")
    except:
        if allowError:
            return None
        else:
            raise ValueError("Could not parse html data!")

    return bsdata


def isBS4(bsdata, debug = False):
    if bsdata:
        return isinstance(bsdata, BeautifulSoup)
    return False


def isBS4Tag(bsdata, debug = False):
    if bsdata:
        return isinstance(bsdata, element.Tag)
    return False


### BeautifulSoup functions
def removeTag(line, tag, debug = False):
    if not isBS4(line) and not isBS4Tag(line):
        try:
            line = BeautifulSoup(line)
        except:
            raise ValueError("Could not create BS data from",line)
    
    if debug:
        print("Removing <"+tag+">from line: "+line)
    
    tagVals = line.findAll(tag)
    for tagVal in tagVals:
        tagVal.extract()
        
    return line