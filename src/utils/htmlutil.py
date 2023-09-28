""" Basic HTML (BeautifulSoup) Functions """

__all__ = ["isBS4", "isBS4Tag", "removeTag"]

from bs4 import BeautifulSoup, element
from copy import copy


def isBS4(bsdata, debug=False):
    return isinstance(bsdata, BeautifulSoup)


def isBS4Tag(bsdata, debug=False):
    return isinstance(bsdata, element.Tag)


def removeTag(line, tag):
    '''
    removeTag: Removes <tag> elements from <line>
    
    Inputs:
        > line: html string
        > tag: html string
        
    Output:
        > line: html string
    '''
    if isBS4Tag(line):
        nline = copy(line)
        for tagVal in nline.findAll(tag):
            tagVal.extract()
        return nline
    return line