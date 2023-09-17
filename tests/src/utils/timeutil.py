""" A simple utility class for measuring timing of processes """

__all__ = ["Now"]

from pandas import Timestamp


##############################################################################################################
# Wrapper For Currenet Time
##############################################################################################################
class Now:
    def __init__(self):
        self.round = 's'
        
    def get(self):
        return Timestamp.today().round(self.round)
    
    def show(self):
        print("Current Time Is {0}".format(self.get()))