# coding: utf-8

from numpy import concatenate, ndarray, asarray, linspace, percentile
from pandas import Series


def mergeArrays(arrays):
    """
    Merge Arrays
    
    Inputs:
      > dictionary or list of arrays
      
    Output:
      > Merged array
    """
    if isinstance(arrays, dict):
        arrays = [arr for (name,arr) in arrays.items()]
    if any([not isinstance(x,(ndarray,Series)) for x in arrays]):
        print("One of the {0} arrays is not an ndarray".format(len(arrays)))
        return None
    
    retval = concatenate(arrays)
    return retval


def createArray(lval):
    """
    Create Arrays
    
    Inputs:
      > Numerical data
      
    Output:
      > Numpy array
    """
    retval = asarray(lval)
    return retval


def getDim(array):
    """
    Get Dimension of Array
    
    Inputs:
      > Array
      
    Output:
      > Dimensions
    """
    return array.ndim


def getRows(array):
    """
    Get Number of rows of Array
    
    Inputs:
      > Array
      
    Output:
      > Number of rows
    """
    try:
        nrows = array.shape[0]
    except:
        print("Could not get shape (row) info from array with {0} dimensions.".format(getDim(array)))
        return None
    return nrows


def getCols(array):
    """
    Get Number of columns of Array
    
    Inputs:
      > Array
      
    Output:
      > Number of columns
    """
    try:
        ncols = array.shape[1]
    except:
        print("Could not get shape (col) info from array with {0} dimensions.".format(getDim(array)))
        return Non
    return nrows


def getQuantiles(array, ptiles = None, flatten = False):
    """
    Get quantiles of an array
    
    Inputs:
      > Array
      > ptiles: A list of percentiles. Use deciles if left as None
      > flatten: Should we flatten the arary(s) before getting quantiles
      
    Output:
      > Quantiles of the array
    """
    dim = getDim(array)
    if ptiles is None:
        ptiles = linspace(0, 100, 11)
    if dim == 1:
        qtiles = percentile(a=array, q=ptiles)
    elif dim == 2:
        if flatten is True:
            tmpval = mergeArrays(array)
            qtiles = percentile(a=tmpval, q=ptiles)
        else:
            qtiles = [percentile(a=x, q=ptiles) for x in array]
    else:
        print("No idea about dim > 2")
        return None
    
    return qtiles

