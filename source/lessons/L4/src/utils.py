import os


def is_zipfile(filename):
    return filename.lower().endswith('.zip')


def list_zipfiles(path):
    #
    # Filenames with full path.
    #
    fns = []
    for root, _, filenames in os.walk(path):
        for filename in filenames:
            if is_zipfile(filename):
                
                fns.append(os.path.join(root, filename))

    return fns


def add_to_dict(target, source):
    """
    A helper function to "add" the source dictionary into the target dictionary.
    Both dictionaries contains keys with counts.

    Example:

        d1 = {'a': 1, 'b': 1}

        d2 = {'b': 1, 'c': 1}

        add_to_dict(d1, d2)

        print(d1)
        >> {'a': 1', 'b': 2, 'c': 1}

    """
    for key, value in source.items():
        if key in target:
            target[key] += value
        else:
            target[key] = value
