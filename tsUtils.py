from numpy import logical_or, logical_not, logical_and, repeat

def getHolidays():
    holidays = [['2017-01-01', '2017-01-02'],
            ['2017-04-14', '2017-04-17'],
            ['2017-05-26', '2017-05-29'],
            ['2017-09-01', '2017-09-04'],
            ['2017-06-29', '2017-07-04'],
            ['2017-11-21', '2017-11-26'],
            ['2017-12-23', '2018-01-02']]
    return holidays

    
def getBreaks():
    breaks = [['2017-02-20', '2017-03-20'],['2017-10-04', '2017-10-13']]
    return breaks



def cutHolidayDates(featdata, extra):
    holidays = getHolidays()
    breaks   = getBreaks()

    keep = repeat(False, featdata.shape[0])
    for i in range(len(holidays)):
        begin = holidays[i][0]
        end   = holidays[i][1]
        keep = logical_or(logical_and(featdata['date'] >= begin, featdata['date'] <= end), keep)
    
    if extra == "noholiday":
        keep = logical_not(keep)
        featdata = featdata[keep]
        
    if extra == "holiday":
        featdata = featdata[keep]

    return featdata