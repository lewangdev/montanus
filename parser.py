#!/usr/bin/env python
# -*- coding:utf-8 -*-

import utils
import re
import logging
import os
import shutil

from logger import logger
from random import sample


class Parser(object):
    """
    Find and Parse all static files to CDN requirement
    """
    __charset          = 'utf-8'
    __binary_file_exts = [
        '.png', '.bmp', '.gif', '.ico',
        '.jfif', '.jpe', '.jpeg', '.jpg'
    ]
    __text_file_exts = ['.css', '.js']
    __templates_exts = ['.jsp', '.html']

    __template_regex = '(?:<link.*href|<script.*src|<img.*src)=["\'](.*?)["\']'
    __css_regex      = '(?:@import.*url|background.*url|background-image.*url).*?\(["\']*(.*?)["\']*\)'
    __js_regex       = '(?:<link.*href|<script.*src|<img.*src)=["\'](.*?)["\']'

    __resource_map = {}

    custom_config = None
    statistics = {
        "static_file_count": 0,
        "not_found_count": 0
    }

    def __init__(self):
        pass

    def __get_templates_path(self):
        return self.custom_config.templates_path

    def __get_static_files_path(self):
        return self.custom_config.static_files_path

    def __get_url_prefix(self):
        return "%s://%s" % (
            self.custom_config.protocol,
            sample(self.custom_config.domains, 1)[0])

    def __rename_with_md5(self, path):
        new_path = utils.unique_name(path, self.custom_config.md5_len,
                                     self.custom_config.md5_concat_by)
        if new_path is None:
            return None
        (parent_path, new_file_name) = os.path.split(new_path)

        #TODO
        #[x] Rename
        if self.custom_config.delete_source:
            os.rename(path, new_path)
        else:
            shutil.copy(path, new_path)
        return new_file_name

    def __is_a_link(self, path):
        """Judge the path is a link or not"""
        # match() is different from search()
        # if we use search(), we should use ^(http(s)?|ftp)
        match = re.match("(http(s)?|ftp|chrome-extension)", path, re.IGNORECASE)
        if match is not None:
            return True
        else:
            return False

    def __gen_path(self, parent_file_path, url):
        if self.__is_a_link(url):
            logger.info("LINK FOUND:%s <- %s" % (url.decode(self.__charset), parent_file_path.decode(self.__charset)))
            return None
        (parent_path, parent_file_name) = os.path.split(parent_file_path)
        if url.startswith('/'):
            return '%s%s' % (self.__get_static_files_path(), url)
        else:
            return '%s/%s' % (parent_path, url)

    def __parse_static_file(self, parent_file_path, url):
        path = self.__gen_path(parent_file_path, url)
        if path is None:
            return

        if not os.path.exists(path):
            if self.__resource_map.get(path) is None:
                logger.warning("NOT FOUND:%s <- %s" % (path.decode(self.__charset), parent_file_path.decode(self.__charset)))
                self.statistics["not_found_count"] += 1
            return

        (url_without_ext, file_ext) = os.path.splitext(url)
        if file_ext in self.__binary_file_exts:
            if self.__resource_map.get(path) is None:
                name_with_md5 = self.__rename_with_md5(path)
                self.__resource_map[path] = name_with_md5
                logger.debug('%s <- %s' % (name_with_md5, path))
            return

        elif file_ext in self.__text_file_exts:
            regex = self.__css_regex
            if url.endswith('.js'):
                regex = self.__js_regex

            logger.info("PATH:%s" % path)
            with open(path, 'r') as staticfile:
                content = staticfile.read().decode(self.__charset)
                pattern = re.compile(regex, re.IGNORECASE)
                targets_matched = pattern.findall(content)
                for target in targets_matched:
                    static_file_url = target
                    if not self.__is_a_link(static_file_url):
                        logger.debug("%s <- %s" % (static_file_url.decode(self.__charset), url.decode(self.__charset)))
                        self.__parse_static_file(path, static_file_url)
                        content = self.__replace_with_cdnurl(path, static_file_url, content)

            with open(path, 'w') as staticfile:
                staticfile.write(content.encode(self.__charset))
                if self.__resource_map.get(path) is None:
                    path_with_md5 = self.__rename_with_md5(path)
                    if path_with_md5 is not None:
                        self.__resource_map[path] = path_with_md5

    def __replace_with_cdnurl(self, parent_path, url_in_parent, content):
        static_file_path = self.__gen_path(parent_path, url_in_parent)
        if self.__resource_map.get(static_file_path) is not None:
            (base_path, file_name) = os.path.split(url_in_parent)
            name_with_md5 = self.__resource_map.get(static_file_path)
            static_file_cdnurl = "%s%s%s" % (self.__get_url_prefix(), base_path, name_with_md5)
            content = content.replace(url_in_parent, static_file_cdnurl)
        return content

    def __parse_template(self, path):
        """
        Find links and img in html. This is the entrance.
        So no need to parse html-like files
        """
        regex = self.__template_regex
        with open(path) as templatefile:
            content = templatefile.read().decode(self.__charset)
            pattern = re.compile(regex, re.IGNORECASE)
            targets_matched = pattern.findall(content)
            for target in targets_matched:
                static_file_url = target
                logger.debug("%s <- %s" % (static_file_url.decode(self.__charset), path.decode(self.__charset)))
                self.statistics["static_file_count"] += 1
                self.__parse_static_file(path, static_file_url)
                content = self.__replace_with_cdnurl(path, static_file_url, content)

        with open(path, 'w') as staticfile:
            staticfile.write(content.encode(self.__charset))

    def find_all_templates(self, parent_path):
        """Find all template files"""
        templates = os.listdir(parent_path)
        for template_name in templates:
            path = '%s/%s' % (parent_path, template_name)
            if os.path.isdir(path):
                self.find_all_templates(path)
            else:
                (full_path_without_ext, template_ext) = os.path.splitext(path)
                if template_ext in self.__templates_exts:
                    self.__parse_template(path)

    def process(self):
        self.find_all_templates(self.__get_templates_path())
        logger.debug('MAP:%s' % self.__resource_map)


parser = Parser()  # build a runtime parser

if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
