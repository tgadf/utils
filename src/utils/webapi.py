""" API I/O Utils """

__all__ = ["APIIO"]

import requests
from .webutil import sleep, wait


class APIIO:
    def __repr__(self):
        return f"APIIO({self.name})"
    
    def __init__(self, name, **kwargs):
        self.verbose = kwargs.get('verbose', False)
        self.name = name
        self.code = None
        self.url = None
        self.response = None
        self.sleep = sleep
        self.wait = wait
        self.timeout = kwargs.get('timeout', 30)
        assert isinstance(self.timeout, (int, float)), "APIIO timeout arg is not an int or float"
        
    def test(self, url, **kwargs):
        response = requests.get(url, **kwargs)
        return response
    
    def get(self, url, headers=None):
        self.url = url
        if headers is not None:
            try:
                self.response = requests.get(url, headers=headers, timeout=self.timeout)
            except Exception as error:
                if self.verbose is True:
                    print(f"Error: {error}")
                self.response = None
                self.code = 0
                return {}
        else:
            try:
                self.response = requests.get(url, timeout=self.timeout)
            except Exception as error:
                if self.verbose is True:
                    print(f"Error: {error}")
                self.response = None
                self.code = 0
                return {}
            
        self.code = self.response.status_code
        
        try:
            json_data = self.response.json() if self.response.status_code == 200 else {}
        except Exception as error:
            if self.verbose is True:
                print(f"Error: {error}")
            json_data = {}
        return json_data
    
    def getResponse(self):
        return self.response
    
    def getURL(self):
        return self.url
    
    def getStatus(self):
        return self.code