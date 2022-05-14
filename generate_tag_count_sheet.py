'''
Used to generate sheet containing count of internal tags in each root tags.

python generate_count_sheet.py <xml_filename> <root_tagname> <root_id_attribute> <internal_tagname_1> [internal_tagname_2] ...

Ex.:
python generate_count_sheet.py Chapter_CHAP_3.xml deck N logo flogo logoform
'''
import xml.etree.ElementTree as ET
import pandas as pd
import sys

def getAllXTags(root, tag, tag_list=[], xpath=''):
    if tag.upper()==root.tag.upper():
        obj = {}
        obj['xpath'] = f'{xpath}/{root.tag}'
        obj['element'] = root
        tag_list.append(obj)
    for child in root:
        getAllXTags(child, tag, tag_list, f'{xpath}/{root.tag}')
    return tag_list

def getChildXTagCount(root, tag):
    count = 0
    if root.tag.upper()==tag.upper():
        count+=1
    for child in root:
        count+=getChildXTagCount(child, tag)
    return count

def main():
    xml_file, root_tag, root_id_attr = sys.argv[1:4]
    internal_tags = sys.argv[4:]
    tree = ET.parse(xml_file)
    root = tree.getroot()
    root_tags = getAllXTags(root, root_tag)
    rows = []
    for tag in root_tags:
        count_dict = {}
        element = tag['element']
        count_dict[root_id_attr] = element.attrib[root_id_attr]
        count_dict[f'{internal_tags[0]}_count'] = 0
        for internal_tag in internal_tags:
            count_dict[f'{internal_tags[0]}_count'] += getChildXTagCount(element, internal_tag)
        rows.append(count_dict)
    df = pd.DataFrame().from_records(rows)
    xml_name = xml_file.split('.')[0]
    df.to_csv(f'{internal_tags[0]}_count_in_{root_tag}_{xml_name}.csv')

if __name__=="__main__":
    main()
