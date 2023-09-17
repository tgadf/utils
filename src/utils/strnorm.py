""" A simple utility class for measuring timing of processes """

__all__ = ["NormalizeString"]

from unicodedata import normalize
import re

class NormalizeString:
    def __init__(self, debug=False):
        self.debug = debug

        self.byteMap = {}
        self.byteMap[re.compile(b'\xe2\x80[\x90-\x94]')] = b'-'
        self.byteMap[re.compile(b'\xe2\x80[\xb2-\xb7]')] = b"'"
        self.byteMap[re.compile(b'\xe2\x80[\x98,\x9b]')] = b"'"
        self.byteMap[re.compile(b'\xe2\x80\x99')]        = b"'"
        self.byteMap[re.compile(b'\xe2\x80[\x9c-\x9f]')] = b'"'
        self.byteMap[re.compile(b'\xe2\x80\xa6')]        = b'...'
        self.byteMap[re.compile(b'\xe2\x81\xba')]        = b'+'
        self.byteMap[re.compile(b'\xe2\x81\xbb')]        = b'-'
        self.byteMap[re.compile(b'\xe2\x81\xbc')]        = b'='
        self.byteMap[re.compile(b'\xe2\x81\xbd')]        = b'('
        self.byteMap[re.compile(b'\xe2\x81\xbe')]        = b')'
    
        self.byteMap[re.compile(b'\xe2\x80[\x80-\x8f]')] = b''
    
    def check(self, s):
        if not isinstance(s, str):
            if self.debug:
                print("Not a string [{0}]".format(s))
            return False
        
        if s.isascii():
            return False
        
        return True
    
    def convert(self, s):
        ##################################################################
        ### Check to see if we even need to run convert()
        ##################################################################
        if self.check(s) is False:
            return s

        
        ##################################################################
        ### Normalize and Encode into Bytes
        ##################################################################
        sNorm = normalize('NFD', s)        
        sByte = sNorm.encode()

        
        ##################################################################
        ### Specific Latin Ascii Replacements
        ##################################################################
        for pattern,value in self.byteMap.items():
            if pattern.search(sByte) is not None:
                if self.debug:
                    print("Found pattern match:",pattern,' --> ',value)
                return re.sub(pattern, value, sByte).decode('utf-8')
        
        
        ##################################################################
        ### Return Normalized String
        ##################################################################
        return sNorm