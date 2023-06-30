#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng

class AlistAdmin(object):
    def __init__(self, alist):
        self.alist = alist
        self.endpoint = '/admin'

    def login(self):
        """ 登录
        :returns:
            登录成功返回Ture，登录失败触发异常。
        """
        endpoint = f'{self.endpoint}/login'
        # if login fail, will raise exception
        return self.alist.get(endpoint)

    def settings(self):
        pass

    def settings_save(self):
        pass

    def settings_delete(self):
        pass


    def accounts(self):
        pass

    def account_create(self):
        pass

    def account_save(self):
        pass


    def drivers(self):
        pass

    def clear_cache(self):
        pass


    def metas(self):
        pass

    def meta_create(self):
        pass

    def meta_save(self):
        pass

    def meta_delete(self):
        pass


    def link(self):
        pass

    def files(self):
        pass

    def mkdir(self):
        pass

    def rename(self):
        pass

    def move(self):
        pass

    def copy(self):
        pass

    def folder(self):
        pass

    def refresh(self):
        pass
