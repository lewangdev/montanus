#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""Montanus.

Usage:
  montanus.py <templates_path> [--with-static-files-path=<p> | --with-protocol=<p> | --with-domains=<l> | --with-md5-len=<l> | --with-md5-concat-by=<c> | --with-conf=<f> | -d]
  montanus.py (-h | --help)
  montanus.py (-v | --version)

Options:
 -h --help                          Show this help message
 -v --version                       Show version
 -d --delete                        Delete all sources
 --with-static-files-path=<p>       Set static file path. If not set, the value will be the same as template_path
 --with-protocol=<p>                Set protocol [Default: http]
 --with-domains=<d>                 Set CDN domains[Default: ]
 --with-md5-len=<l>                 Set MD5 Length [Default: 10]
 --with-md5-concat-by=<c>           Set MD5 concatenator [Default: -]
 --with-conf=<f>                    Set config file path
 """

import logging
from docopt import docopt
from logger import logger
from config import config
from processor import processor
from utils import DictWrapper

__version__ = '0.0.1'


def main():
    """Start to build the package to CDN requirement"""
    processor.custom_config = parse_arguments()
    processor.process()
    logger.info(processor.statistics)
    logger.info(processor.custom_config)

def parse_arguments():
    """Get all arguments as a dict object"""
    custom_config = config.read()
    arguments = docopt(__doc__, version='Montanus %s' % __version__)
    logger.debug(custom_config)
    conf_file = arguments.get('--with-conf')
    if conf_file is not None:
        conf_config = config.read(conf_file)

        for (k, v) in conf_config.items():
            if v is not None:
                custom_config[k] = v

    logger.debug(arguments)
    command_config = {
        'templates_path': arguments.get('<templates_path>'),
        'static_files_path': arguments.get('--with-static-files-path') \
            if arguments.get('-with-static-files-path') is not None \
            else arguments.get('<templates_path>'),
        'delete_source': arguments.get('--delete'),
        'protocol': arguments.get('--with-protocol'),
        'domains': arguments.get('--with-domains').split(',') \
            if arguments.get('--with-domains') is not None \
            else None,
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
    logger.setLevel(logging.DEBUG)
    main()
