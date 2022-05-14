'''
INPUT: Mastersheet with all xpaths in order according to XML
OUTPUT: Skeleton XML
'''
import pandas as pd
from xml.etree import ElementTree as ET

MASTERSHEET_FILEPATH = './mastersheet.xlsx'
OUTPUT_XML_PATH = './legacy_skeleton.xml'

def gen_legacy_skeleton_etree(xpaths):
    # assuming all the xpaths are listed as they occur in XML
    root_name = xpaths[0].split('/')[-1]  # considering first xpath to be of the form '/root' and the XML has only
    # one root node
    root = ET.Element(root_name)
    tag_node = {xpaths[0]: root}  # dictionary storing the skeleton etree nodes for the corresponding xpaths
    for xpath in xpaths:
        print(xpath)
        if xpath not in tag_node:
            tag_names = xpath.split('/')
            new_tag_name, parent_xpath = tag_names[-1], '/'.join(tag_names[:-1])
            node = tag_node[parent_xpath]
            tag_node[xpath] = ET.SubElement(node, new_tag_name)

    return root

if __name__=='__main__':
    print('Reading mastersheet...')
    df = pd.read_excel(MASTERSHEET_FILEPATH)
    xpaths = list(df['Xpaths'])
    print('Generating the model tree...')
    root = gen_legacy_skeleton_etree(xpaths)
    etree = ET.ElementTree(root)
    print('Generated the tree. Writing XML to file...')
    etree.write(OUTPUT_XML_PATH)
    print('Dumped the skeleton XML to file.')