#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng

# doc: https://alist-doc.nn.ci/docs/api

from alist.setting import AlistPublicSettings

class AlistPublic(object):
    def __init__(self, alist):
        self.alist = alist
        self.endpoint = '/public'
        self.settings = AlistPublicSettings(self.alist, self, self.endpoint)

    def path(self, path, page_num=1, page_size=30, password=None):
        """
        获取指定路径 path 下的文件和文件夹列表。

        :param path: 路径
        :param page_num: 默认为1
        :param page_size: 默认为30
        :param password: 路径的访问密码。
        :return: 文件或目录属性，以及文件列表。

        .. code-block:: python

            files = client.public.path('/path')
            print(files['files'])
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
        """
        获取文件的预览URL。

        :param path: 文件路径
        :return: 文件的预览URL。
        """
        endpoint = f'{self.endpoint}/preview'
        data = {
            'path': path
        }
        return self.alist.post(endpoint, json=data)

    def search(self, path, keyword):
        """
        搜索文件。需要开启设置 enable search。默认是关闭的。

        :param path: 在此路径下搜索。
        :param keyword: 搜索关键字
        :return: 搜索的文件列表。
        """
        endpoint = f'{self.endpoint}/search'
        data = {
            'path': path,
            'keyword': keyword,
        }
        return self.alist.post(endpoint, json=data)

    def upload(self, files, path, password=None):
        """
        上传文件到指定路径。如果没有登录，则需要开启允许游客上传。参考meta。

        :param files: 文件列表
        :param path: 上传的路径
        :param password: 访问密码
        :type files: list
        :return: 上传结果。True表示成功，False表示失败。

        .. code-block:: python

            client.public.upload(['/path/to/local_file'], '/path/to/upload/path')
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

