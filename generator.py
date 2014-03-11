# coding=utf8

""""""

import signals
from .config import config
from .exceptions import *
from .logger import logger, logging
from .utils import unique_name

import sys
from os.path import exists
from datetime import datetime


class Generator(object):

    def __init__(self):
        """init attributes to store runtime data"""
        # initialize them the default value.
        self.reset()
        # register signals
        self.register_signals()

    def reset(self):

    def register_signals(self):
        """Register all signals in this process"""

    def step(step_method):
        """decorator to wrap each step method"""
        def wrapper(self, *args, **kwargs):
            logger.info(step_method.__doc__)
            return step_method(self, *args, **kwargs)
        return wrapper

    @step
    def initialize(self):
        # read config to update the default
        try:
            conf = config.read()
        except ConfigSyntaxError as e:
            logger.error(e.__doc__)
            sys.exit(1)


    # make alias to initialize
    generate = initialize

    def re_generate(self):
        pass

    @step
    def parse_atom(self, sender):
        pass

generator = Generator()
