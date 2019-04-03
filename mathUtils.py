def doCirclesIntersect(com1, rad1, com2, rad2):
    x1 = com1[0]
    y1 = com1[1]
    
    x2 = com2[0]
    y2 = com2[1]
    
    r1 = rad1
    r2 = rad2
   
    distSq = (x1 - x2) * (x1 - x2) + (y1 - y2) * (y1 - y2);  
    radSumSq = (r1 + r2) * (r1 + r2);  
    if (distSq == radSumSq):
        return True
    elif (distSq > radSumSq): 
        return False
    else: 
        return True
    
    
def siground(x, sig=3):
    if not isinstance(x, (float, int)):
        print("Must pass a real number. You passed a {0}".format(type(x)))
        return None
    
    retval = '%s' % float('%.{0}g'.format(sig) % x)
    
    try:
        result = float(retval)
    except:
        print("Could not turn [{0}] into a float.".format(retval))
        result = None
    
    return result