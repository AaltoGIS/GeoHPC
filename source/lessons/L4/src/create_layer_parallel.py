import os

import fiona
import shapely.geometry

from merge        import merge_geometries
from create_layer import merge_from_layer
from projection   import project_to_epsg_3067_if_needed


def create_merged_layer(
        procs,
        join_attribute_name,
        index,
        layer_spec,
        path_out):
    #
    # A buffer to store the geometries we are reading from the tiles. Only
    # needed for the join_attribute_name with multiple occurrences.
    #
    geometry_buffer = {key: [] for key, count in index.items() if count > 1}

    with fiona.open(os.path.join(path_out, f'{layer_spec["filename"]}.0_{procs}_single')) as fin:
        schema = fin.schema
        crs    = fin.crs
        driver = fin.driver

    fn_out = os.path.join(path_out, layer_spec['filename'])
    write_buffer = []
    with fiona.open(fn_out, 'w', layer=layer_spec['layername'], driver=driver, crs=crs, schema=schema) as fout:
        for rank in range(procs):
            rank_fn_out_single = os.path.join(path_out, f'{layer_spec["filename"]}.{rank}_{procs}_single')
            rank_fn_out_parts  = os.path.join(path_out, f'{layer_spec["filename"]}.{rank}_{procs}_parts')
            #
            # Transfer the non-split features directly.
            #
            with fiona.open(rank_fn_out_single) as fin:
                for feature in fin:
                    write_buffer.append(feature)

            write_buffer += merge_from_layer(rank_fn_out_parts, layer_spec['layername'], layer_spec['include_LUOKKA'], join_attribute_name, index, geometry_buffer)

            fout.writerecords(write_buffer)
            write_buffer.clear()


def extract_from_layer(
        fn_tile,
        layer_name,
        include_LUOKKA,
        join_attribute_name,
        index,
        write_buffer_single,
        write_buffer_parts):
    """
    Find from the given layer all the features whose LUOKKA attribute is included in include_LUOKKA.

    If the feature was not split, save it immediately into the write_buffer.
    Otherwise, add its geometry into the geometry_buffer dictionary. If all the
    parts with the same KOHDEOSO have been found, merge the geometries and add the
    result into the write_buffer.
    """

    with fiona.open(f'/vsizip/{fn_tile}', 'r', layer=layer_name) as fin:
        for feature in fin:
            luokka = feature.properties['LUOKKA']
            if not luokka in include_LUOKKA:
                continue
            key = feature.properties[join_attribute_name]
            geom = project_to_epsg_3067_if_needed(
                shapely.geometry.shape(feature.geometry))
            if index[key] == 1:
                write_buffer_single.append({
                    'geometry': shapely.geometry.mapping(geom),
                    'properties': feature.properties
                })
            else:
                write_buffer_parts.append({
                    'geometry': shapely.geometry.mapping(geom),
                    'properties': feature.properties
                })


def extract_features(
        rank,
        procs,
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
    # Note: These temporary files must have unique names, otherwise another
    # program that is creating another layer might overwrite these. This is
    # also the reason we required each layer to be written to separate file in
    # settings.py
    #
    my_fn_out_single = os.path.join(path_out, f'{layer_spec["filename"]}.{rank}_{procs}_single')
    my_fn_out_parts  = os.path.join(path_out, f'{layer_spec["filename"]}.{rank}_{procs}_parts')
    #
    # First we open one layer from one of the tiles to get the schema of the
    # original data.
    #
    with fiona.open(f'/vsizip/{file_list[0]}') as fin:
        schema = fin.schema

    #
    # We don't know which layer we opened, so the geometry type can be anything.
    # Let's update that to the type that we are currently creating.
    #
    schema['geometry'] = layer_spec['geometry_type']

    #
    # Another buffer to store the new features. It is inefficient to write
    # features to file one by one, so instead we store them on this buffer and
    # write larger batches every now and then.
    #
    write_buffer_single = []
    write_buffer_parts  = []

    with fiona.open(my_fn_out_single, 'w', driver='GPKG', layer=layer_spec['layername'], schema=schema, crs=fiona.crs.CRS.from_epsg(3067)) as fout_single, \
         fiona.open(my_fn_out_parts,  'w', driver='GPKG', layer=layer_spec['layername'], schema=schema, crs=fiona.crs.CRS.from_epsg(3067)) as fout_parts:
        for fn_tile in file_list[rank::procs]:
            print(f'Info: Processing "{fn_tile}"...')
            layer_names = fiona.listlayers(f'/vsizip/{fn_tile}')
            for layer_name in layer_names:
                extract_from_layer(
                    fn_tile, layer_name, layer_spec['include_LUOKKA'], join_attribute_name, index, write_buffer_single, write_buffer_parts)

            for buf, fout in [[write_buffer_single, fout_single], [write_buffer_parts, fout_parts]]:
                #
                # If the write_buffer has enough items, write on in the output file
                # and clear the buffer.
                #
                if len(buf) > 10000:
                    fout.writerecords(buf)
                    buf.clear()

        #
        # Final write, the buffer may contains some elements.
        #
        for buf, fout in [[write_buffer_single, fout_single], [write_buffer_parts, fout_parts]]:
            #
            # If the write_buffer has enough items, write on in the output file
            # and clear the buffer.
            #
            if len(buf):
                fout.writerecords(buf)
