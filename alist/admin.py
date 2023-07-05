#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng

from alist.setting import AlistAaminSettings

class AlistAdmin(object):
    def __init__(self, alist):
        self.alist = alist
        self.endpoint = '/admin'
        self.settings = AlistAaminSettings(alist, self.endpoint)

    def login(self):
        """ 登录
        :returns:
            登录成功返回Ture，登录失败触发异常。
        """
        endpoint = f'{self.endpoint}/login'
        # if login fail, will raise exception
        return self.alist.get(endpoint)

    def accounts(self):
        """ 获取账号列表。
        :returns:
            账号列表。
        """
        endpoint = f'{self.endpoint}/accounts'
        return self.alist.get(endpoint)

    def account_create(self):
        pass

    def account_save(self):
        pass

    def account_delete(self):
        pass


    def drivers(self):
        """ 获取dricer列表，包含driver需要配置的字段列表
        :returns:
            driver列表
        """
        endpoint = f'{self.endpoint}/drivers'
        return self.alist.get(endpoint)

    def clear_cache(self):
        """ 清理所有的缓存数据。
        :returns:
            清理成功返回True，清理失败触发异常。
        """
        endpoint = f'{self.endpoint}/clear_cache'
        return self.alist.get(endpoint)


    def metas(self):
        """ 获取meta列表。
        :returns:
            meta列表。
        """
        endpoint = f'{self.endpoint}/metas'
        return self.alist.get(endpoint)

    def meta_create(self):
        pass

    def meta_save(self):
        pass

    def meta_delete(self):
        pass


    def link(self, path):
        """ 返回真实的链接，且携带头，只提供给中转程序使用。
        :param path:
        :returns:
            真实的链接。
        """
        data = {
            'path': path
        }
        endpoint = f'{self.endpoint}/link'
        return self.alist.get(endpoint, json=data)

    def files(self, path, names):
        """ 删除指定路径下的若干个文件和文件夹
        :param path:
        :param names: 文件名和文件夹列表。
        :returns:
            删除成功返回True。
        """
        endpoint = f'{self.endpoint}/files'
        data = {
            'path': path,
            'names': names
        }
        return self.alist.delete(endpoint, json=data)

    def mkdir(self, path):
        """ 创建文件夹
        :param path:
        :returns:
            创建成功放回True。
        """
        data = {
            'path': path
        }
        endpoint = f'{self.endpoint}/mkdir'
        return self.alist.post(endpoint, json=data)

    def rename(self, path, name):
        """ 重命名
        :param path: 旧文件名，完整路径
        :param name: 新文件名，不带路径
        :returns:
            重命名成功返回True
        """
        data = {
            'path': path,
            'name': name
        }
        endpoint = f'{self.endpoint}/rename'
        return self.alist.post(endpoint, json=data)

    def move(self, src_dir, dst_dir, names):
        """ 移动文件，支持文件夹。
        :param src_dir: 源文件夹
        :param dst_dir: 目的文件夹
        :param names: 文件/文件夹列表
        :returns:
            移动成功返回True
        """
        data = {
            'src_dir': src_dir,
            'dst_dir': dst_dir,
            'names': names
        }
        endpoint = f'{self.endpoint}/move'
        return self.alist.post(endpoint, json=data)

    def copy(self, src_dir, dst_dir, names):
        """ 复制文件，支持文件夹。
        :param src_dir: 源文件夹
        :param dst_dir: 目的文件夹
        :param names: 文件/文件夹列表
        :returns:
            复制成功返回True
        """
        data = {
            'src_dir': src_dir,
            'dst_dir': dst_dir,
            'names': names
        }
        endpoint = f'{self.endpoint}/copy'
        return self.alist.post(endpoint, json=data)

    def folder(self, path):
        """ 获取指定路径下的所有文件夹
        :param path:
        :returns:
            文件夹列表。
        """
        data = {
            'path': path
        }
        endpoint = f'{self.endpoint}/folder'
        return self.alist.post(endpoint, json=data)

    def refresh(self, path):
        """ 刷新指定路径。
        :param path: 刷新的路径。
        :returns:
            刷新成功返回True，刷新失败触发异常。
        """
        endpoint = f'{self.endpoint}/refresh'
        data = {
            'path': path
        }
        self.alist.post(endpoint, json=data)
        self.alist.public.path(path)
        return True
