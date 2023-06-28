#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng

class AlistPublic(object):
    def __init__(self, alist):
        self.alist = alist
        self.endpoint = '/public'

    def path(self, path, page_num=1, page_size=30, password=None):
        endpoint = f'{self.endpoint}/path'
        data = {
            'path': path,
            'password': password,
            'page_num': page_num,
            'page_size': page_size

        }
        return self.alist.post(endpoint, json=data)

    def preview(self, path):
        endpoint = f'{self.endpoint}/preview'
        data = {
            'path': path
        }
        return self.alist.post(endpoint, json=data)

    def search(self, path, keyword):
        endpoint = f'{self.endpoint}/search'
        data = {
            'path': path,
            'keyword': keyword,
        }
        return self.alist.post(endpoint, json=data)

    def upload(self, files, path, password=None):
        # Content Type 不再是json，而是 multipart/form-data
        endpoint = f'{self.endpoint}/upload'
        pass

    def settings(self):
        endpoint = f'{self.endpoint}/settings'
        return self.alist.get(endpoint)

