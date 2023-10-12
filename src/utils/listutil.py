""" Common List-based Utility Functions """

__all__ = ["getFlatList", "flattenLists", "assertType"]

from collections import Counter


def least_common(array, to_find=None):
    """
    >>> least_common_values([1,1,2,2,2,2,3,3,3,3,3,3,3,4,4,4,4,4,4,4], 2)
    [(1, 2), (2, 4)]
    """
    counts = Counter(array) if isinstance(array, list) else array
    if isinstance(to_find, int):
        return list(reversed(counts.most_common()[-to_find:]))
    else:
        return list(reversed(counts.most_common()))
    

def getFlatList(listval):
    """
    Flatten two-tier list
    """
    
    # assert isinstance(listval, list), f"getFlatList arg [{type(listval)}] is not a list"
    flat_list = [item for sublist in listval for item in sublist]
    return flat_list


def flattenLists(values, rmNa=True, unique=False):
    if len(values) == 0:
        return []
    group = []
    for value in values:
        try:
            group += [item for item in value if item is not None] if rmNa is True else [item for item in value]
        except Exception as error:
            continue
    retval = list(set(group)) if unique is True else group
    return retval


def isIn(values, listval):
    if not isinstance(listval, list):
        listval = [listval]
    if not isinstance(values, list):
        values = [values]
    known = False
    for val in values:
        for lval in listval:
            if lval.find(val) != -1:
                known = True
    return known


def getIndex(listval, val):
    try:
        idx = listval.index(val)
    except Exception as error:
        idx = None
        
    return idx


def assertType(listval: list, dtype) -> 'bool':
    """
    Test that all list values are type [dtype]
    """
    
    # assert isinstance(listval, (list), f"getFlatList arg [{type(listval)}] is not a list"
    retval = all([isinstance(item, dtype) for item in listval])
    return retval
    
    