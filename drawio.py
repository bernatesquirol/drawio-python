import xml.etree.ElementTree as ET
import json
import copy
import urllib
import base64
import gzip
import zlib


# +
# root = ET.fromstring(decompress_graph("jVAxDsMgDHwNO4Glc5M2U6e+ACVuQIKCwG3I7+uEtFGGSB2Qznc+czaTtcttVEHffA+WyQuTdfQeC3K5BmuZ4KZnsmFCcHpMXA/UalF5UBGe+I9BFMNb2RcUphAJJ7sSZDAhUXEetUG4B9XNykiZidPoKHRTEVQpQDf/+jAZaP55nQ0RIR/mW6g1XAveAcaJWkbToy4dp7IC12AGjXtOpVIPP+e2LIF132+53XXRdmf/AA=="))
# -

# compression tools for draw.io

def bytes_to_string(byte_array):
    return [chr(x) for x in byte_array]


def compress_graph(to_compress):    
    import urllib
    import zlib
    url_encoded = urllib.parse.quote(to_compress, safe='')
    compressor = zlib.compressobj(wbits=-15)
    compressed = list(compressor.compress(bytes(url_encoded,'utf-8')))
    compressed += compressor.flush()
    return base64.b64encode(bytes(compressed))


def decompress_graph(bytes_compressed):    
    import urllib
    import zlib
    decompressed = zlib.decompress(base64.b64decode(bytes_compressed), wbits=-15)
    return urllib.parse.unquote(decompressed.decode("utf-8"))


# Cell operations drawio

BASICS_FILE = 'basics.xml'


def get_single_cell_from_lib(xml_source, title, name=None):
    mxlib = ET.parse(xml_source)
    lib_components = json.loads(mxlib.getroot().text)
    input_c = [c for c in lib_components if c['title']==title][0]
    return ET.fromstring(decompress_graph(input_c['xml']).format(name))[0][2]


def get_geometry(cell):
    geometry = copy.copy(cell.find('mxGeometry').attrib)
    for key in geometry:
        try:
            geometry[key]=int(geometry[key])
        except:
            pass
    return geometry


def update_geometry(cell, x=None, y=None, width=None, height=None):
    geometry = cell.find('mxGeometry')
    if width!=None:
        geometry.attrib['width']=str(width)
    if height!=None:
        geometry.attrib['height']=str(height)
    if x!=None:
        geometry.attrib['x']=str(x)
    if y!=None:
        geometry.attrib['y']=str(y)
    return cell


def update_single_cell(cell, cell_id=None, parent_id=None):
    if cell_id != None:
        cell.attrib['id']=str(cell_id)
    if parent_id != None:
        cell.attrib['parent']=str(parent_id)
    return cell#, geometry.attrib['width'], geometry.attrib['height']


def input_cell(name, input_id, parent_id):
    real_input = get_single_cell_from_lib(BASICS_FILE, 'input', name)
    return update_single_cell(real_input, input_id, parent_id)


def output_cell(name, output_id, parent_id):
    real_output = get_single_cell_from_lib(BASICS_FILE, 'output', name)
    return update_single_cell(real_output, output_id, parent_id)


def function_cell(inputs, outputs, function_id, function_name):
    function = get_single_cell_from_lib(BASICS_FILE, 'function', function_name)
    function = update_single_cell(function, function_id, '{parent_id}')
    geo_func = get_geometry(function)
    inputs_c = [input_cell(input_c, input_c, function_id) for input_c in inputs]
    padding_side = 10
    y_in=5
    for cell_in in inputs_c:
        geo = get_geometry(cell_in)
        update_geometry(cell_in, x=padding_side, y=y_in)
        y_in+=2+int(geo['height'])
    
    outputs_c = [output_cell(output_c, output_c, function_id) for output_c in outputs]
    y_out=5
    for cell_in in outputs_c:
        geo = get_geometry(cell_in)
        update_geometry(cell_in, x=(geo_func['width']-padding_side-geo['width']), y=y_out)
        y_out+=2+int(geo['height'])
    update_geometry(function, height=max(y_in,y_out))
    return [function]+outputs_c+inputs_c


def create_diagram(list_et):
    # A4 landscape
    model = ET.fromstring('<mxGraphModel dx="2153" dy="1303" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0"/>')
    root = ET.SubElement(model, 'root')
    ET.SubElement(root, 'mxCell', {'id':'0'})
    ET.SubElement(root, 'mxCell', {'id':'1', 'parent':'0'})
    for et in list_et:
        cell = ET.fromstring(ET.tostring(et).decode().format(parent_id='1'))
        root.append(cell)
    return model



def create_encoded_mxfile(diagram, id_diagram, page_name='Page-1'):
    mxfile = ET.Element('mxfile')
    diagram_cell = ET.SubElement(mxfile,'diagram',{'id':id_diagram, 'name':page_name})
    diagram_cell.text = compress_graph(ET.tostring(diagram).decode()).decode()
    return mxfile
    


def save_xml(mxfile, file_path):
    ET.ElementTree(mxfile).write(open(file_path,'w'), encoding='unicode')


# +
# function_id = 'func_1'
# function_name = 'nom_func_1'
# inputs = ['p1','p2']
# outputs = ['r1','r2']
# func_1 = function_cell(inputs, outputs, function_id, function_name)
# save_xml(create_encoded_mxfile(create_diagram(func_1), 'id_diagram_1'), 'compressed.xml')
# save_xml(create_diagram(func_1), 'no_compressed.xml')
# -

# Debug functions

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
