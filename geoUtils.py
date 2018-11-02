from pyspark.sql.functions import udf
from pyspark.sql.types import StringType, DoubleType, FloatType
from numpy import pi, cos


def getGeo3(lat, long):
    try:
        retval = geohash.encode(lat, long, precision=3)
    except:
        retval = None
    return retval

def getGeo4(lat, long):
    try:
        retval = geohash.encode(lat, long, precision=4)
    except:
        retval = None
    return retval

def getGeo5(lat, long):
    try:
        retval = geohash.encode(lat, long, precision=5)
    except:
        retval = None
    return retval

def getGeo6(lat, long):
    try:
        retval = geohash.encode(lat, long, precision=6)
    except:
        retval = None
    return retval

def getGeo7(lat, long):
    try:
        retval = geohash.encode(lat, long, precision=7)
    except:
        retval = None
    return retval

def getGeo8(lat, long):
    try:
        retval = geohash.encode(lat, long, precision=8)
    except:
        retval = None
    return retval


def convertMetersToLat(dist, debug=False):
    # Earth's radius, sphere
    R=6378137

    # Distances
    dn = dist

    # Coordinate offsets in radians
    dLat = dn/R
    
    # OffsetPosition, decimal degrees
    lat = dLat * 180/pi
    
    return lat


def convertLatToMeters(ang, debug=False):
    # Earth's radius, sphere
    R=6378137
    
    # convert decimal to radians
    dLat = ang * pi/180
    
    # scale to Earth's radius
    dist = dLat * R
    
    return dist


def convertMetersToLong(dist, lat, debug=False):
    # Earth's radius, sphere
    R=6378137

    # Distances
    de = dist

    # Coordinate offsets in radians
    dLon = de/(R*cos(pi*lat/180))
    
    # OffsetPosition, decimal degrees
    lng = dLon * 180/pi
    
    return lng


def convertLongToMeters(ang, lat, debug=False):
    # Earth's radius, sphere
    R=6378137
    
    # convert decimal to radians
    dLon = ang * pi/180
    dLat = lat * pi/180
    
    # scale to Earth's radius with known latitude
    dist = dLon * (R*cos(dLat))
    
    return dist

prec=""
get_geo3_udf = udf(lambda lat,long: getGeo3(lat, long), StringType())
get_geo4_udf = udf(lambda lat,long: getGeo4(lat, long), StringType())
get_geo5_udf = udf(lambda lat,long: getGeo5(lat, long), StringType())
get_geo6_udf = udf(lambda lat,long: getGeo6(lat, long), StringType())
get_geo7_udf = udf(lambda lat,long: getGeo7(lat, long), StringType())
get_geo8_udf = udf(lambda lat,long: getGeo8(lat, long), StringType())

_, _ = clock("Last Run")