#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Configuration manager, config is in json"""

import toml
import logging
from logger import logger
from os.path import join
from os.path import exists



class Config:
    """Configuration manager"""

    filename = "config.toml"
    filepath = join(".", filename)


    def read(self, path=None):
        """Read and parse config, return a dict"""
        if path is None:
            path = self.filepath

        if not exists(path):
            return None

        with open(path) as conffile:
            config = toml.loads(conffile.read())
            logger.debug(config)
            return config


config = Config()  # build a config instance

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    config.read()
