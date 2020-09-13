def getFlatList(listval):
    flat_list = [item for sublist in listval for item in sublist]
    return flat_list

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
    except:
        idx = None
        
    return idx