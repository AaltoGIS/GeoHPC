import os
import sys
import pickle

from utils import list_zipfiles


def main():
    try:
        year = int(sys.argv[1])
    except Exception:
        print('Usage: python main_list_files.py <year>')
        return

    from settings import layer_specs
    from settings import output_settings

    path_out    = os.path.join(output_settings['path'], f'{year}')
    fn_filelist = os.path.join(path_out, f'files_{year}.pckl')

    if not os.path.exists(fn_filelist):
        os.makedirs(path_out, exist_ok=True)
        path_tiles = layer_specs[year]['path_tiles']
        file_list = list_zipfiles(path_tiles)

        with open(fn_filelist, 'wb') as fout:
            pickle.dump(file_list, fout)


if __name__ == '__main__':
    main()
