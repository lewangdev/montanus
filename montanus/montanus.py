#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""Montanus.

Usage:
  montanus.py <root_path> [--with-protocol=<p> | --with-domains=<l>i | --with-md5-len=<l> | --with-conf=<f>]
  montanus.py (-h | --help)
  montanus.py (-v | --version)

Options:
 -h --help              Show this help message
 -v --version           Show version
 --with-protocol=<p>    Set protocol [Default: http]
 --with-domains=<d>     Set CDN domains [Default: s0.ga.1txdn.com,s1.ga.1txdn.com]
 --with-md5-len=<l>     Set MD5 Length [Default: 10]
 --with-conf=<f>        Set config file path
 """

import logging
from os.path import split
from docopt import docopt

from logger import logger
from config import config
from parser import parser

__version__ = '0.0.1'

def build():
    """"""
    parser.BASE_PATH = config.default['base_dir']
    parser.URI_PREFIX = "%s://%s" % (config.default['protocol'], config.default['domain'])
    parser.process()
    logger.success("Build Done")


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


def parse_arguments():
    custom_config = config.read()
    arguments = docopt(__doc__, version='Montanus %s' % __version__)

    conf_file = arguments.get('--with-conf')
    if conf_file is not None:
        (config.filepath, config.filename) = split(conf_file)
        conf_config = config.read(conf_file)

        for (k, v) in conf_config.items():
            if v is not None:
                custom_config[k] = v

    command_config = {
        'root_path': arguments.get('<root_path>'),
        'protocol': arguments.get('--with-protocol'),
        'domains': arguments.get('--with-domains').split(','),
        'md5_len': arguments.get('--md5-len')
    }
    logger.debug(command_config)

    for (k, v) in command_config.items():
        if v is not None:
            custom_config[k] = v

    logger.debug(custom_config)
    return DictWrapper(custom_config)


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    logger.debug(parse_arguments())
