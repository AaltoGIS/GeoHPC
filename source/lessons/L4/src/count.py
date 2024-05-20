import os
import pickle

import fiona

from utils import add_to_dict


def count_from_layer(fn_tile, layer_name, join_attribute_name):
    occurences = dict()

    with fiona.open(fn_tile, layer=layer_name) as fin:
        for feature in fin:
            
            key = feature.properties[join_attribute_name]
            
            if key in occurences:
                
                occurences[key] += 1
                
            else:
                
                occurences[key] = 1
                
    return occurences


def count_from_zip(fn, join_attribute_name):
    """
    Iterate over the layers in the given zip file and count the occurences of
    different values of the attribute `join_attribute_name`.
    """
    occurences = dict()
    zip_layers = fiona.listlayers(f'/vsizip/{fn}')

    for layer_name in zip_layers:
        
        occ = count_from_layer(f'/vsizip/{fn}', layer_name, join_attribute_name)
        
        add_to_dict(occurences, occ)

    return occurences


def count_from_zipfiles(file_list, join_attribute_name):
    """
    Iterate over the zip files in the given path and count the occurences of
    different values of the attribute `join_attribute_name` in each file.
    """
    occurences = dict()

    for fn_tile in file_list:
        
        print(f'Counting from "{fn_tile}"...')
        
        occ = count_from_zip(fn_tile, join_attribute_name)
        
        add_to_dict(occurences, occ)

    return occurences
