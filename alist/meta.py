#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng

from copy import deepcopy
from alist import utils

empty_meta = {
    "path"              : None, # str
    "password"          : None, # str
    "hide"              : None, # list
    "only_shows"        : None, # list
    "upload"            : None, # bool
    "readme"            : None, # str
}

class AlistMeta(dict):
    """
    描述Alist meta信息
    """

    def __init__(self, **kwargs):
        super().__init__(deepcopy(empty_meta))
        for key in kwargs:
            try:
                self[key] = kwargs[key]
            except KeyError:
                pass

    def __setitem__(self, __key, __value):
        if __key in self.keys() or __key == 'id':
            if __key in ['hide', 'only_shows'] and __value != None:
                return super().__setitem__(__key, ','.join(__value))
            else:
                return super().__setitem__(__key, __value)
        else:
            raise KeyError(__key)

    def __delitem__(self, __key) -> None:
        raise NotImplemented

class AlistAdminMeta(object):
    """
    /admin/meta 相关API的实现
    """
    def __init__(self, alist, endpoint: str):
        self.alist = alist
        self.endpoint = f'{endpoint}/meta'

    def _post_create(self, account: AlistMeta):
        endpoint = f'{self.endpoint}/create'
        return self.alist.post(endpoint, json=account)

    def _create(self, **kwargs):
        # 检查必要的字段是否设置
        if 'path' not in kwargs:
            raise ValueError(f"meta must set path")
        account = AlistMeta(**kwargs)
        return self._post_create(account)

    def create(self,
               path,
               password = None,
               hide = None,
               only_shows = None,
               upload = False,
               readme = None):
        """创建meta
        :param path: 路径
        :param password: 访问密码
        :param hide: 隐藏文件列表
        :type hide: list
        :param only_shows: 允许显示的文件列表
        :type only_shows: list
        :param upload: 允许游客上传
        :param readme: readme url

        >>> alist.admin.meta.create('/path', password='123', hide=['README.md'])
        True
        """
        return self._create(path=path,
                            password=password,
                            hide=hide,
                            only_shows=only_shows,
                            upload=upload,
                            readme=readme)

    def _delete(self, id):
        params = {'id': id}
        return self.alist.delete(self.endpoint, params = params)

    def delete(self, path):
        """删除meta
        :param path: 路径

        >>> alist.admin.meta.delete('/path')
        True
        """
        meta = self.alist.admin.metas.get_meta(path)
        return self._delete(meta['id'])

    def save(self, meta: AlistMeta):
        """修改meta的设置并保存
        :param meta: meta信息
        :type meta: AlistMeta

        >>> meta = client.admin.metas.get_meta('/path')
        >>> meta['password'] = '789'
        >>> meta['upload'] = True
        >>> client.admin.meta.save(meta)
        True
        """
        endpoint = f'{self.endpoint}/save'
        return self.alist.post(endpoint, json = meta)

class AlistAdminMetas(object):
    """
    meta列表
    """
    metas = list()
    def __init__(self, alist, endpoint):
        self.alist = alist
        self.endpoint = f'{endpoint}/metas'
        self.metas = deepcopy(self.metas)

    def get(self):
        """获取meta列表

        >>> client.admin.metas.get()
        [{'path': '/path', 'password': '789', 'hide': 'README.md', 'only_shows': '', 'upload': True, 'readme': '', 'id': 1}]
        """
        self.metas.clear()
        results = self.alist.get(self.endpoint)
        for r in results:
            self.metas.append(AlistMeta(**r))
        return self.metas

    def get_meta(self, id_or_path):
        """获取指定meta
        :param id_or_path: meta id 或者是 meta path

        >>> client.admin.metas.get_meta('/path')
        {'path': '/path', 'password': '789', 'hide': 'README.md', 'only_shows': '', 'upload': True, 'readme': '', 'id': 1}
        """
        metas = self.get()
        for meta in metas:
            if meta['id'] == id_or_path or meta['path'] == id_or_path:
                return meta
        raise KeyError(f'{id_or_path} not found')

    def __getitem__(self, index):
        return self.get()[index]

    def __delitem__(self, __key):
        raise NotImplemented

    def __call__(self, *args, **kwds):
        return self.get()

