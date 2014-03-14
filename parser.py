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
    IMAGE_FILE_EXTS = [
            'svg', 'tif', 'tiff', 'wbmp',
            'png', 'bmp', 'fax', 'gif',
            'ico', 'jfif', 'jpe', 'jpeg',
            'jpg', 'woff', 'cur', 'webp',
            'swf', 'ttf', 'eot'
            ]

    TEXT_FILE_EXTS = [
            'css', 'tpl', 'js', 'php',
            'txt', 'json', 'xml', 'htm',
            'text', 'xhtml', 'html', 'md',
            'coffee', 'less', 'sass', 'jsp'
            ]

    #HTML_REGEX = '<link.*href="(.*?)"|<script.*src="(.*?)"|<img.*src="(.*?)"'
    HTML_REGEX = '(<link.*href|<script.*src|<img.*src)="(.*?)"'
    CSS_REGEX = ''

    def __init__(self):
        pass

    def __css_parse(self, path):
        """
        Parse css files
        """
        content = open(path).read().decode(self.CHARSET)

    def __js_parse(self, path):
        """
        Parse js files
        """
        content = open(path).read().decode(self.CHARSET)
    def __binary_parse(self, path):
        base_path = '/Users/wangle/Workspace/gitlab/proto/src/main/webapp%s%s'
        abs_path = base_path % ('/' if path.startswith('.') else '', path)
        logger.info(abs_path)
        new_abs_path = utils.unique_name(abs_path, 10, '_')
        logger.debug(new_abs_path)

        #TODO [x] Rename
        os.rename(abs_path, new_abs_path)



    def parse(self, path):
        """
        Find links and img in html
        """
        logger.debug(path)
        content = open(path).read().decode(self.CHARSET)
        pattern = re.compile(self.HTML_REGEX, re.IGNORECASE)
        res_list = pattern.findall(content)

        #TODO
        #[ ] Dive into css,js... files
        #[x] Get md5 of image files

        for item in res_list:
            logger.debug(item[1])
            if item[1].endswith('.css'):
                logger.warning("CSS FOUND")
            elif item[1].endswith('.js'):
                logger.warning('JS FOUND')
            elif item[1].endswith('.png'):
                logger.warning('PNG Found')
                self.__binary_parse(item[1])


parser = Parser()  # build a runtime parser

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    path = '/Users/wangle/Workspace/gitlab/proto/src/main/webapp/general/login.jsp'
    parser.parse(path)
