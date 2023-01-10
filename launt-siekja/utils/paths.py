import os
import sys

def get_root_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__),"../.."))

def resolve_path(*path):
    return os.path.join(get_root_dir(), *path)
