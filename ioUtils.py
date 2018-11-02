# coding: utf-8

from sklearn.externals import joblib
from os.path import getsize, exists, join, dirname, basename
from os import listdir
from sklearn.model_selection import train_test_split
from glob import glob, glob1
from numpy import ndarray, reshape
from pandas import DataFrame, Series, read_csv

from timeUtils import clock, elapsed
from pandasUtils import dropColumns


##########################################################################################
#
# Generic file io functions
#
##########################################################################################
def showSize(filename):
    """
    Show file size
    
    Inputs: filename
    Outputs: None
    """
    fsize = getsize(filename)
    units = "B"
    if fsize > 1e6:
        fsize /= 1e6
        units = "MB"
    elif fsize > 1e3:
        fsize /= 1e3
        units = "kB"
    print("  --> This file is {0}{1}.".format(round(fsize,1), units))

    
def saveJoblib(data, filename, compress=True):
    """
    Save data using joblib
    
    Inputs:
      > data: anything that can be pickled
      > filename: the saved filename
      > compress (True by default): compress the output file?
      
    Output:
      > None
    """
    joblib.dump(data, filename, compress=compress)
    showSize(filename)

    
def loadJoblib(filename):
    """
    Load data using joblib
    
    Inputs:
      > filename: the saved filename
      
    Output:
      > None
    """
    data = joblib.load(filename)
    return data



##########################################################################################
#
# Model Prediction IO Functions
#
##########################################################################################
def predictDataFilename(name, outdir, dataSuffix, timeSuffix, extra = None):
    """
    The filename convention for the model prediction data
    
    Inputs:
      > name: model name
      > outdir: the output directory
      > dataSuffix: a flag specifying the original data
      > timeSuffix: a flag specifying when the predictions were made
      > extra (optional): any additional string to specify the model/data
      
    Output:
      > The filename of the prediction file
    """
    ext=[name, "predict", dataSuffix, timeSuffix]
    if extra:
        ext.append(extra)
        
    filename = join(outdir, ".".join(["-".join(ext), "p"]))
    return filename


def loadPredictData(name, outdir, dataSuffix, timeSuffix, extra = None):
    """
    Load the model prediction data
    
    Inputs:
      > name: model name
      > outdir: the output directory
      > dataSuffix: a flag specifying the original data
      > timeSuffix: a flag specifying when the predictions were made
      > extra (optional): any additional string to specify the model/data
      
    Output:
      > The predicted data (dictionary)
    """
    filename = predictDataFilename(name, outdir, dataSuffix, timeSuffix, extra)
    if not exists(filename):
        print("{0} does not exist!".format(filename))
        return None
    print("Loading {0}".format(filename))
    data = loadJoblib(filename)
    return data

def savePredictData(data, name, outdir, dataSuffix, timeSuffix, extra = None):
    """
    Save the model prediction data
    
    Inputs:
      > data: The predicted data (dictionary)
      > name: data name
      > outdir: the output directory
      > dataSuffix: a flag specifying the original data
      > timeSuffix: a flag specifying when the model was created
      > extra (optional): any additional string to specify the model/data
      
    Output:
      > None
    """
    filename = predictDataFilename(name, outdir, dataSuffix, timeSuffix, extra)
    print("Saving {0} predict data to {1}".format(name, filename))
    saveJoblib(data, filename)



##########################################################################################
#
# Model Estimator IO Functions
#
##########################################################################################   
def modelFilename(name, outdir, dataSuffix, timeSuffix, extra = None):
    """
    The filename convention for the scikit-learn model
    
    Inputs:
      > name: model name
      > outdir: the output directory
      > dataSuffix: a flag specifying the original data
      > timeSuffix: a flag specifying when the predictions were made
      > extra (optional): any additional string to specify the model/data
      
    Output:
      > The filename of the scikit-learn model file
    """
    ext=[name, dataSuffix, timeSuffix]
    if extra:
        ext.append(extra)
        
    filename = join(outdir, ".".join(["-".join(ext), "p"]))
    return filename


def loadModel(name, outdir, dataSuffix, timeSuffix, extra = None):
    """
    Load the scikit-learn model 
    
    Inputs:
      > name: model name
      > outdir: the output directory
      > dataSuffix: a flag specifying the original data
      > timeSuffix: a flag specifying when the model was created
      > extra (optional): any additional string to specify the model/data
      
    Output:
      > The scikit-learn model
    """
    filename = modelFilename(name, outdir, dataSuffix, timeSuffix, extra)        
    if not exists(filename):
        print("{0} does not exist!".format(filename))
        return None
    print("Loading {0}".format(filename))
    estimator = loadJoblib(filename)
    return estimator


def saveModel(estimator, name, outdir, dataSuffix, timeSuffix, extra = None):
    """
    Save the scikit-learn model
    
    Inputs:
      > estimator: The scikit-learn model
      > name: data name
      > outdir: the output directory
      > dataSuffix: a flag specifying the original data
      > timeSuffix: a flag specifying when the model was created
      > extra (optional): any additional string to specify the model/data
      
    Output:
      > None
    """
    filename = modelFilename(name, outdir, dataSuffix, timeSuffix, extra)
    print("Saving {0} model to {1}".format(name, filename))
    saveJoblib(estimator, filename)



##########################################################################################
#
# Model Estimator IO Functions
#
##########################################################################################   
def dataFilename(name, outdir, dataSuffix, extra = None):
    """
    The filename convention for the model data
    
    Inputs:
      > name: model name
      > outdir: the output directory
      > dataSuffix: a flag specifying the original data
      > extra (optional): any additional string to specify the model/data
      
    Output:
      > The filename of the model data filename
    """
    ext = [name, dataSuffix]    
    if extra:
        ext.append(extra)
        
    filename = join(outdir, ".".join(["-".join(ext), "p"]))
    return filename

def loadData(name, outdir, dataSuffix, extra = None):
    """
    Load the data used for modeling
    
    Inputs:
      > name: data name
      > outdir: the output directory
      > dataSuffix: a flag specifying the original data
      > extra (optional): any additional string to specify the model/data
      
    Output:
      > The modeling data (DataFrame)
    """
    filename = dataFilename(name, outdir, dataSuffix, extra)
    if not exists(filename):
        print("Could not find {0}.".format(filename))
        similar = findPattern(outdir, pattern=name, debug=False)
        print("Similar files are: {0}".format(similar))
        return None
    print("Loading {0}".format(filename))
    pdd = loadJoblib(filename)
    return pdd


def saveData(pdd, name, outdir, dataSuffix, extra = None):
    """
    Save the data used for modeling
    
    Inputs:
      > pdd: The modeling data (DataFrame)
      > name: data name
      > outdir: the output directory
      > dataSuffix: a flag specifying the original data
      > extra (optional): any additional string to specify the model/data
      
    Output:
      > None
    """
    filename = dataFilename(name, outdir, dataSuffix, extra)
    print("Saving {0} data to {1}".format(name, filename))
    saveJoblib(pdd, filename)
    
    
    
##########################################################################################
#
# Spark Data Helpers
#
##########################################################################################   
def saveSparkData(spdf, dbname, tablename):
    start, cmt = clock("Saving spark dataframe to {0}.{1}".format(dbname, tablename))
    spdf.write.mode('overwrite').format('parquet').saveAsTable("{0}.{1}".format(dbname, tablename))
    elapsed(start, cmt)
    
def appendSparkData(spdf, dbname, tablename):
    start, cmt = clock("Appending spark dataframe to {0}.{1}".format(dbname, tablename))
    spdf.write.mode('append').format('parquet').saveAsTable("{0}.{1}".format(dbname, tablename))
    elapsed(start, cmt)
        
    
    
##########################################################################################
#
# Data Helpers
#
##########################################################################################   
def LoadOriginalData(pattern='1_nogps', dataSuffix='20180228', ext='csv', fillna=True, dropcols=True, savedata=True, extra=None):
    """
    Load the Anne's .csv files to a data frame and clean them up
    
    Inputs:
      > pattern: unique string pattern for the files you want
      > dataSuffix: a flag specifying the original data
      > ext (csv by default): The file extensions
      > fillna (True by default): should we set all NA values to 0
      > dropcols (True by default): should we drop the keyed columns
      > savedata (True by default): should we save the data? if false, then return the DataFrame
      > extra (optional): any additional string to specify the model/data
      
    Output:
      > The scikit-learn model
    """
    basedir = '/home/tgadf/astro_research_data/pol_futuremiles_xgboost/train_test_files'
    files = findPatternExt(basedir, pattern="_".join([pattern,dataSuffix]), ext=ext, debug=False)
    trainData = None
    for i,ifile in enumerate(files):
        print("Loading {0}/{1}: {2}".format(i,len(files),ifile), end='    ')
        if trainData is None:
            trainData = read_csv(ifile)
        else:
            trainData = trainData.append(read_csv(ifile))
        print(trainData.shape)

    try:
        if dropcols is True:
            trainDataKeys = trainData[['dev_imei', 'date']].copy()
            drops = ['dev_imei', 'date', 'this_date_min_1hr_segment', 'Unnamed: 0']
            print("  Dropping {0}".format(drops))
            dropColumns(trainData, drops)
        if fillna is True:
            print("  Filling NA with 0")
            trainData.fillna(0, inplace=True)
    except:
        print("Could not drop the usual columns")

    if savedata is True:
        outdatadir = '/home/tgadf/astro_research_data/futuremiles'
        saveData(trainData, name="data", outdir=outdatadir, dataSuffix=dataSuffix, extra=extra)
        return None
    
    return trainData


def splitFeaturesTarget(trainData, targetname):
    """
    Split the data into features and target
    
    Inputs:
      > trainData: the model data (DataFrame)
      > targetname: the target column name
      
    Outputs:
      > feature DataFrame and target Series
    """
    target = trainData[targetname].copy()
    dropColumns(trainData, targetname)
    return trainData, target

def splitData(features, target, trainFraction=0.25):
    """
    Split the data into test and train data
    
    Inputs:
      > features: the model feature data (DataFrame)
      > target: the target data (Series)
      > trainFraction (0.25 by default): fraction of events to use for training
      
    Outputs:
      > Training feature data (DataFrame), Testing feature data (DataFrame), Training target data (Series), Testing target data (Series)
    """
    X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=1-trainFraction, random_state=42)
    return X_train, X_test, y_train, y_test

def splitDataByKey(pddata, key, targetcol, trainFraction=0.25):
    """
    Split the data into test and train data
    
    Inputs:
      > pddata: the model feature data (DataFrame)
      > key: a key to split the train/test data on
      > targetcol: the name of the target column
      > trainFraction (0.25 by default): fraction of events to use for training
      
    Outputs:
      > Training feature data (DataFrame), Testing feature data (DataFrame), Training target data (Series), Testing target data (Series)
    """
    keydata = [str(x) for x in list(pddata[key].unique())]
    print("There are {0} unique keys.".format(len(keydata)))
    print("Using {0} training fraction.".format(trainFraction))
    from random import sample
    from numpy import asarray
    trainKeys = list(sample(keydata, int(trainFraction*len(keydata))))
    testKeys = [e for e in keydata if e not in trainKeys]
    
    if len(set(trainKeys).intersection(testKeys)) > 0:
        print("There are common keys in train/test!!")
        return None
    
    trainKeys = asarray(trainKeys)
    testKeys  = asarray(testKeys)
    print("There are {0} keys in the training data.".format(trainKeys.shape[0]))
    print("There are {0} keys in the testing data.".format(testKeys.shape[0]))
        
    trainData = pddata[pddata[key].isin(trainKeys)].copy()
    testData  = pddata[pddata[key].isin(testKeys)].copy()
    
    X_train, y_train = splitFeaturesTarget(trainData, targetcol)
    X_test, y_test   = splitFeaturesTarget(testData, targetcol)
    print("Train data has size {0} with target size {1}.".format(X_train.shape, y_train.shape))
    print("Test data has size {0} with target size {1}.".format(X_test.shape, y_test.shape))

    dropColumns(trainData, key)
    dropColumns(testData, key)
    
    return X_train, X_test, y_train, y_test


def getBasename(name):
    bname = basename(name)
    return bname

def getDirname(name):
    dname = dirname(name)
    return dname


def findPattern(basedir, pattern, debug = False):
    if basedir == None: return []
    files = [x for x in listdir(basedir) if x.find(pattern) != -1]
    files = glob(join(basedir, "*"+pattern+"*"))
    return files
     
def findPatternExt(basedir, pattern, ext, debug = False):
    if basedir == None: return []
    files = findExt(basedir, ext)
    files = [x for x in files if x.find(pattern) != -1]
    return files 
    
def findExt(basedir, ext, debug = False):
    if basedir == None: return []
    if isinstance(ext, list):
        files = []
        for exten in ext:
            files += [join(basedir,x) for x in glob1(basedir, "*"+exten)]
    else:
        files = [join(basedir,x) for x in glob1(basedir, "*"+ext)]
    return files