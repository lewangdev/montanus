# coding=utf8

"""cli interface"""

import logging
import sys
from os.path import dirname
from .logger import logger
from . import version
from .generator import generator
from docopt import docopt

def task(task_func):
    def wrapper(*args, **kwargs):
        if task_func.__doc__:
            logger.info(task_func.__doc__)
        return task_func(*args, **kwargs)
    return wrapper

@task
def build():
    """"""
    lib_dir = dirname(__file__)  # this library's directory
    res = join(lib_dir, "resources")
    logger.success("Build Done")
    logger.info("Please edit config.json to meet our needs")
    logger.info("Run 'make clean' to remove built static files")


@task
def clean():
    """rm -rf static files"""
    paths = [
    ]

    cmd = ["rm", "-rf"] + paths
    call(cmd)
    logger.success("clean done")


def main():
    """Usage:
  montanus (build|clean)

Options:
  -h --help     show this help message
  -v --version  show version
  --watch       watch source files for changes

Commands:
  build         build static files to CDN version
  clean         remove files built by montanus
  """

    arguments = docopt(main.__doc__, version='montanus version: ' + version)
    # set logger's level to info
    logger.setLevel(logging.INFO)

    if arguments["build"]:
        build()
    elif arguments["clean"]:
        clean()
    else:
        exit(main.__doc__)
