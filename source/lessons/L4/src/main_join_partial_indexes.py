import os
import sys
import pickle

from utils import add_to_dict


def main():
    try:
        procs = int(sys.argv[1])
        year  = int(sys.argv[2])
    except Exception:
        print('Usage: python main_join_partial_indexes.py <procs> <year>')
        return

    from settings import output_settings

    path_out = os.path.join(output_settings['path'], f'{year}')
    fn_index = os.path.join(path_out, f'index_{year}.pckl')

    index = dict()
    for rank in range(procs):
        fn_index_partial = f'{fn_index}.{rank}_{procs}'
        with open(fn_index_partial, 'rb') as fin:
            occ = pickle.load(fin)
            add_to_dict(index, occ)

    with open(fn_index, 'wb') as fout:
        pickle.dump(index, fout)


if __name__ == '__main__':
    main()
