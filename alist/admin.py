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
