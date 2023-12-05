""" Web Download Utils """

__all__ = ["WebIO", "WebData"]

from urllib.request import urlopen, Request
from urllib.error import URLError
from .webutil import wait, sleep


class WebData:
    def __repr__(self):
        return f"WebData(code={self.code})"
        
    def __init__(self, data, code):
        self.data = data
        self.code = code
        
    def getData(self):
        return self.data
    
    def getCode(self):
        return self.code


class WebIO:
    def __repr__(self):
        return f"WebIO({self.user_agent})"
    
    def __init__(self, **kwargs):
        self.verbose = kwargs.get('verbose', False)
        self.url = None
        self.user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
        self.debug = self.verbose
        self.sleep = sleep
        self.wait = wait
        
        if self.verbose is True:
            print(self.__repr__())
        
    def get(self, url: str) -> 'WebData':
        assert isinstance(url, str), f"url [{url}] is not a str"
        request = Request(url, None, self.headers)
        self.url = url
        try:
            response = urlopen(request)
        except URLError as e:
            response = None
            if self.debug:
                print("URL ERROR: {0}".format(e.__dict__))

        if response is not None:
            try:
                urldata = response.read()
                urlcode = response.getcode()
            except Exception as error:
                urldata = None
                urlcode = None
                if self.debug:
                    print(f"Error: {error}")

            retval = WebData(data=urldata, code=urlcode)
            return retval
        else:
            retval = WebData(data=None, code=None)
            return retval
    
    def getURL(self):
        return self.url