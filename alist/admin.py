#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng

from alist.setting import AlistAaminSettings
from alist.driver import AlistAdminDrivers
from alist.account import AlistAdminAccount, AlistAdminAccounts
from alist.meta    import AlistAdminMeta, AlistAdminMetas

class AlistAdmin(object):
    """
    '/api/admin'相关的API
    """
    def __init__(self, alist):
        self.alist = alist
        self.endpoint = '/admin'
        self.settings = AlistAaminSettings(alist, self, self.endpoint)
        self.drivers  = AlistAdminDrivers(alist, self.endpoint)
        self.account  = AlistAdminAccount(alist, self.endpoint)
        self.accounts = AlistAdminAccounts(alist, self.endpoint)

        self.meta     = AlistAdminMeta(alist, self.endpoint)
        self.metas    = AlistAdminMetas(alist, self.endpoint)

    def login(self):
        """
        登录。不建议直接使用此接口。

        .. code-block:: python

            result = client.admin.login()

        :return: 登录成功返回Ture，登录失败触发异常。
        """
        endpoint = f'{self.endpoint}/login'
        # if login fail, will raise exception
        return self.alist.get(endpoint)

    def clear_cache(self):
        """
        清理所有的缓存数据。

        .. code-block:: python

            client.admin.clear_cache()

        :return: 清理成功返回True，清理失败触发异常。
        """
        endpoint = f'{self.endpoint}/clear_cache'
        return self.alist.get(endpoint)

    def link(self, path):
        """
        返回真实的链接，且携带头，只提供给中转程序使用。

        .. code-block:: python

            link = client.admin.link('/path/to/file')

        :param path: 文件路径。
        :return: 真实的链接。
        """
        data = {
            'path': path
        }
        endpoint = f'{self.endpoint}/link'
        return self.alist.get(endpoint, json=data)

    def files(self, path, names):
        """
        删除指定路径下的若干个文件和文件夹。

        .. code-block:: python

            # 删除文件 '/path/file' 和文件夹 '/path/dir'。
            result = client.admin.files('/path', ['file', 'dir'])

        :param path: 文件所在路径。
        :param names: 文件名和文件夹列表。
        :return: 删除成功返回True。
        :type names: list
        """
        endpoint = f'{self.endpoint}/files'
        data = {
            'path': path,
            'names': names
        }
        return self.alist.delete(endpoint, json=data)

    def mkdir(self, path):
        """
        创建文件夹。

        .. code-block:: python

            client.admin.mkdir('/path/to/new-dir')

        :param path: 新文件夹的路径
        :return: 创建成功放回True。创建失败触发异常。
        """
        data = {
            'path': path
        }
        endpoint = f'{self.endpoint}/mkdir'
        return self.alist.post(endpoint, json=data)

    def rename(self, path, name):
        """
        重命名文件或文件名

        .. code-block:: python

            # 将文件 '/path/to/old-name' 重命名为 '/path/to/new-name'
            client.admin.rename('/path/to/old-name', 'new-name')

        :param path: 旧文件名，完整路径
        :param name: 新文件名，不带路径
        :return: 重命名成功返回True
        """
        data = {
            'path': path,
            'name': name
        }
        endpoint = f'{self.endpoint}/rename'
        return self.alist.post(endpoint, json=data)

    def move(self, src_dir, dst_dir, names):
        """
        移动文件和文件夹。

        .. code-block:: python

            # 将文件 '/path/to/old/file' 移动到 '/path/to/new/file'
            # 将文件 '/path/to/old/dir' 移动到 '/path/to/new/dir'

            client.admin.move('/path/to/old', '/path/to/new', ['file', 'dir'])

        :param src_dir: 源文件夹
        :param dst_dir: 目的文件夹
        :param names: 文件/文件夹列表
        :return: 移动成功返回True
        :type names: list
        """
        data = {
            'src_dir': src_dir,
            'dst_dir': dst_dir,
            'names': names
        }
        endpoint = f'{self.endpoint}/move'
        return self.alist.post(endpoint, json=data)

    def copy(self, src_dir, dst_dir, names):
        """
        复制文件和文件夹。

        .. code-block:: python

            # 将文件 '/path/to/old/file' 复制到 '/path/to/new/file'
            # 将文件 '/path/to/old/dir' 复制到 '/path/to/new/dir'

            client.admin.copy('/path/to/old', '/path/to/new', ['file', 'dir'])

        :param src_dir: 源文件夹
        :param dst_dir: 目的文件夹
        :param names: 文件/文件夹列表
        :return: 复制成功返回True
        :type names: list
        """
        data = {
            'src_dir': src_dir,
            'dst_dir': dst_dir,
            'names': names
        }
        endpoint = f'{self.endpoint}/copy'
        return self.alist.post(endpoint, json=data)

    def folder(self, path):
        """
        获取指定路径下的所有文件夹。

        .. code-block:: python

            result = client.admin.folder('/path')

        :param path: 指定路径。
        :return: 文件夹列表。
        """
        data = {
            'path': path
        }
        endpoint = f'{self.endpoint}/folder'
        return self.alist.post(endpoint, json=data)

    def refresh(self, path):
        """
        刷新指定路径。

        .. code-block:: python

            client.admin.refresh('/path')

        :param path: 刷新的路径。
        :return: 刷新成功返回True，刷新失败触发异常。
        """
        endpoint = f'{self.endpoint}/refresh'
        data = {
            'path': path
        }
        self.alist.post(endpoint, json=data)
        self.alist.public.path(path)
        return True
