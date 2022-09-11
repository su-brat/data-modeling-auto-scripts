from lxml import etree

tree = etree.parse('temp.xml')
with open('temp.txt', 'w') as f:
    # replacing all PI inside table with <newline> tag
    pis = tree.xpath('//table//processing-instruction()')
    for pi in pis:
        parent_tag = pi.getparent()
        replace_tag = etree.Element('newline')
        replace_tag.tail = pi.tail
        parent_tag.replace(pi, replace_tag)
    # replacing the rest of the PI with <space> tag
    pis = tree.xpath('//processing-instruction()')
    for pi in pis:
        parent_tag = pi.getparent()
        # replace with space tag
        replace_tag = etree.Element('space')
        replace_tag.tail = pi.tail
        parent_tag.replace(pi, replace_tag)
        # replace with hardcoded space
        # pi.tail = ' ' + pi.tail
        # parent_tag.strip_tags(pi)
    xml_string = etree.tostring(tree.getroot())
    f.write(str(xml_string))
