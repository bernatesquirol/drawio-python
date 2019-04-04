import xml.etree.ElementTree as ET


def indent(elem_o, level=0):
    import copy
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    #elem = copy.deepcopy(elem_o)
    elem = elem_o
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem 


def print_tree(tree):
    ET.dump(indent(tree))


def print_xml(xml):
    graphmodel = ET.fromstring(decompress_graph(xml))
    ET.dump(indent(graphmodel))


