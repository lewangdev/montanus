#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import errno
import hashlib

def unique_name(path, length, cat):
    """
    Rename a file according to the md5 of its content
    """
    method = hashlib.md5()
    with open(path, 'rb') as fh:
        method.update(fh.read())
        hex_str = method.hexdigest()
        (file_name, ext_name) = os.path.splitext(path)
        return "".join([file_name, cat, hex_str[0:length], ext_name])

def mkdir_p(path):
    """mkdir -p
    Note: comes from stackoverflow"""
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def join(*p):
    """return normpath version of path.join"""
    return os.path.normpath(os.path.join(*p))

class DictWrapper(dict):
    """Dict Wrapper"""

    def __init__(self, d):
        self.dict = d
        for k, v in d.items():
            setattr(self, k, v)

    def __getattr__(self, i):
        if i in self:
            return self[i]
        else:
            return None

    def __str__(self):
        return self.dict.__str__()
