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

    HTML_REGEX = '(<link.*href|<script.*src|<img.*src)="(.*?)"'
    CSS_REGEX = '(@import.*url|backgroud.*url|background-image.*url).*\(["\']*(.*?)["\']*\)'
    RESOURCE_MAP = {}

    def __init__(self):
        pass

    def __css_parse(self, path):
        """
        Parse css files
        """
        base_path = '/Users/wangle/Workspace/gitlab/proto/src/main/webapp%s%s'
        abs_path = base_path % ('/' if path.startswith('.') else '', path)
        content = open(abs_path).read().decode(self.CHARSET)
        pattern = re.compile(self.CSS_REGEX, re.IGNORECASE)
        res_list = pattern.findall(content)
        for item in res_list:
            logger.debug("css parser %s" % item[1])
            #TODO
            #[] Parse all files found in res_list

        #TODO
        #[] Replace all files with new name in RESOURCE_MAP
        for item in res_list:
            pass
            #content.replace(item[1], self.RESOURCE_MAP[item[1]])

    def __js_parse(self, path):
        """
        Parse js files
        """
        content = open(path).read().decode(self.CHARSET)

    def __binary_parse(self, url):
        base_path = '/Users/wangle/Workspace/gitlab/proto/src/main/webapp%s%s'
        abs_path = base_path % ('/' if url.startswith('.') else '', url)
        new_abs_path = utils.unique_name(abs_path, 10, '_')

        (parent_path, new_file_name) = os.path.split(new_abs_path)
        (parent_url, old_file_name) = os.path.split(url)
        logger.success("%s %s %s %s" % (parent_path, new_file_name, parent_url, old_file_name))

        new_url = "%s/%s" % (parent_url, new_file_name)
        logger.success(new_url)
        self.RESOURCE_MAP[url] = new_url;

        #TODO
        #[x] Rename
        #os.rename(abs_path, new_abs_path)

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
                self.__css_parse(item[1])
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
