'''
Author: Víctor Ruiz Gómez
Description:
Setup script to install pylib3d-mec-ginac library.
'''

# Import statements
from distutils.core import setup
from distutils.extension import Extension
from os import listdir
from os.path import dirname, join
from functools import reduce, partial



######## PACKAGE DESCRIPTION ########

# Name of this library
NAME = 'pylib3d-mec-ginac'

# Version of the library
VERSION = '1.0.0'

# Author details
AUTHOR = 'Victor Ruiz Gomez'
AUTHOR_EMAIL = 'victorruizgomezdev@gmail.com'


root_dir = dirname(__file__)

# Library description
DESCRIPTION = 'Python extension for the library lib3d_mec_ginac'

with open(join(root_dir, 'README.md'), 'r') as f:
    LONG_DESCRIPTION = f.read()

# License
with open(join(root_dir, 'LICENSE.txt'), 'r') as f:
    LICENSE = f.read()

# Classifiers
CLASSIFIERS = [
    'Development Status :: 1 - Planning',
    'Framework :: Buildout :: Extension',
    'Programming Language :: Cython',
    'Programming Language :: C++'
]

# Keywords
KEYWORDS = [
    'cython', 'c++', 'bindings',
    'extension', 'wrapper'
]


######## PYTHON PACKAGE SETUP ########

# Name of the library inside python
PACKAGE = 'lib3d_mec_ginac'

# Diretory where source files of the package can be found
PACKAGE_DIR = 'src'



######## C EXTENSION CONFIGURATION VARIABLES ########

# Directory that contains all lib3d-mec-ginac headers
LIB3D_MEC_GINAC_INCLUDE_DIR = '../lib3d-mec-ginac/include/lib_3d_mec_ginac'

# Directory where lib3d-mec-ginac libraries are located
LIB3D_MEC_GINAC_LIBRARY_DIR = '../lib3d-mec-ginac/lib'

# Directories containing header files used to build the extensions
INCLUDE_DIRS = [
    '/usr/local/include',
    '/usr/include',
    LIB3D_MEC_GINAC_INCLUDE_DIR
]

# Directories to search for libraries at link time
LIBRARY_DIRS = [
    LIB3D_MEC_GINAC_LIBRARY_DIR,
    '/usr/local/lib'
]

# Directories to search for dynamic libraries at runtime
RUNTIME_LIBRARY_DIRS = [
    LIB3D_MEC_GINAC_LIBRARY_DIR
]

# Name of the libraries for the extensions to link against
LIBRARIES = [
    'cln',
    'ginac',
    '_3d_mec_ginac-2.0'
]


# This list holds all the extensions defined by this library
EXTENSIONS = [
    Extension(
        name=f'{PACKAGE}_ext',
        sources=['src/main.pyx', 'src/extern.cpp'],
        include_dirs=INCLUDE_DIRS,
        library_dirs=LIBRARY_DIRS,
        runtime_library_dirs=RUNTIME_LIBRARY_DIRS,
        libraries=LIBRARIES,
        language='c++',
        extra_compile_args=['-w']
    )
]



######## INSTALLATION PROCEDURE ########

if __name__ == '__main__':
    ## Import statements
    try:
        from Cython.Build import cythonize
        from source import parse_source
    except ImportError as e:
        # Generate error message if missing dependencies
        print(f'Failed to import "{e.name}" module')
        print('Make sure to install dependencies with "pip install -r requirements.txt"')
        exit(-1)


    ## Parse .pyx modules and merge them into one single source

    with open('src/main.pyx', 'w') as f_out: # All source code will be merged to this file
        # Insert a header comment in the output file
        f_out.write('\n'.join([
            "'"*3,
            f'Author: {AUTHOR}',
            'Description: This is an autogenerated source file made by the setup.py script.',
            'It contains all Cython definitions (methods & classes) of this library extension in order to interact with lib3d_mec_ginac',
            f'Version : {VERSION}',
            "'"*3
        ]))

        # Parse each .pyx file
        for filename in listdir('src'):
            if not filename.endswith('.pyx') or filename.startswith('main'):
                continue

            print(f'Parsing {filename}')
            with open(join('src', filename), 'r') as f_in:
                f_out.write(parse_source(f_in.read()))
                f_out.write('\n')

    print(f"Generated src/main.pyx file")



    ## Invoke distutils setup
    setup(
        name=NAME,
        version=VERSION,

        author=AUTHOR,
        author_email=AUTHOR_EMAIL,

        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        license=LICENSE,

        keywords=KEYWORDS,
        classifiers=CLASSIFIERS,

        packages=[PACKAGE],
        package_dir={PACKAGE:PACKAGE_DIR},
        ext_modules=cythonize(EXTENSIONS,
            compiler_directives={'language_level': 3},
            nthreads=2, force=True),
    )
