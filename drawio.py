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

# Compression tools for draw.io

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

def get_single_cell_from_lib(xml_source: str, title: str)->ET.ElementTree:
    """
    Returns first mxGeometry occurence in recursive children
    Args:
        xml_source: path of xml
        title: title of element in library
    Returns:
        ET
    """
    mxlib = ET.parse(xml_source)
    lib_components = json.loads(mxlib.getroot().text)
    input_c = [c for c in lib_components if c['title']==title][0]
    return ET.fromstring(decompress_graph(input_c['xml']))[0][2]


def get_mxGeometry(cell: ET.ElementTree)->object:
    """
    Returns first mxGeometry occurence in recursive children
    Args:
        cell: ElementTree
    Returns:
        object with geometry attributes
    """
    geometry_cell = next(cell.iter('mxGeometry'))
    geometry = copy.copy(geometry_cell.attrib)
    for key in geometry:
        try:
            geometry[key]=int(geometry[key])
        except:
            pass
    return geometry


def update_mxGeometry(cell_obj: ET.ElementTree, x:float=None, y:float=None, width:float=None, height:float=None)->ET.Element:
    """
    Updates mxGeometry attributes and returns cell
    Args:
        cell_obj: cell
        x: new x
        y: new y
        width: new width
        height: new height
    Returns:
        Same cell with updated geometry
    """
    geometry = next(cell_obj.iter('mxGeometry'))
    if width!=None:
        geometry.attrib['width']=str(width)
    if height!=None:
        geometry.attrib['height']=str(height)
    if x!=None:
        geometry.attrib['x']=str(x)
    if y!=None:
        geometry.attrib['y']=str(y)
    return cell_obj


def update_mxCell(cell_obj:ET.ElementTree, cell_id:str=None, parent_id:str=None):
    """
    Updates mxCell attributes and returns cell
    Args:
        cell_obj: cell
        cell_id: new cell_id
        parent_id: new parent_id
    Returns:
        Same cell with updated mxCell
    """
    cell = next(cell_obj.iter('mxCell'))
    if cell_id != None:
        cell.attrib['id']=str(cell_id)
    if parent_id != None:
        cell.attrib['parent']=str(parent_id)
    return cell_obj#, geometry.attrib['width'], geometry.attrib['height']


def update_mx(cell:ET.ElementTree, cell_id:str=None, parent_id:str=None):
    """
    Updates cell attributes and returns cell
    Args:
        cell_obj: cell
        cell_id: new cell_id
        parent_id: new parent_id
    Returns:
        Same cell with updated mxCell
    """
    if cell_id != None:
        cell.attrib['id']=str(cell_id)
    if parent_id != None:
        cell.attrib['parent']=str(parent_id)
    return cell
