# coding=utf8

import os
import errno
import hashlib
import traceback

def unique_name(path, length, cat):
    """
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


class Color(object):
    """
     utility to return ansi colored text
     usage::

         >>> colored("text","red")
        '\x1b[31mtext\x1b[0m'

    """
    colors = {
        'black': 30,
        'red': 31,
        'green': 32,
        'yellow': 33,
        'blue': 34,
        'magenta': 35,
        'cyan': 36,
        'white': 37,
        'bgred': 41,
        'bggrey': 100
    }

    prefix = '\033['

    suffix = '\033[0m'

    def colored(self, text, color=None):
        if color not in self.colors:
            color = 'white'

        clr = self.colors[color]
        return (self.prefix+'%dm%s'+self.suffix) % (clr, text)

colored = Color().colored
