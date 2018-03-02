# yang2cpp
Script to conver [YANG models](https://tools.ietf.org/html/rfc6020) to C++ Class.

## Requirements
 - [Python 2.7.6](https://www.python.org/)
 - [Pyang](https://github.com/mbj4668/pyang)

## What's alerady done
 - Module parsing
 - Container parsing
 - Single-key list parsing
 - Augment parsing
 - Leaf parsing

## TODO List
Please refer to [Issues](https://github.com/redivo/yang2cpp/issues)

## How to use
 ```
# ./yang2cpp.py --help
usage: yang2cpp.py [-h] [-o PREFIX] [-d DIR] [-p PATH1:PATH2] input

Convert a given YANG model in a C++ classes model.

positional arguments:
  input                 YANG file to be converted.

optional arguments:
  -h, --help            show this help message and exit
  -o PREFIX, --output PREFIX
                        Output prefix. Two files (a .h and a .cc) will be
                        created based on this prefix. The default is the YANG
                        module name.
  -d DIR, --output-directory DIR
                        Path to directory where the output files will be
                        placed in. The default is the current directory.
  -p PATH1:PATH2, --path PATH1:PATH2
                        path is a colon (:) separated list of directories to
                        search for import
```
