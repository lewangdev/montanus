#!/usr/bin/env python
# -*- coding:utf-8 -*-

from logger import logger
from random import sample
import utils
import re
import logging
import os


class Parser(object):
    """
    """
    __charset = 'utf-8'
    __binary_file_exts = [
        '.png', '.bmp', '.gif', '.ico',
        '.jfif', '.jpe', '.jpeg', '.jpg'
    ]

    __text_file_exts = ['.css', '.js', '.jsp', '.html']
    __entry_file_exts = ['.jsp', '.html']

    __html_regex = '(<link.*href|<script.*src|<img.*src)=["\'](.*?)["\']'
    __css_regex = '(@import.*url|background.*url|background-image.*url).*?\(["\']*(.*?)["\']*\)'
    __resource_map = {}

    custom_config = None

    def __init__(self):
        pass

    def get_root_path(self):
        return self.custom_config.root_path

    def get_url_prefix(self):
        return "%s://%s" % (
            self.custom_config.protocol,
            sample(self.custom_config.domains, 1)[0])

    def rename_with_md5(self, path):
        new_path = utils.unique_name(path, self.custom_config.md5_length,
                                     self.custom_config.md5_concat_by)
        if new_path is None:
            return None
        (parent_path, new_file_name) = os.path.split(new_path)
        logger.debug(new_file_name)

        #TODO
        #[x] Rename
        os.rename(path, new_path)
        return new_file_name

    def parse(self, path):
        """
        Find links and img in html. This is the entrance. So no need to parse html-like files
        """
        logger.debug('In Parse %s' % path)
        lower_path = path.lower()
        if lower_path.startswith("http") or lower_path.startswith(
                "https") or lower_path.startswith("ftp"):
            return

        (file_name_with_path, file_ext) = os.path.splitext(path)
        if not file_ext in self.__text_file_exts:
            return

        regex = self.__html_regex
        if lower_path.endswith('css'):
            regex = self.__css_regex
        elif lower_path.endswith('js'):
            regex = self.__html_regex

        try:
            content = open(path).read().decode(self.__charset)
        except Exception:
            return
        pattern = re.compile(regex, re.IGNORECASE)
        res_list = pattern.findall(content)

        (parent_path, file_name) = os.path.split(path)
        relative_parent_path_len = len(parent_path) - len(self.get_root_path())
        relative_parent_path = parent_path[0 - relative_parent_path_len:]
        logger.debug("File Meta : %s %s %s" % (
            parent_path, file_name, relative_parent_path))

        #TODO
        #[x] Dive into css,js... files
        #[x] Get md5 of image files
        for item in res_list:
            logger.debug('Found %s ' % item[1])
            if item[1].startswith('.') or item[1].startswith('..'):
                abs_path = (parent_path + '%s%s') % ('/', item[1])
            elif item[1].startswith("/"):
                abs_path = self.get_root_path() + item[1]
            else:
                continue
            (file_name_with_path, file_ext) = os.path.splitext(abs_path)
            if file_ext in self.__binary_file_exts:
                if self.__resource_map.get(abs_path) is None:
                    new_file_name = self.rename_with_md5(abs_path)
                    logger.success(new_file_name)
                    self.__resource_map[abs_path] = new_file_name
            else:
                self.parse(abs_path)

        for item in res_list:
            if item[1].startswith('.') or item[1].startswith('..'):
                item_abs_path = (parent_path + '%s%s') % ('/', item[1])
            elif item[1].startswith("/"):
                item_abs_path = self.get_root_path() + item[1]
            else:
                continue
            if self.__resource_map.get(item_abs_path) is not None:
                (parent_path, file_name) = os.path.split(item[1])
                logger.debug('Path: %s %s' % (parent_path, file_name))
                logger.debug('Replace %s to %s' % (item[1],
                                                   ( parent_path + '/%s') % self.__resource_map.get(item_abs_path)))
                content = content.replace(item[1],
                                          ('%s' + parent_path + '/%s') % (
                                              self.get_url_prefix(),
                                              self.__resource_map.get(
                                                  item_abs_path)))

        content = content.encode(self.__charset)
        file_handler = open(path, 'w')
        file_handler.write(content)
        file_handler.close()

        if self.__resource_map.get(path) is None and (
                    path.endswith('.css') or path.endswith('.js')):
            new_path = self.rename_with_md5(path)
            if new_path is not None:
                logger.debug(new_path)
                self.__resource_map[path] = new_path

    def find(self, root_path):
        """Find all entry files"""
        file_name_list = os.listdir(root_path)
        for file_name in file_name_list:
            path = '%s/%s' % (root_path, file_name)
            (file_name_with_path, file_ext) = os.path.splitext(path)
            if os.path.isdir(path):
                self.find(path)
            elif file_ext in self.__entry_file_exts:
                self.parse(path)

    def process(self):
        self.find(self.get_root_path())


parser = Parser()  # build a runtime parser

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
