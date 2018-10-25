
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType, DoubleType, FloatType

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

prec=""
get_geo3_udf = udf(lambda lat,long: getGeo3(lat, long), StringType())
get_geo4_udf = udf(lambda lat,long: getGeo4(lat, long), StringType())
get_geo5_udf = udf(lambda lat,long: getGeo5(lat, long), StringType())
get_geo6_udf = udf(lambda lat,long: getGeo6(lat, long), StringType())
get_geo7_udf = udf(lambda lat,long: getGeo7(lat, long), StringType())
get_geo8_udf = udf(lambda lat,long: getGeo8(lat, long), StringType())

_, _ = clock("Last Run")