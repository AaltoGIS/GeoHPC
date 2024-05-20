import os
import fiona
import shapely.geometry

from merge      import merge_geometries
from projection import project_to_epsg_3067_if_needed


def merge_from_layer(
        fn_tile,
        layer_name,
        include_LUOKKA,      # the list of LUOKKA attribute values to include
        join_attribute_name, # the attribute used to merge features
        index,               # the count of the attribute values
        geometry_buffer):    # a dictionary to store the geometries that will be merged
    """
    Find from the given layer all the features whose LUOKKA attribute is included in include_LUOKKA.

    If the feature was not split, save it immediately into the write_buffer.
    Otherwise, add its geometry into the geometry_buffer dictionary. If all the
    parts with the same KOHDEOSO have been found, merge the geometries and add the
    result into the write_buffer.
    """
    write_buffer = []

    with fiona.open(fn_tile, 'r', layer=layer_name) as fin:
        for feature in fin:
            luokka = feature.properties['LUOKKA']
            if not luokka in include_LUOKKA:
                continue
            key  = feature.properties[join_attribute_name]
            geom = project_to_epsg_3067_if_needed(
                shapely.geometry.shape(feature.geometry))
            if index[key] == 1:
                write_buffer.append({
                    'geometry': shapely.geometry.mapping(geom),
                    'properties': feature.properties
                })
            else:
                geometry_buffer[key].append(geom)
                if len(geometry_buffer[key]) == index[key]:
                    #
                    # We have gathered all the features with this
                    # join_attribute_name value
                    #
                    try:
                        merged = merge_geometries(geometry_buffer[key])
                    except Exception as e:
                        print(f'ERROR {fn_tile=} {layer_name=} Merging features with {join_attribute_name}={key} failed.')
                        continue
                    new_features = [
                        {
                            'geometry': shapely.geometry.mapping(g),
                            'properties': feature.properties
                        } for g in merged]
                    write_buffer += new_features
                    #
                    # We don't need these geometries anymore
                    #
                    del geometry_buffer[key]

    return write_buffer


def create_merged_layer(
        file_list,
        join_attribute_name,
        index,
        layer_spec,
        path_out):
    """
    Gather requested features from the tiles, merge the split features back into single
    features, and write them into a single layer.
    """
    #
    # First we open one layer from one of the tiles to get the schema of the
    # original data.
    #
    fn_tile = file_list[0]
    with fiona.open(f'/vsizip/{fn_tile}') as fin:
        schema = fin.schema

    #
    # We don't know which layer we opened, so the geometry type can be anything.
    # Let's update that to the type that we are currently creating.
    #
    schema['geometry'] = layer_spec['geometry_type']

    #
    # A buffer to store the geometries we are reading from the tiles. Only
    # needed for the join_attribute_name with multiple occurrences.
    #
    geometry_buffer = {key: [] for key, count in index.items() if count > 1}

    #
    # Another buffer to store the new features. It is inefficient to write
    # features to file one by one, so instead we store them on this buffer and
    # write larger batches every now and then.
    #
    write_buffer = []

    fn_out = os.path.join(path_out, layer_spec['filename'])
    with fiona.open(fn_out, 'w', layer=layer_spec['layername'], schema=schema, crs=fiona.crs.CRS.from_epsg(3067)) as fout:
        for fn_tile in file_list:
            print(f'Info: Processing "{fn_tile}"...')
            layer_names = fiona.listlayers(f'/vsizip/{fn_tile}')
            for layer_name in layer_names:
                write_buffer += merge_from_layer(
                    f'/vsizip/{fn_tile}', layer_name, layer_spec['include_LUOKKA'], join_attribute_name, index, geometry_buffer)

            #
            # If the write_buffer has enough items, write on in the output file
            # and clear the buffer.
            #
            if len(write_buffer) > 10000:
                fout.writerecords(write_buffer)
                write_buffer = []

        #
        # Final write, the buffer may contains some elements.
        #
        if len(write_buffer):
            fout.writerecords(write_buffer)
