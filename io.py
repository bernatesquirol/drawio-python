# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.3'
#       jupytext_version: 1.0.5
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

import urllib
import base64
import gzip
import zlib


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

# +
#decompress_graph(compressed_original)==uncompressed

# +
#compress_graph(uncompressed)==compressed_original
# -


