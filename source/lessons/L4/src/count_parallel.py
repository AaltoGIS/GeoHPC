#import os
#import pickle
#
#from utils import add_to_dict
#from count_occurences import count_from_zip
#
#
#def count_from_zipfiles(rank, procs, file_list, join_attribute_name):
#    occurences = dict()
#
#    for i, fn in enumerate(file_list):
#        if i % procs == rank:
#            occ = count_from_zip(fn, join_attribute_name)
#            add_to_dict(occurences, occ)
#
#    return occurences
#
#
#def create_occurence_index(rank, procs, file_list, join_attribute_name, fn_pickle):
#    if os.path.isfile(fn_pickle):
#        print(f'File "{fn_pickle}" already exists.')
#    else:
#        print(f'Counting the occurences...')
#        occurences = count_from_zipfiles(rank, procs, file_list, join_attribute_name)
#        with open(fn_pickle, 'wb') as fout:
#            pickle.dump(occurences, fout)
#        print('The attribute occurence counting finished.')
