import seaborn as sns
from matplotlib import pyplot as plt
from pandasUtils import isDataFrame, isSeries
from numpy import arange, random

try:
    from MulticoreTSNE import MulticoreTSNE as MultiTSNE
except:    
    print("Could not import MulticoreTNSE")
    
try:
    from sklearn.manifold import TSNE as SkTSNE
except:
    print("Could not import SklearnTNSE!")
    
    
def computeTSNE(Xdata, target = None, useMulti=True, num=2500, njobs=4):
    if target is not None:
        idx = random.choice(arange(len(target)), num, replace=False)
        tsneFeatures = Xdata.iloc[idx,]
        tsneTarget   = target.iloc[idx].values
    else:
        idx = random.choice(arange(Xdata.shape[0]), num, replace=False)
        tsneFeatures = Xdata.iloc[idx,]
        tsneTarget = None

    if useMulti is True:
        try:
            tsne = MultiTSNE(n_jobs=njobs)
            print("Running MultiCore TSNE with {0} jobs.".format(njobs))
        except:
            print("Tried to use MultiCore TSNE, but could not load it. Using Sklearn instead.")
            tsne = SkTSNE()
    else:
        try:
            tsne = SkTSNE()
            print("Running Sklearn TSNE.")
        except:            
            print("Tried to use Sklearn TSNE, but could not load it. Returning.")
            return None   
    
    projection = tsne.fit_transform(tsneFeatures)
    return projection, tsneFeatures, tsneTarget
    
    
    
def plotTSNE(Xdata, target = None, useMulti=True, num=2500, savename=None, njobs=4, size=4, cmap=None, dim=(12,8)):
    """ 
    Plot TSNE for training data
    
    Inputs:
      > Xdata: The training feature data (DataFrame)
      > target: The training target data (Series)
      > num (2500 by default): The number of rows to use
      
    Output: None
    """
    sns.set(style="ticks")
    
    if Xdata is None:
        print("Xdata is NONE in plotTSNE!")
        return None
    if not isDataFrame(Xdata):
        print("Xdata is not a Pandas DataFrame!")
        return None
    if target is not None:
        if not isSeries(target):
            print("target is not a Pandas Series!")
            return None

        
    print("Computing TSNE for {0} events with {1} features".format(num, Xdata.shape[1]))
    projection, tsneFeatures, tsneTarget = computeTSNE(Xdata=Xdata, target=target, useMulti=useMulti, num=num, njobs=njobs)
    print("Plotting TSNE for {0} events".format(num))

    showTSNE(projection=projection, target=target, savename=savename, title="TSNE", size=size, cmap=cmap, dim=dim)
    return projection, tsneFeatures, tsneTarget



def getCMAP(name, size):
    try:
        cmap = plt.cm.get_cmap(name, size)
    except:
        print("Could not create CMAP with name {0} and size {1}".format(name, size))
        cmap = None

    return cmap

def showTSNE(projection, target, savename, title="TSNE", size=4, cmap=None, dim=(12,8)):
    plt.figure(figsize=dim)
    
    if target is not None:
        c = target
        if cmap is None:
            cmap = getCMAP('winter', len(set(c)))
        plt.scatter(*projection.T, c=c, s=size, linewidth=0, cmap=cmap)
        plt.title(title)
        cbar= plt.colorbar()
        cbar.set_label("Target Range", labelpad=+1)
        plt.show()
    else:
        plt.scatter(*projection.T, s=size, linewidth=0)
        plt.title(title)
        plt.show()
        
    if savename is not None:
        print("Saving TSNE plot to {0}".format(savename))
        plt.savefig(savename)
        