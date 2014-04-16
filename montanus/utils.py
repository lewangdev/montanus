#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import errno
import hashlib
import traceback

def unique_name(path, length, cat):
    """
    Rename a file according to the md5 of its content
    """
    method = hashlib.md5()
    try:
        fh = open(path, 'rb')
        method.update(fh.read())
        fh.close()
        hex_str = method.hexdigest()
        (file_name, ext_name) = os.path.splitext(path)
        return "".join([file_name, cat, hex_str[0:length], ext_name])
    except Exception:
        traceback.print_exc()
        return None

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

