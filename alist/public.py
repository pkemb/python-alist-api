#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng

# doc: https://alist-doc.nn.ci/docs/api

from alist.setting import AlistPublicSettings

class AlistPublic(object):
    def __init__(self, alist):
        self.alist = alist
        self.endpoint = '/public'
        self.settings = AlistPublicSettings(self.alist, self.endpoint)

    def path(self, path, page_num=1, page_size=30, password=None):
        """ 根据路径和密码请求文件或文件列表。
        :returns:
            文件或目录属性，以及文件列表。
        """
        endpoint = f'{self.endpoint}/path'
        data = {
            'path': path,
            'password': password,
            'page_num': page_num,
            'page_size': page_size

        }
        return self.alist.post(endpoint, json=data)

    def preview(self, path):
        """ 获取文件的预览URL。
        :returns:
            文件的预览URL。
        """
        endpoint = f'{self.endpoint}/preview'
        data = {
            'path': path
        }
        return self.alist.post(endpoint, json=data)

    def search(self, path, keyword):
        """ 搜索文件。需要开启，默认是关闭的。
        :returns:
            搜索的文件列表。
        """
        endpoint = f'{self.endpoint}/search'
        data = {
            'path': path,
            'keyword': keyword,
        }
        return self.alist.post(endpoint, json=data)

    def upload(self, files, path, password=None):
        """ 上传文件到指定路径。
        :returns:
            上传结果。True表示成功，False表示失败。
        """
        # Content Type 是 multipart/form-data
        endpoint = f'{self.endpoint}/upload'
        data = {
            'path': path,
            'password': password,
        }
        # https://docs.python-requests.org/en/latest/user/advanced/#post-multiple-multipart-encoded-files
        fs = [
            ('files', (filename, open(filename, 'rb'))) for filename in files
        ]
        return self.alist.post(endpoint, files=fs, data=data)

