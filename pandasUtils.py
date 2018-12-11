
# coding: utf-8

from numpy import ndarray, reshape, random, repeat, linspace, percentile, arange, std, append, logical_and, int64, float64
from pandas import DataFrame, Series, read_csv, Timestamp, offsets, to_datetime
from pandas.core.indexes import datetimes
from pyUtils import getKeys



def isSeries(data):
    return isinstance(data, Series)

def isDataFrame(data):
    return isinstance(data, DataFrame)
    

def cutSeries(data, minval = None, maxval = None, cutoff = None):
    """
    Cut a Series
    
    Inputs:
      > data: The series
      > minval (optional): a min value
      > maxval (optional): a max value
      > cutoff (optional): a quantile cutoff
      
    Output:
      > The cut series
    """
    if isinstance(data, Series):
        retval = data.copy()
        if cutoff is not None:
            cutvals = percentile(retval, q=[100*cutoff, 100*(1-cutoff)])
            minval  = cutvals[0]
            maxval  = cutvals[1]    
        retval = retval[retval >= minval]
        retval = retval[retval <= maxval]
        return retval
    else:
        return data
    
    
def getFrequency(data):
    if isSeries(data):
        return data.value_counts()
    return None
    
    
def createSeries(data, index=None, name=None):
    """
    Create a Series from other data
    
    Inputs:
      > data: The series
      > index (optional): data for the index
      > name (optional): data for the name
      
    Output:
      > The Series
    """
    if isinstance(data, DataFrame):
        if index is None:
            index = data.index
        if name is None:
            name = data.columns[0]
    if isinstance(data, ndarray):
        if index is None:
            index = range(len(data))
        if name is None:
            name = "myseries"
    colData = data.values.ravel()
    retval = Series(colData, index=index, name=name)
    return retval                    
    
    
def getColData(data, colnums = None, colnames = None, copy=False):
    """
    Get data from a DataFrame column(s)
    
    Inputs:
      > data: The DataFrame
      > colnums: The number(s) of the column(s)
      > colnames: The name(s) of the column(s)
      > copy (False by default): should we copy the data?
      
    Output:
      > DataFrame of the specified column data
    """
    if colnums is not None:
        if copy is True:
            subdata = data.iloc[:,colnums].copy()
        else:
            subdata = data.iloc[:,colnums]
    elif colnames is not None:
        if copy is True:
            subdata = data[colnames].copy()
        else:
            subdata = data[colnames]         
    else:
        print("Not doing anything with the data in getColData")
        return data
    return subdata
    
    
def getRowData(data, rownums = None, rownames = None, copy=False):
    """
    Get data from a DataFrame row(s)
    
    Inputs:
      > data: The DataFrame
      > rownums: The number(s) of the row(s)
      > rownames: The name(s) of the row(s)
      > copy (False by default): should we copy the data?
      
    Output:
      > DataFrame of the specified row data
    """
    if rownums is not None:
        subdata = data.iloc[rownums,]
    elif rownames is not None:
        subdata = data.loc[rownames]
    else:
        print("Not doing anything with the data in getRowData()")
        return data
    
    if copy is True:
        subdata = subdata.copy()
    return subdata


def getRows(data, colname, colvalue):
    try:
        retval = data.loc[data[colname] == colvalue]
    except:
        print("Could not select column {0} value of {1}".format(colname, colvalue))
        return data
    return retval


def mergeSeries(sdata, resetIdx=False):
    """
    Merge Series
    
    Inputs:
      > sdata: Either a list of dictionary of Series data
      > resetIdx (False by default): should we reset the indices?
      
    Output:
      > The merged Series
    """
    if isinstance(sdata, list):
        retval = concat(sdata)
        return retval
    
    if isinstance(sdata, dict):
        retval = concat(sdata.values)
        return retval

    return None
    
    fKey,lKeys = getKeys(sdata)
    if isinstance(fKey, Series):
        initSeries = fKey
        retval = initSeries.append(lKeys)
    else:
        initSeries = sdata[fKey]
        mSeries    = [sdata[x] for k in lKeys]
        retval = initSeries.append(mSeries)
        
    return retval


def cutDataFrameByDate(data, mindate = None, maxdate = None, copy = False):
    """
    Cut a DataFrame by date
    
    Inputs:
      > data: DataFrame
      > mindate (None by default): A start date
      > maxdate (None by default): An end date
      > copy (False by default): returna a copy of the data
      
    Output:
      > The cut date frame
    """
    if not isinstance(data, DataFrame):
        print("Input is not a DataFrame")
        return data

    if not isinstance(data.index, datetimes.DatetimeIndex):
        print("DataFrame index is not a DateTimeIndex")
        return data
    
    keep = repeat(True, len(data.index))
    if mindate is not None:
        keep = logical_and(data.index >= mindate, keep)
    if maxdate is not None:
        keep = logical_and(data.index <= maxdate, keep)
    
    if all(keep):
        return data
    
    subdata = data[keep]
    if copy is True:
        subdata = subdata.copy()
    return subdata



def getRandomDate(start, end, position=None):
    start, end = Timestamp(start), Timestamp(end)
    delta = (end - start).total_seconds()
    if position is None:
        offset = random.uniform(0., delta)
    else:
        offset = position * delta
    offset = offsets.Second(offset)
    t = start + offset
    return t



def dropColumns(pddata, columns, inplace=True):
    if inplace is True:
        pddata.drop(columns, axis=1, inplace=True)
    else:
        return pddata.drop(columns, axis=1, inplace=False)
    

def fillNAWithZero(pddata, inplace=True):
    if inplace is True:
        pddata.fillna(0, inplace=True)
    else:
        return pddata.fillna(0, inplace=False)
    
    
def castDateTime(coldata):
    return to_datetime(coldata)

def castInt64(coldata):
    return coldata.astype(int, errors='ignore')

def castFloat64(coldata):
    return coldata.astype(float)

def castStr(coldata):
    return coldata.astype(str)

def convertToDate(coldata):
    try:
        return coldata.dt.date
    except:
        return coldata
    
    
########################################################################################################
# Fix Type when saving data frame
########################################################################################################
def fixType(value):
    import numpy as np
    if isinstance(value, tuple):
        value = str(value)
    elif isinstance(value, int64):
        value = int(value)
    elif isinstance(value, float64):
        value = float(value)
    elif isinstance(value, str):
        value = str(value)
    elif isinstance(value, float):
        value = float(value)
    elif isinstance(value, int):
        value = int(value)
    elif isinstance(value, type(None)):
        value = None
    elif isinstance(value, list):
        value = str(value)
    else:
        raise ValueError("Unknown Type: {0} --> {1}".format(type(value), value))
    return value
