import urllib.request
import xml.dom.minidom
import re
def runParse(data):
    res = ()
    res_list = []
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?date_req={}'.format(data)
    response = urllib.request.urlopen(url)
    dom = xml.dom.minidom.parse(response)
    dom.normalize()
    nodeArray = dom.getElementsByTagName("Valute")
    for node in nodeArray:
        childList = node.childNodes
        count = str(childList[2].childNodes[0].nodeValue)
        name = str(childList[3].childNodes[0].nodeValue)
        price = str(childList[4].childNodes[0].nodeValue)
        price = price.replace(",", ".")
        res = (name, price, count)
        res_list.append(res)
    return res_list
