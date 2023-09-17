""" API/Web Utils """

__all__ = ["sleep", "wait"]

from tqdm import tqdm
from tqdm.notebook import tqdm_notebook
import time

def sleep(value):
    time.sleep(value)
    
def wait(value, inc=10, desc="Waiting"):
    try:
        inc  = min([inc,10])
        incs = int(value*inc)        
    except:
        raise TypeError("Could not convert [{0}]*[{1}] into Integer".format(value, inc))
    for i in tqdm_notebook(range(incs), desc = desc):
        time.sleep(1.0/inc)