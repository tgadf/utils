
# coding: utf-8

from pyspark.sql.window import Window
from pyspark.sql.functions import avg, sum, udf, countDistinct, col, datediff, max, min
from pyspark.sql.types import IntegerType, BooleanType, DateType, StringType, LongType, TimestampType
from pyspark.sql import dataframe

from timeUtils import clock, elapsed, isFuture, isDate

def isSparkDF(spdf):
    if isinstance(spdf, dataframe.DataFrame):
        return True
    return False
def isSparkDataFrame(spdf):
    return isSparkDF(spdf)
    
    
def getSparkDFRows(spdf):
    try:
        nrows = spdf.count()
    except:
        print("Could not get number of rows from Spark DataFrame")
        return 0
    
    return nrows
    
    
def getSparkDFCols(spdf):
    try:
        ncols = len(spdf.dtypes())
    except:
        print("Could not get number of columns from Spark DataFrame")
        return 0
    
    return nrows


def getSparkDFDim(spdf):
    if isSparkDF(spdf):
        shape = (getSparkDFRows(spdf), getSparkDFCols(spdf))
        return shape
    return (None,None)


modFunc = lambda y: udf(lambda x: x % y == 0, 'boolean')


def castInt(spdf, colname):
    spdf = spdf.withColumn(colname, spdf[colname].cast(IntegerType()))
    return spdf

def castDouble(spdf, colname):
    spdf = spdf.withColumn(colname, spdf[colname].cast(DoubleType()))
    return spdf

def castString(spdf, colname):
    spdf = spdf.withColumn(colname, spdf[colname].cast(StringType()))
    return spdf
    
def castLong(spdf, colname):
    spdf = spdf.withColumn(colname, spdf[colname].cast(LongType()))
    return spdf
    
def castDate(spdf, colname):
    spdf = spdf.withColumn(colname, spdf[colname].cast(DateType()))
    return spdf

def castTimestamp(spdf, colname):
    spdf = spdf.withColumn(colname, spdf[colname].cast(TimestampType()))
    return spdf




def getPandasDataFrame(spdf):
    start = clock(comment="Creating Pandas DataFrame from Spark DataFrame")
    pddf = spdf.toPandas()
    elapsed(start, comment="Create Pandas DataFrame")
    return pddf


def fillNAWithZero(spdf):
    spdf.na.fill(0)
    
    
def setupHive(sc):
    from pyspark.sql import HiveContext
    hc = HiveContext(sc)
    return hc
    
    
def setupSQL(sc):
    from pyspark.sql import SQLContext
    sqlc = SQLContext(sc)
    return sqlc


def commonSparkAddOns(sc, debug=False):
    if debug is True:
        print("  Adding common files to SparkContent")
    try:
        sc.addFile("timeUtils.py")
        sc.addFile("modelio.py")
        sc.addFile("network.py")
        sc.addFile("driverNetwork.py")
        sc.addFile("networkFeatures.py")
        sc.addFile("networkTrips.py")
        
        sc.addFile("vertexData.py")
        sc.addFile("edgeData.py")
        sc.addFile("networkCategories.py")

        sc.addFile("geoClustering.py")
        sc.addFile("poi-7.p")
        sc.addFile("geoCBSA-5.p")
        sc.addFile("geoCSA-5.p")
        sc.addFile("geoPlace-5.p")
        sc.addFile("geoState-5.p")
        sc.addFile("geoZCTA-5.p")
        sc.addFile("georec-7-Road.p")
        sc.addFile("georec-7-loc.p")
        
        #sc.addFile("geoCD111-5.p")
        #sc.addFile("geoELSD-5.p")
        #sc.addFile("geoSCSD-5.p")
        #sc.addFile("geoSubMCD-5.p")
        sc.addFile("geoCounty-5.p")
        #sc.addFile("geomap-fix-5.p")
        #sc.addFile("geoSLDL-5.p")
        sc.addFile("geoTract-5.p")
        #sc.addFile("geoCouSub-5.p")
        sc.addFile("geoMetDiv-5.p")
        #sc.addFile("geoSLDU-5.p")
        #sc.addFile("geoUNSD-5.p")
        sc.addFile("countyData.p")
        sc.addFile("tractData.p")
        sc.addFile("blkgrpData.p")
        sc.addFile("countyData.p")
        sc.addFile("pandasUtils.py")
        sc.addFile("pyUtils.py")
        sc.addFile("pygeohash.py")
        sc.addFile("sparkUtils.py")
    except:
        raise ValueError("  Could not add all common files to SparkContent!!!")
    if debug is True:
        print("  All common files added to SparkContent")
        
    
def setupSpark(debug=False):
    start, cmt = clock("Setting up Spark/PySpark")
    
    import os
    try:
        sparkhome=os.environ.get("SPARK_HOME")
        print("PySpark home is {0}".format(sparkhome))
    except:
        raise ValueError("There is not SPARK_HOME variable")
    
    try:
        import findspark
        findspark.init(sparkhome)
    except:
        raise ValueError("Could import findspark")
        
    try:
        import pyspark    
    except:
        raise ValueError("Could not import pyspark")
    
    hivejar = '/opt/cloudera/parcels/CDH/jars/hive-hcatalog-core-1.1.0-cdh5.13.3.jar'
    from os.path import exists
    if not exists(hivejar):
        raise ValueError("Hive JAR {0} does not exist".format(hivejar))
    
    conf = (pyspark.SparkConf()
        .setAppName('Daily Feature Generator')
        .setMaster('yarn')
        .set('spark.driver.memory', '20g')
        .set('spark.shuffle.service.enabled', True)
        .set('spark.dynamicAllocation.enabled', True)
#        .set('spark.executor.heartbeatInterval', '3600s')
        .set('spark.executor.memory', '5g')
        .set('spark.yarn.executor.memoryOverhead', '4000m')
        .set('spark.dynamicAllocation.maxExecutors', 250)
        .set('spark.dynamicAllocation.minExecutors', 10)
        .set('spark.kryoserializer.buffer.max', '1g')
        .set('spark.speculation', True)
        .set('spark.jars', hivejar)
        .set('spark.port.maxRetries', 100)
        .set('spark.driver.maxResultSize', '6g')
        .set('spark.sql.broadcastTimeout', 600))

    sc = pyspark.SparkContext(conf = conf)
    sc.setLogLevel('ERROR')
    
    elapsed(start, cmt)
    
    return sc


def checkForDuplicatesInSparkDataFrame(hc, keys, db, table):
    args = ", ".join(keys)
    args = args.replace('date', '`date`')

    retval = hc.sql("""select {0}, count(*)
                       from {1}.{2}
                       group by {0}
                       having count(*) > 1""".format(args, db, table))
    retval.show()
    return retval
    

def getHiveData(hc, dbName, tableName, startDate=None, endDate=None, sql=None, cache=True):
    '''
    getHiveData: Retreive data from a Hive Table
    
    Inputs:
        > hc (HiveContext object)
        > dbName (string): Database name
        > tableName (string): Table name
        > startDate (string, optional): A lower bound on the date
        > endDate (string, optional): A upper bound on the date
        > cache (boolean, True by default): Cache the result
        
    Output:
        > pyspark dataframe
    '''
    from pyspark.sql.context import HiveContext
    if not isinstance(hc, HiveContext):
        print("The first argument 'hc' must be a HiveContext object")
        return None
    
    if sql is not None:
        sqlcmd = sql
    else:
        if isDate(startDate) and isDate(endDate):
            if isFuture(endDate):
                sqlcmd = "SELECT * FROM {0}.{1} WHERE date >= '{2}'".format(dbName, tableName, startDate)
            else:
                sqlcmd = "SELECT * FROM {0}.{1} WHERE date between '{2}' and '{3}'".format(dbName, tableName, startDate, endDate)
        else:
            sqlcmd = "SELECT * FROM {0}.{1}".format(dbName, tableName)


    print("Running this SQL Command: {0}".format(sqlcmd))
    try:
        sql_data = hc.sql(sqlcmd)
        print("Command is valid")
    except:
        print("Could not execute the SQL Query!")
        return None
        
    if cache is True:        
        print("Caching Result")
        sql_data.cache()
        
    print("Returning pyspark dataframe")
    return sql_data