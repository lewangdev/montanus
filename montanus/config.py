#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""Configuration manager, config is in json"""

import toml
from os.path import join
from os.path import exists


class Config(object):
    """Configuration manager"""

    filename = "config.toml"
    filepath = join(".", filename)

def read(self):
    """Read and parse config, return a dict"""

    if not exists(self.filepath):
        # if not exists, touch one
        open(self.filepath, "a").close()

    with open("conf.toml") as conffile:
        config = toml.loads(conffile.read())

    return config

config = Config()  # build a config instance

