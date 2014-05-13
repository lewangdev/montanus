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

        js_regex = '\$\.include\(\[(.*?)\]\)[;]'
        pattern = re.compile(js_regex, re.IGNORECASE)
        matched = pattern.findall(content)
        for mitem in matched:
            targets = mitem.split(',')
            for target in targets:
                targets_matched.append(target.strip('\''))
        return targets_matched

    def common(self, content):
        template_regex = '(?:<link.*href|<script.*src|<img.*src)=["\'](.*?)["\']'
        pattern = re.compile(template_regex, re.IGNORECASE)
        targets_matched = pattern.findall(content)

        template_regex = '(?:@import.*url|background.*url|background-image.*url).*?\(["\']*(.*?)["\']*\)'
        pattern = re.compile(template_regex, re.IGNORECASE)
        matched = pattern.findall(content)
        for mitem in matched:
            targets_matched.append(mitem)
        return targets_matched

handler = Handler()
