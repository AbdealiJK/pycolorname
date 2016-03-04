# -*- coding: utf-8 -*-
"""
Created on Sat Jun 30 22:57:26 2012

@author: drtrigon
"""

import pickle

from helper import *


colors_01 = loadData('RAL_wikipedia.pkl')
colors    = colors_01  


# RAL color look-up table from http://de.wikipedia.org/wiki/RAL-Farbe
# WITHOUT 9000 codes except 9003 and 9005 !
#
# (should be according to Categories available in Commons and more)
# other/alternative color system include "NCS" and "Pantone"


def getPMSdata_wikipedia():
    sys.path.insert(0, '..')
    sys.path.insert(0, '.')
    
    import wikipedia as pywikibot
    from pywikibot.comms import http
    import BeautifulSoup

    # put code here ...


def getNames():
    colors_names = {
    u'1': u'Yellow/Beige',
    u'2': u'Orange',
    u'3': u'Red',
    u'4': u'Violet',
    u'5': u'Blue',
    u'6': u'Green',
    u'7': u'Gray',
    u'8': u'Brown',
    #u'9': u'White/Black',
    u'9003': u'White',
    u'9005': u'Black',
    }
    
    return colors_names

def assignColorNames(data, names_dict):
    result = {}
    for item in data:
        if (item[0] == u'9'):
            key = u'RAL %s (%s)' % (item, names_dict[item])
        else:
            key = u'RAL %s (%s)' % (item, names_dict[item[0]])
        result[key] = data[item]
    return result


def refresh():
#    data_01 = getPMSdata_wikipedia()
#    storeData('RAL_wikipedia_raw.pkl', data_01)
    data_01 = loadData('RAL_wikipedia_raw.pkl')

    data = data_01

    print "Retrieved number of colors:", len(data)

    names_dict = getNames()

    data = assignColorNames(data, names_dict)
    for item in data:
        print item, data[item]
    storeData('RAL_wikipedia.pkl', data)
    print "Processed number of colors:", len(data)


if __name__ == '__main__':
    import re, sys
    
    refresh()
