# -*- coding: utf-8 -*-
#This file contains functions for background tasks
from os.path import join, exists, dirname
import os
import re
import shutil
import sys


def copy_folder(source_dir, target_dir, merge=True, overwrite=True):
    """
    Copy source folder to target. 
    If merge=False, deletes and creates target folder.
    If overwrite=False, exising files will remain untouched.
    By default, merges target dir to source with overwriting existing files  
    """
    if not merge and exists(target_dir):
        shutil.rmtree(target_dir)
        os.mkdir(target_dir)
    if not exists(target_dir):
        os.makedirs(target_dir)

    for root, dirs, files in os.walk(source_dir):
        relative_path = root.replace(source_dir, '')  # e.g. relative_path = 'templates'
        relative_path = relative_path.lstrip(os.path.sep)
        for file in files:
            if not overwrite and (exists(join(target_dir, relative_path, file))):
                pass
            else:
                shutil.copy(
                    join(root, file),
                    join(target_dir, relative_path)
                )

        for dir in dirs:
            if not exists(join(target_dir, relative_path, dir)):
                os.mkdir(join(target_dir, relative_path, dir))

def write_file(path, content, overwrite=False):
    target_dir = dirname(path)
    if not exists(target_dir):
        os.makedirs(target_dir)
    if not overwrite and exists(path):
        fileobj = open(path, 'w+')
    else:
        fileobj = open(path, 'w')
    fileobj.write(content)
    fileobj.close
