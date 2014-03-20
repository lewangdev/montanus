# coding=utf8

"""cli interface"""

import logging
from os.path import dirname
from docopt import docopt

from .logger import logger
from . import version
from .utils import join

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
    logger.success("clean done")


def main():
    """Usage:
  montanus (build|clean)

Options:
  -h --help     show this help message
  -v --version  show version

Command:
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

if __name__ == '__main__':
    main()
