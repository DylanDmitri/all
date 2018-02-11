base = '/Users/dg/Downloads/hw6'

import os

# newtext = open('jack_tests.js', 'r').read()
newhtml = open('htmlfile', 'r').read()

def foreach(f):
    for folder_name in os.listdir(base):
        if folder_name.startswith('.') or folder_name == 'aagh':
            continue
        tests_folder = os.path.join(base,folder_name,'unit_tests')

        f(tests_folder, folder_name)

# BUILD MONGO BOY
newtext = []

# TARGET = 'test_transit.js'
TARGET = 'test_undirected_graph.js'

def build_mongo_boy(tests_folder, folder_name):
    for file_name in os.listdir(tests_folder):
        if file_name == TARGET:
            globals()['newtext'].append(open(os.path.join(tests_folder,file_name),'r').read())

def purge(tests_folder, folder_name):
    for file_name in os.listdir(tests_folder):
        if file_name.startswith('test_'):
            os.remove(os.path.join(tests_folder,file_name))

def place_new_files(tests_folder, folder_name):
    open(os.path.join(tests_folder, TARGET), 'w').write(newtext)

def write_symlinks(tests_folder, folder_name):
    hf = os.path.join(tests_folder,'unit_tests.html')
    os.symlink(hf, os.path.join(tests_folder, '../../aagh', folder_name))

# ----------

# foreach(build_mongo_boy)
newtext = '\n'.join(newtext)
#
# foreach(purge)
# foreach(place_new_files)

foreach(write_symlinks)

