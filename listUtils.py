def getFlatList(listval):
    flat_list = [item for sublist in listval for item in sublist]
    return flat_list


def getIndex(listval, val):
    try:
        idx = listval.index(val)
    except:
        idx = None
        
    return idx