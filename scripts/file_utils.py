import fnmatch
import os


# https://stackoverflow.com/questions/2186525/use-a-glob-to-find-files-recursively-in-python
def search_file(search_file, search_path):
    for root, dirnames, filenames in os.walk(search_path):
        for filename in fnmatch.filter(filenames, search_file):
            return os.path.join(root, filename)
