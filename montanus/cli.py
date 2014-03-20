# coding=utf8

"""cli interface"""

import logging
from os.path import split
from docopt import docopt

from .logger import logger
from . import version
from .config import config
from .parser import parser

def task(task_func):
    def wrapper(*args, **kwargs):
        if task_func.__doc__:
            logger.info(task_func.__doc__)
        return task_func(*args, **kwargs)
    return wrapper


@task
def build():
    """"""
    parser.process(config.default['base_dir'])
    logger.success("Build Done")


def main():
    """Usage:
  montanus BASE_DIR

Arguments:
    BASE_DIR     Base directory

Options:
  -h --help              Show this help message
  -v --version           Show version
  --with-protocol=<p>    Set protocol [Default: http]
  --with-domain=<d>      Set CDN domain
  --md5-len=<l>          Set MD5 Length [Default: 10]
  --conf=<f>             Set config file path
  """
    arguments = docopt(main.__doc__, version='montanus version: ' + version)
    # Set logger's level to info
    logger.setLevel(logging.INFO)

    base_dir = arguments.get('BASE_DIR')
    config.default['base_dir'] = base_dir

    conf_file = arguments.get('--conf')
    if conf_file is not None:
        (config.filepath, config.filename) = split(conf_file)
        conf_config = config.read()

        for (k, v) in conf_config.items():
            if v is not None:
                config.default[k] = v

    command_config = {
        'protocol': arguments.get('--with-protocol'),
        'domain': arguments.get('--with-domain'),
        'md5_len': arguments.get('--md5-len')
    }

    for (k, v) in command_config.items():
        if v is not None:
            config.default[k] = v

    print config.default


if __name__ == '__main__':
    main()
