

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

