import os
import sys
import pickle

from utils        import list_zipfiles
from count        import count_from_zipfiles
from create_layer import create_merged_layer


def main():
    try:
        year     = int(sys.argv[1])
    except Exception:
        print('Usage: python main.py <year>')
        return

    from settings import layer_specs
    from settings import output_settings

    path_out    = os.path.join(output_settings['path'], f'{year}')
    fn_filelist = os.path.join(path_out, f'files_{year}.pckl')

    #
    # Make sure that the output path exists.
    #
    if not os.path.isdir(path_out):
        os.makedirs(path_out, exist_ok=True)

    #
    # ------ Create the list only if the file does not exists. If created, save it.
    #
    path_tiles = layer_specs[year]['path_tiles']
    file_list  = list_zipfiles(path_tiles)
    
    
    if not os.path.exists(fn_filelist):
        
       path_tiles = layer_specs[year]['path_tiles']
       
       os.makedirs(path_out, exist_ok=True)
       
       file_list = list_zipfiles(path_tiles)
    
       with open(fn_filelist, 'wb') as fout:
           pickle.dump(file_list, fout) # fns, fout
           
    else:
       with open(fn_filelist, 'rb') as fin:           
           file_list = pickle.load(fin)

    #
    # ------- Create the index only if the file does not exists. If created, save it.
    #
    index = count_from_zipfiles(file_list, layer_specs[year]['join_attribute_name'])
    
    
    fn_index = os.path.join(path_out, f'index_{year}.pckl')
    
    if not os.path.exists(fn_index):
        
       index = count_from_zipfiles(file_list, layer_specs[year]['join_attribute_name'])
       
       with open(fn_index, 'wb') as fout:
           pickle.dump(index, fout)
           
    else:
       with open(fn_index, 'rb') as fin:
           index = pickle.load(fin)

    #
    # Loop over all the layer definitions for the given year
    #
    for layer_spec in layer_specs[year]['layers'].values():

        create_merged_layer(file_list, layer_specs[year]['join_attribute_name'], index, layer_spec, path_out)


if __name__ == '__main__':
    main()
