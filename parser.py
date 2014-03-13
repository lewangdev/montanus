# coding=utf8

#import config
from logger import logger

import re
import logging

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

    HTML_REGEX = '<link.*href.*?>|<script.*src.*?>|<img.*src.*?>'
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
        Parse css files
        """
        content = open(path).read().decode(self.CHARSET)

    def parse(self, path):
        """
        Find links and img in html
        """
        logger.debug(path)
        content = open(path).read().decode(self.CHARSET)
        pattern = re.compile(self.HTML_REGEX, re.IGNORECASE)
        res_list = pattern.findall(content)
#TODO
#[] Dive into css,js... files
#[] get md5 of image files

        for item in res_list:
            logger.debug(item)


parser = Parser()  # build a runtime parser

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    path = '/Users/wangle/Workspace/gitlab/proto/src/main/webapp/general/login.jsp'
    parser.parse(path)
