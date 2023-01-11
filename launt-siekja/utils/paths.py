import os
import sys

def get_root_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__),"../.."))

def resolve_path(*path):
    return os.path.join(get_root_dir(), *path)

def create_path_if_not_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)
