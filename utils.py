import glob
import importlib
import inspect
import os.path
import pickle


def longest(seq):
    """Find the longuest sequence values (different from 0) in a list"""
    best = (None, 0)
    curr = (None, 0)  # the value of the sequence, and its size
    for v in seq:
        if not v:
            curr = (None, 0)
        else:
            count = (v == curr[0]) * curr[1] + 1
            curr = (v, count)

        if curr[1] > best[1]:
            best = curr
    return best


def loadClasses(where: str, suffix: str, basenames=[], recursive=True) -> list:
    """
    Dynamically loads the classes that are described by the `where` path,
    that has the class suffix name `suffix` and that maybe only limited to the
    name in `basenames`. Abstract classes are not returned.
    """
    extension = ".py"
    result = []
    filenames = glob.glob(where)
    for filename in filenames:
        if '__' in filename:
            continue

        noExtension = filename[:-len(extension)]
        basename = os.path.basename(noExtension)
        if basenames and basename not in basenames:
            continue

        moduleName = noExtension.replace("\\", ".")
        mod = importlib.import_module(moduleName)
        for name, klass in vars(mod).items():
            if name.endswith(suffix) and klass.__module__ == mod.__name__ and \
                    not inspect.isabstract(klass):
                result.append(klass)
    return result


def loadInstance(filename):
    """Loads an object saved as pickle file"""
    with open(filename, 'rb') as fp:
        return pickle.load(fp)
