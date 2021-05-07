import urllib.request
import xml.dom.minidom
import re
from module_structures import POINT


def runParse(data, count=False, currentVal = ''):
    res = ()
    res_list = []
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req={}'.format(data)
    response = urllib.request.urlopen(url)
    dom = xml.dom.minidom.parse(response)
    dom.normalize()
    nodeArray = dom.getElementsByTagName("Valute")
    for node in nodeArray:
        childList = node.childNodes
        name = str(childList[3].childNodes[0].nodeValue)
        if (currentVal != ""):
            if (name == currentVal):    
                price = str(childList[4].childNodes[0].nodeValue)
                price = price.replace(",", ".")
                price = float(price)
                obj = POINT(price, name, data, count)
                return obj

        else:
            if (count):
                count = str(childList[2].childNodes[0].nodeValue)
            price = str(childList[4].childNodes[0].nodeValue)
            price = price.replace(",", ".")
            obj =  POINT(price, name, data, count)     
            res_list.append(obj)
    if (len(nodeArray) == 0):
        return POINT(None, currentVal, data, count) 
    return res_list

