"""
To run the script, execute:
python splitXmls.py

INPUT_PATH is the path to product folders having their respective xmls.
OUTPUT_PATH is the path to the output folder where the split xml product folders are to be generated.

Fill the CHAPTER_TAGS list with all the chapter level tag names for the products.
"""

import os
import xml.etree.ElementTree as ET

INPUT_PATH = 'C:/Users/C283803/Desktop/ScratchyAutomationScripts/tempContainer/New folder'
OUTPUT_PATH = 'C:/Users/C283803/Desktop/ScratchyAutomationScripts/tempContainer/out'
CHAPTER_TAGS = ['Chapter']

def getElementsFromTagname(root, childname, roots):
    for child in root:
        if child.tag.upper()==childname.upper():
            roots.append(child)
    for child in root:
        getElementsFromTagname(child, childname, roots)

def saveFileFromTree(tree, filename):
    tree.write(filename)

def saveSplitFiles(roots, split_file_prefix):
    for index in range(len(roots)):
        tree = ET.ElementTree(roots[index])
        saveFileFromTree(tree, f'{split_file_prefix}_chapter_{index+1}.xml')

def main():
    for dir in os.listdir(INPUT_PATH):
        print(f'Working on {dir}')
        split_roots = []
        split_file_prefix = dir
        os.chdir(f'{INPUT_PATH}/{dir}')
        print('Working on files:')
        for file in os.listdir(os.getcwd()):
            if file[-3:]!='xml':
                continue
            print(file)
            tree = ET.parse(file)
            root = tree.getroot()
            for split_root_name in CHAPTER_TAGS:
                print(split_root_name)
                getElementsFromTagname(root, split_root_name, split_roots)
        os.chdir(OUTPUT_PATH)
        if dir not in os.getcwd():
            os.mkdir(dir)
        os.chdir(f'{os.getcwd()}/{dir}')
        saveSplitFiles(split_roots, split_file_prefix)

if __name__=="__main__":
    main()