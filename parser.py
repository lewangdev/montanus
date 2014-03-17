# coding=utf8

#import config
from logger import logger
import utils

import re
import logging
import os

class Parser(object):
    """
    """
    CHARSET = 'utf8'
    BINARY_FILE_EXTS = [
            'png', 'bmp', 'gif',  'ico',
            'jfif', 'jpe', 'jpeg', 'jpg'
            ]


    HTML_REGEX = '(<link.*href|<script.*src|<img.*src)="(.*?)"'
    CSS_REGEX = '(@import.*url|backgroud.*url|background-image.*url).*\(["\']*(.*?)["\']*\)'
    RESOURCE_MAP = {}
    BASE_PATH = '/Users/wangle/Workspace/gitlab/proto/src/main/webapp'

    def __init__(self):
        pass

    def __css_parse(self, path):
        """
        Parse css files
        """
        content = open(path).read().decode(self.CHARSET)
        pattern = re.compile(self.CSS_REGEX, re.IGNORECASE)
        res_list = pattern.findall(content)
        for item in res_list:
            logger.debug("In css parser %s" % item[1])
            #TODO Refactor
            #[ ] Parse all files found in res_list
            #[ ] Need refactor and merge code
            if item[1].endswith('.png'):
                (parent_path, file_name) = os.path.split(path)
                relative_parent_path_len = len(parent_path) - len(self.BASE_PATH)
                relative_parent_path = parent_path[0-relative_parent_path_len:]
                logger.debug("%s %s %s" % (parent_path, file_name, relative_parent_path))
                if item[1].startswith('.') or item[1].startswith('..'):
                    abs_path = (parent_path + '%s%s') % ('/', item[1])
                elif item[1].startswith("/"):
                    abs_path = self.BASE_PATH + item[1]
                logger.debug(abs_path)
                new_file_name = self.__binary_parse(abs_path)
                # TODO MAPPING
                #[ ] Gether new file name to a map for replace old name
            elif item[1].endswith('css'):
                (parent_path, file_name) = os.path.split(path)
                relative_parent_path_len = len(parent_path) - len(self.BASE_PATH)
                relative_parent_path = parent_path[0-relative_parent_path_len:]
                logger.debug("%s %s %s" % (parent_path, file_name, relative_parent_path))
                if item[1].startswith('.') or item[1].startswith('..'):
                    abs_path = (parent_path + '%s%s') % ('/', item[1])
                elif item[1].startswith("/"):
                    abs_path = self.BASE_PATH + item[1]
                logger.debug(abs_path)
                self.__css_parse(abs_path)


        #TODO Replace
        #[ ] Replace all files with new name in RESOURCE_MAP
        for item in res_list:
            pass

    def __js_parse(self, path):
        """
        Parse js files
        """
        content = open(path).read().decode(self.CHARSET)

    def __binary_parse(self, path):
        new_abs_path = utils.unique_name(path, 10, '_')

        (parent_path, new_file_name) = os.path.split(new_abs_path)
        logger.success(new_file_name)

        #TODO
        #[x] Rename
        #os.rename(abs_path, new_abs_path)
        return new_file_name

    def parse(self, path):
        """
        Find links and img in html. This is the entrance.
        """
        logger.debug(path)
        content = open(path).read().decode(self.CHARSET)
        pattern = re.compile(self.HTML_REGEX, re.IGNORECASE)
        res_list = pattern.findall(content)

        (parent_path, file_name) = os.path.split(path)
        relative_parent_path_len = len(parent_path) - len(self.BASE_PATH)
        relative_parent_path = parent_path[0-relative_parent_path_len:]
        logger.debug("%s %s %s" % (parent_path, file_name, relative_parent_path))

        #TODO
        #[ ] Dive into css,js... files
        #[x] Get md5 of image files

        for item in res_list:
            logger.debug(item[1])
            if item[1].endswith('.css'):
                if item[1].startswith('.') or item[1].startswith('..'):
                    abs_path = (parent_path + '%s%s') % ('/', item[1])
                elif item[1].startswith("/"):
                    abs_path = self.BASE_PATH + item[1]
                logger.debug(abs_path)
                self.__css_parse(abs_path)
            elif item[1].endswith('.js'):
                pass
            elif item[1].endswith('.png'):
                pass
                #abs_path = parent_path % ('/' if item[1].startswith('.') else '', item[1])
                #self.__binary_parse(abs_path)


parser = Parser()  # build a runtime parser

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    path = '/Users/wangle/Workspace/gitlab/proto/src/main/webapp/general/login.jsp'
    parser.parse(path)
