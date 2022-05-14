"""
Execute below cmd:
python analyseTag.py <xml_file> <tagname>

"""

import xml.etree.ElementTree as ET
import pandas as pd
import sys
import os
import json

GENERATE_XLSHEET = True

def cleanTagName(tagname):
    return tagname.split('}')[-1] if '}' in tagname else tagname

def generateSheetFromAttributeDict(attr_dict, filename):
    df = pd.DataFrame(attr_dict)
    with pd.ExcelWriter(filename) as writer:
        df.to_excel(writer, index=False)

def generateJSONFromAttributeDict(attr_dict, filename):
    with open(filename, "w") as outfile:
        json.dump(attr_dict, outfile)

def getAllXTags(root, tag, tag_list=[], xpath=''):
    curr_tag_name = cleanTagName(root.tag)
    if tag.upper()==curr_tag_name.upper():
        obj = {}
        obj['xpath'] = f'{xpath}/{curr_tag_name}'
        obj['element'] = root
        tag_list.append(obj)
    for child in root:
        getAllXTags(child, tag, tag_list, f'{xpath}/{curr_tag_name}')
    return tag_list

def getAllAttributesAndValues(nodes, contain_xpath=False, append_attr_dict={}):
    attr_dict = append_attr_dict
    for node in nodes:
        element = node['element']
        for attr, val in dict(element.attrib).items():
            attr_dict[attr] = attr_dict.get(attr, set())
            attr_dict[attr].add(val)
        if contain_xpath:
            attr_dict['xpath'] = attr_dict.get('xpath', set())
            attr_dict['xpath'].add(node['xpath'])
    return attr_dict

def generateSheetForXTagList(tag_list, filename):
    rows = []
    for node in tag_list:
        row = {}
        row['Text'] = str(node['element'].text).strip()
        row['XMLString'] = ET.tostring(node['element'])
        row['ChildTags'] = ','.join([cleanTagName(child.tag) for child in node['element']])
        row['Xpath'] = node['xpath']
        row.update(node['element'].attrib)
        rows.append(row)
    df = pd.DataFrame(rows)
    df.to_csv(filename, index=False)

def main():
    path = sys.argv[1]
    tagname = sys.argv[2]
    file_list = path.split('.')
    if len(file_list)==2 and file_list[-1]=='xml':
        files = [path]
        path = ''
    else:
        files = list(filter(lambda x: x.split('.')[-1]=='xml', os.listdir(path)))
    attr_dict = {}
    rel_path = f'{path}/' if path else ''
    for file in files:
        tree = ET.parse(f'{rel_path}{file}')
        root = tree.getroot()
        nodes = getAllXTags(root, tagname)
        attr_dict = getAllAttributesAndValues(nodes, contain_xpath=True, append_attr_dict=attr_dict)
    for key in attr_dict:
        attr_dict[key] = list(attr_dict[key])
    
    json_filename = f'{tagname.upper()}.json'
    excel_filename = f'{tagname.upper()}.csv'
    generateJSONFromAttributeDict(attr_dict, json_filename)
    if GENERATE_XLSHEET:
        generateSheetForXTagList(nodes, excel_filename)

if __name__=="__main__":
    main()
