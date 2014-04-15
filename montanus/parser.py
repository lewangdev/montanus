# coding=utf8

#importdd config

from logger import logger
import utils
from config import config

import re
import logging
import os

class Parser(object):
    """
    """
    CHARSET = 'utf8'
    BINARY_FILE_EXTS = [
            '.png', '.bmp', '.gif',  '.ico',
            '.jfif', '.jpe', '.jpeg', '.jpg'
            ]

    TEXT_FILE_EXT = ['.css', '.js', '.jsp', '.html']
    ENTRY_FILE_EXT = ['.jsp', '.html']

    HTML_REGEX = '(<link.*href|<script.*src|<img.*src)=["\'](.*?)["\']'
    CSS_REGEX = '(@import.*url|background.*url|background-image.*url).*?\(["\']*(.*?)["\']*\)'
    RESOURCE_MAP = {}
    BASE_PATH = '.'
    URI_PREFIX = ''

    def __init__(self):
        pass

    def rename(self, path):
        new_path = utils.unique_name(path, config.default['md5_length'], '_')
        if new_path is None:
            return None
        (parent_path, new_file_name) = os.path.split(new_path)
        logger.debug(new_file_name)

        #TODO
        #[x] Rename
        os.rename(path, new_path)
        os.co
        return new_file_name

    def parse(self, path):
        """
        Find links and img in html. This is the entrance. So no need to parse html-like files
        """
        logger.debug('In Parse %s' % path)
        lower_path = path.lower()
        if lower_path.startswith("http") or lower_path.startswith("https") or lower_path.startswith("ftp"):
            return

        (file_name_with_path, file_ext) = os.path.splitext(path)
        if not file_ext in self.TEXT_FILE_EXT:
            return

        regex = self.HTML_REGEX
        if lower_path.endswith('css'):
            regex = self.CSS_REGEX
        elif lower_path.endswith('js'):
            regex = self.HTML_REGEX

        try:
            content = open(path).read().decode(self.CHARSET)
        except Exception:
            return
        pattern = re.compile(regex, re.IGNORECASE)
        res_list = pattern.findall(content)

        (parent_path, file_name) = os.path.split(path)
        relative_parent_path_len = len(parent_path) - len(self.BASE_PATH)
        relative_parent_path = parent_path[0 - relative_parent_path_len:]
        logger.debug("File Meta : %s %s %s" % (parent_path, file_name, relative_parent_path))

        #TODO
        #[x] Dive into css,js... files
        #[x] Get md5 of image files
        for item in res_list:
            logger.debug('Found %s ' % item[1])
            if item[1].startswith('.') or item[1].startswith('..'):
                abs_path = (parent_path + '%s%s') % ('/', item[1])
            elif item[1].startswith("/"):
                abs_path = self.BASE_PATH + item[1]
            else:
                continue
            (file_name_with_path, file_ext) = os.path.splitext(abs_path)
            if file_ext in self.BINARY_FILE_EXTS:
                if self.RESOURCE_MAP.get(abs_path) is None:
                    new_file_name = self.rename(abs_path)
                    logger.success(new_file_name)
                    self.RESOURCE_MAP[abs_path] = new_file_name
            else:
                self.parse(abs_path)

        for item in res_list:
            if item[1].startswith('.') or item[1].startswith('..'):
                item_abs_path = (parent_path + '%s%s') % ('/', item[1])
            elif item[1].startswith("/"):
                item_abs_path = self.BASE_PATH + item[1]
            else:
                continue
            if self.RESOURCE_MAP.get(item_abs_path) is not None:
                (parent_path, file_name) = os.path.split(item[1])
                logger.debug('Path: %s %s' % (parent_path, file_name))
                logger.debug('Replace %s to %s' % ( item[1], (parent_path + '/%s') % self.RESOURCE_MAP.get(item_abs_path)))
                content = content.replace(item[1], ('%s' + parent_path + '/%s') % (self.URI_PREFIX, self.RESOURCE_MAP.get(item_abs_path)))

        content = content.encode('utf-8')
        file = open(path, 'w')
        logger.debug(path)
        file.write(content)
        file.close()

        if self.RESOURCE_MAP.get(path) is None and (path.endswith('.css') or path.endswith('.js')):
            new_path =  self.rename(path)
            if new_path is not None:
                logger.debug(new_path)
                self.RESOURCE_MAP[path] = new_path

    def find(self, base_path):
        '''Find all entry files'''
        file_name_list = os.listdir(base_path)
        for file_name in file_name_list:
            logger.debug(file_name)
            path = '%s/%s' % (base_path, file_name)
            (file_name_with_path, file_ext) = os.path.splitext(path)
            if os.path.isdir(path):
                self.find(path)
            elif file_ext in self.ENTRY_FILE_EXT:
                self.parse(path)

    def process(self):
        self.find(self.BASE_PATH)
        logger.success("All files have been processed")

parser = Parser()  # build a runtime parser

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
