# coding=utf8

"""Configuration manager, config is in json"""

from exceptions import ConfigSyntaxError

from os.path import join
from os.path import exists
from json import loads


class Config(object):
    """Configuration manager"""

    filename = "config.json"
    filepath = join(".", filename)
    # default configuration
    default = {
        'project': {
            'charset': 'utf8'
            'md5_length': 10,
            'md5_cat_str': '_'
        }
    }

    def read(self):
        """Read and parse config, return a dict"""

        if not exists(self.filepath):
            # if not exists, touch one
            open(self.filepath, "a").close()

        content = open(self.filepath).read().decode(charset)
        try:
            config = loads(content)
        except TypeError:
            raise ConfigSyntaxError

        return config

config = Config()  # build a config instance
