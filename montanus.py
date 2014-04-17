#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""Montanus.

Usage:
  montanus.py <templates_path> [--with-static-files-path=<p> | --with-protocol=<p> | --with-domains=<l> | --with-md5-len=<l> | --with-md5-concat-by=<c> | --with-conf=<f>]
  montanus.py (-h | --help)
  montanus.py (-v | --version)

Options:
 -h --help                          Show this help message
 -v --version                       Show version
 --with-static-files-path=<p>       Set static file path. If not set, the value will be the same as template_path
 --with-protocol=<p>                Set protocol [Default: http]
 --with-domains=<d>                 Set CDN domains [Default: s0.ga.1txdn.com,s1.ga.1txdn.com]
 --with-md5-len=<l>                 Set MD5 Length [Default: 10]
 --with-md5-concat-by=<c>           Set MD5 concatenator [Default: -]
 --with-conf=<f>                    Set config file path
 """

import logging
from os.path import split
from docopt import docopt

from logger import logger
from config import config
from parser import parser
from utils import DictWrapper

__version__ = '0.0.1'


def build():
    """Start to build the package to CDN requirement"""
    parser.custom_config = parse_arguments()
    parser.process()
    logger.info(parser.statistics)

def parse_arguments():
    """Get all arguments as a dict object"""
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
        'templates_path': arguments.get('<templates_path>'),
        'static_files_path': arguments.get('--with-static-files-path') \
            if arguments.get('-with-static-files-path') is not None \
            else arguments.get('<templates_path>'),
        'protocol': arguments.get('--with-protocol'),
        'domains': arguments.get('--with-domains').split(','),
        'md5_len': int(arguments.get('--with-md5-len')),
        'md5_concat_by': arguments.get('--with-md5-concat-by')
    }
    logger.debug(command_config)

    for (k, v) in command_config.items():
        if v is not None:
            custom_config[k] = v

    logger.debug(custom_config)
    return DictWrapper(custom_config)


if __name__ == '__main__':
    logger.setLevel(logging.INFO)
    build()
