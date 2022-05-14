'''
INPUT: XML file path
OUTPUT: Sheet containing Xpaths and Tags

python tag_Xpath.py <path_to_xml>
'''
import xml.etree.ElementTree as ET
import pandas as pd
import sys

tree = ET.parse(sys.argv[1])
root = tree.getroot()

pathTagMap = {}

def parseXPath(node, path = ''):
    curtag = node.tag
    path = path+'/'+curtag
    if path not in pathTagMap:
        pathTagMap[path] = curtag
    for child in node:
        parseXPath(child, path)

parseXPath(root)
df = pd.DataFrame(data=pathTagMap.items(), columns=['Xpath', 'Tag'])
df.to_excel('tag_xpath.xlsx')
