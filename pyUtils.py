
# coding: utf-8

def getKeys(dct, merge=False):
    """
    Get dictionary keys for Python3
    
    Input:
      > dct: A dictionary
      
    Output:
      > The first key, all other keys
    """
    if not isinstance(dct, (dict,list)):
        print("Argument is not a dictionary")
        return None
    
    if isinstance(dct,list):
        fKey  = dct[0]
        lKeys = dct[1:]
    else:
        allKeys = list(dct.keys())
        if merge is True:
            return allKeys
    
        if len(allKeys) > 1:
            fKey  = allKeys[0]
            lKeys = allKeys[1:]
        else:
            fKey  = allKeys[0]
            lKeys = []
    
    return fKey, lKeys


