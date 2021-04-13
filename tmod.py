#! /usr/bin/env python3

# -*- coding: utf-8 -*-
version = '2021-04-13'

import os.path
import sys


# File I/O /////////////////////////////////////////
def get_resource_path(rel_path):
    dir_of_py_file = os.path.dirname(sys.argv[0])
    rel_path_to_resource = os.path.join(dir_of_py_file, rel_path)
    abs_path_to_resource = os.path.abspath(rel_path_to_resource)
    return abs_path_to_resource


def save_file_list(file_,variable,type_='relative'):
    home = os.path.expanduser("~")
    if type_ == 'Home':
        with open('{}/{}'.format(home,file_), 'w') as output:
            output.write(''.join(variable))
    else:
        with open(get_resource_path(file_), 'w') as output:
            output.write(''.join(variable))


    
