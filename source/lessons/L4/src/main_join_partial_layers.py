import os
import sys
import pickle

import fiona

from create_layer_parallel import create_merged_layer


def main():
    try:
        procs     = int(sys.argv[1])
        year      = int(sys.argv[2])
        layer_pos = int(sys.argv[3])
    except Exception:
        print('Usage: python main_create_merged_layer.py <procs> <year> <layer_index>.')
        return

    from settings import layer_specs
    from settings import output_settings

    layer_spec = layer_specs[year]['layers'][layer_pos]
    path_out   = os.path.join(output_settings['path'], f'{year}')

    fn_index = os.path.join(path_out, f'index_{year}.pckl')
    with open(fn_index, 'rb') as fin:
        index = pickle.load(fin)

    create_merged_layer(procs, layer_specs[year]['join_attribute_name'], index, layer_spec, path_out)


if __name__ == '__main__':
    main()
