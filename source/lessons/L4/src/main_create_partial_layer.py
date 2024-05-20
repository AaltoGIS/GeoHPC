import os
import sys
import pickle

from create_layer_parallel import extract_features


def main():
    try:
        rank      = int(sys.argv[1])
        procs     = int(sys.argv[2])
        year      = int(sys.argv[3])
        layer_pos = int(sys.argv[4])
    except Exception:
        print('Usage: python main_create_partial_layers.py <rank> <procs> <year> <layer_index>')
        return

    if procs == 1:
        raise Exception(f'Use main_create_partial_layer.py with procs > 1.')

    if rank >= procs:
        raise Exception(f'{rank=} >= {procs=}')

    from settings import layer_specs
    from settings import output_settings

    path_out    = os.path.join(output_settings['path'], str(year))
    fn_filelist = os.path.join(path_out, f'files_{year}.pckl')

    with open(fn_filelist, 'rb') as fin:
        file_list = pickle.load(fin)

    layer_spec = layer_specs[year]

    fn_index = os.path.join(path_out, f'index_{year}.pckl')
    with open(fn_index, 'rb') as fin:
        index = pickle.load(fin)

    extract_features(rank, procs, file_list, layer_spec['join_attribute_name'], index, layer_spec['layers'][layer_pos], path_out)


if __name__ == '__main__':
    main()
