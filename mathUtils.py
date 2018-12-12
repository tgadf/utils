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