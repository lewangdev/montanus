#!/usr/bin/env python
# -*- coding:utf-8 -*-
import re

class Handler:
    def css(self, content):
        css_regex = '(?:@import.*url|background.*url|background-image.*url).*?\(["\']*(.*?)["\']*\)'
        pattern = re.compile(css_regex, re.IGNORECASE)
        targets_matched = pattern.findall(content)
        return targets_matched

    def js(self, content):
        js_regex = '(?:<link.*href|<script.*src|<img.*src)=["\'](.*?)["\']'
        pattern = re.compile(js_regex, re.IGNORECASE)
        targets_matched = pattern.findall(content)

        js_regex = '(?:.*?)include\(\[(.*?)\]\)[;]'
        pattern = re.compile(js_regex, re.IGNORECASE)
        matched = pattern.findall(content)
        targets = matched[0].split(',')
        for targets in targets:
            targets_matched.append(targets.strip('\''))
        return targets_matched

    def common(self, content):
        template_regex = '(?:<link.*href|<script.*src|<img.*src)=["\'](.*?)["\']|(?:@import.*url|background.*url|background-image.*url).*?\(["\']*(.*?)["\']*\)''
        pattern = re.compile(template_regex, re.IGNORECASE)
        targets_matched = pattern.findall(content)
        return targets_matched

handler = Handler()
