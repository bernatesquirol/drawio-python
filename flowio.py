# basics.xml draw.io library with simple cells: input, output & function

import xml.etree.ElementTree as ET
import json
import copy
import urllib
import base64
import gzip
import zlib
import drawio
from typing import List

BASICS_FILE = 'basics.xml'


def basic_cell(title:str, text: str, input_id: str, parent_id: str) -> ET.Element:
    """
    Returns basic cell, changing its title
    Args:
        title: 'input', 'output' o 'function' (titles in BASICS_FILE library)
        text: will appear inside the cell
        input_id: id of this particular cell
        parent_id: the id of the parent cell
    Returns:
        ET.Element xml
    """
    cell = drawio.get_single_cell_from_lib(BASICS_FILE, title)
    cell_formatted = ET.fromstring(ET.tostring(cell).decode().format(title=title))
    return drawio.update_mx(cell_formatted, input_id, parent_id)


def function_cell(inputs: List[str], outputs:List[str], function_id: str, function_name:str)->List[ET.Element]:
    """
    Returns list of all the elements that compose a function
    Args:
        inputs: list of names of the input parameters 
        outputs: list of names of the output parameters 
        function_id: id of the function cell
        function_name: title of the function cell
    Returns:
        List of all ETs: the function + ouputs + inputs
    """
    function = basic_cell('function', function_name, function_id, '{parent_id}')
    geo_func = drawio.get_mxGeometry(function)
    inputs_c = [basic_cell('input', input_c, input_c, function_id) for input_c in inputs]
    outputs_c = [basic_cell('output', output_c, output_c, function_id) for output_c in outputs]    
    padding_side = 15
    y_in=5
    for cell_in in inputs_c:
        geo = drawio.get_mxGeometry(cell_in)
        drawio.update_mxGeometry(cell_in, x=padding_side, y=y_in)
        y_in+=2+int(geo['height'])
    y_out=5
    for cell_in in outputs_c:
        geo = drawio.get_mxGeometry(cell_in)
        drawio.update_mxGeometry(cell_in, x=(geo_func['width']-padding_side-geo['width']), y=y_out)
        y_out+=2+int(geo['height'])
    drawio.update_mxGeometry(function, height=max(y_in,y_out))
    return [function]+outputs_c+inputs_c


def create_diagram(list_et: List[ET.Element])->ET.Element:
    """
    Creation of a diagram given 
    Args:
        list_et: list of ETs which can have '{parent_id}' as parent_id
    Returns:
        ET.Element of type mxGraphModel
    """
    model = ET.fromstring('<mxGraphModel dx="2153" dy="1303" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1169" pageHeight="827" math="0" shadow="0"/>')
    root = ET.SubElement(model, 'root')
    ET.SubElement(root, 'mxCell', {'id':'0'})
    ET.SubElement(root, 'mxCell', {'id':'1', 'parent':'0'})
    for et in list_et:
        cell = ET.fromstring(ET.tostring(et).decode().format(parent_id='1'))
        root.append(cell)
    return model


def create_encoded_mxfile(diagram:ET.Element, id_diagram: str, page_name: str='Page-1')->ET.Element:
    mxfile = ET.Element('mxfile')
    diagram_cell = ET.SubElement(mxfile,'diagram',{'id':id_diagram, 'name':page_name})
    diagram_cell.text = drawio.compress_graph(ET.tostring(diagram).decode()).decode()
    return mxfile


def save_xml(mxfile: ET.Element, file_path: str)->None:
    ET.ElementTree(mxfile).write(open(file_path+'.drawio','w'), encoding='unicode')

# +
# import test
# function_id = 'func_1'
# function_name = 'nom_func_1'
# inputs = ['p1','p2']
# outputs = ['r1','r2']
# func_1 = function_cell(inputs, outputs, function_id, function_name)
# save_xml(create_encoded_mxfile(create_diagram(func_1), 'id_diagram_1'), 'compressed.xml')
# save_xml(create_diagram(func_1), 'no_compressed.xml')
# -


