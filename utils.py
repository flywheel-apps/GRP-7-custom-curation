import os
import sys


def load_converter(converter):
    """Load converter from the file, return the module
    """
    if os.path.sep in converter or os.path.lexists(converter):
        converter_file = os.path.realpath(converter)
        path, fname = os.path.split(converter_file)
        try:
            old_syspath = sys.path[:]
            sys.path.append(path)
            mod = __import__(fname.split('.')[0])
            mod.filename = converter_file
        finally:
            sys.path = old_syspath
    else:
        mod = None

    return mod

