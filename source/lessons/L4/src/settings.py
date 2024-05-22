layer_specs = {
    2005: {
        'path_tiles': '/projappl/project_2009245/GeoHPC/source/lessons/L4/2005_tiles',
        'join_attribute_name': 'KOHDEOSO',
        'layers': {
            0: {
                'include_LUOKKA': [35411, 35412, 35421, 35422, 35300],
                'filename': '2005_vakavesi.gpkg',
                'layername': 'vakavesi',
                'geometry_type': 'Polygon'
            },
            1: {
                'include_LUOKKA': [
                    42210, 42211, 42212, 42220, 42221, 42222, 42230, 42231,
                    42232, 42240, 42241, 42242, 42250, 42251, 42252, 42260,
                    42261, 42262, 42270
                ],
                'filename': '2005_rakennus.gpkg',
                'layername': 'rakennus',
                'geometry_type': 'Polygon'
            }
        }
    }
}

output_settings = {
    'path': '/scratch/project_200xxxx/topoDB'
}

#
# Some checks for the settings.
#

#
# Make sure that each layer is going into a separate output file.
#
for d in layer_specs.values():
    layer_names = [layer['filename'] for layer in d['layers'].values()]
    n = len(layer_names)
    m = len(set(layer_names))
    if m < n:
        raise Exception('Outputting different layers to the same file is not implemented.')
