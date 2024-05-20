import os
import sys
import pickle

from count import count_from_zipfiles


def main():
    try:
        rank  = int(sys.argv[1])
        procs = int(sys.argv[2])
        year  = int(sys.argv[3])
    except Exception:
        print('Usage: python main_create_partial_index.py <rank> <procs> <year>')
        return

    if rank >= procs:
        raise Exception(f'{rank=} >= {procs=}')

    from settings import layer_specs
    from settings import output_settings

    path_out    = os.path.join(output_settings['path'], str(year))
    fn_filelist = os.path.join(path_out, f'files_{year}.pckl')

    with open(fn_filelist, 'rb') as fin:
        file_list = pickle.load(fin)

    layer_spec = layer_specs[year]

    fn_index    = os.path.join(path_out, f'index_{year}.pckl')
    my_fn_index = f'{fn_index}.{rank}_{procs}'

    if not os.path.exists(my_fn_index):
        index = count_from_zipfiles(
            file_list[rank::procs],
            layer_specs[year]['join_attribute_name'])
        with open(my_fn_index, 'wb') as fout:
            pickle.dump(index, fout)


if __name__ == '__main__':
    main()
