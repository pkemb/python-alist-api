#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng

from collections.abc import Iterator
import json
from copy import deepcopy

group_front = 0
group_back  = 1
group_other = 2

empty_setting = {
    "key"           : None, # str
    "value"         : None, # str
    "description"   : None, # str
    "type"          : None, # str
    "group"         : None, # int, group_front / group_back / group_other
    "access"        : None, # int
    "values"        : None, # str
    "version"       : None, # str
}

class AlistSetting(dict):
    """
    描述Alist设置，包含key、value、description、type、group、access、values、version等信息。
    必须设置key。对象初始化之后，只能修改value，其他属性不能修改。
    """
    def __init__(self, **kwargs):
        super().__init__(deepcopy(empty_setting))
        if 'key' not in kwargs:
            raise ValueError("must set \"key\"")

        for key in super().keys():
            try:
                super().__setitem__(key, kwargs[key])
            except KeyError:
                pass

    def __setitem__(self, __key, __value):
        if __key != 'value':
            raise KeyError(f'only value allow modify')
        return super().__setitem__(__key, __value)

    def __delitem__(self, __key):
        raise NotImplementedError("can't delete any item")

    def get_value(self):
        """
        获取设置值
        """
        return self['value']

    def set_value(self, new):
        """
        根据类型，对新值new进行判断，保存。

        :param new: 如果type == 'bool'，则新值new只能是'true'或'false'。
                    如果type == 'select'，则新值new必须是values指定的值。
                    其他type无限制。

        :return: 新值new。
        """
        stype = self['type']
        if stype == 'bool':
            if new not in ['true', 'false']:
                raise ValueError(f"for bool setting, value must be true or false")
        elif stype == 'select':
            if new not in self['values'].split(','):
                raise ValueError(f"for select setting, value must be {self['values']}")

        self['value'] = new
        return self['value']


class AlistAaminSettings(object):
    """
    Alist管理员设置
    """

    settings_ro = ['version']
    """只读设置"""

    settings_rw = ['title', 'logo', 'favicon', 'icon color',
                   'announcement', 'text types', 'audio types',
                   'video types', 'hide files', 'music cover', 'site beian',
                   'global readme url', 'pdf viewer url', 'autoplay video',
                   'autoplay audio', 'customize head', 'customize body',
                   'home emoji', 'animation', 'artplayer whitelist',
                   'artplayer autoSize', 'load type', 'default page size',
                   'password', 'd_proxy types', 'check parent folder',
                   'check down link', 'WebDAV username', 'WebDAV password',
                   'Visitor WebDAV username', 'Visitor WebDAV password',
                   'ocr api', 'enable search', 'Aria2 RPC url',
                   'Aria2 RPC secret',]
    """可修改的设置"""

    def __init__(self, alist, admin, endpoint):
        self.alist = alist
        self.endpoint = endpoint

        for key in self.settings_ro:
            attr = f"setting_{key.replace(' ', '_').replace('.', '_')}"
            setattr(admin, attr, self._factory_get(key))

        for key in self.settings_rw:
            attr = f"setting_{key.replace(' ', '_').replace('.', '_')}"
            setattr(admin, attr, self._factory_get_or_update(key))

    def get(self, group = None):
        """
        获取管理员设置。

        :param group: 指定设置组。如果留空，返回所有设置。
        :return: 管理员设置。
        """
        endpoint = f'{self.endpoint}/settings'
        if group is None:
            settings = self.alist.get(endpoint)
        else:
            settings = self.alist.get(endpoint, params = {'group': group})

        return [AlistSetting(**s) for s in settings]

    def __call__(self, group = None):
        return self.get(group)

    def frontend(self):
        """获取前端设置"""
        return self.get(group=group_front)

    def backend(self):
        """获取后端设置"""
        return self.get(group=group_back)

    def other(self):
        """获取其他设置"""
        return self.get(group=group_other)

    def get_setting(self, key) -> AlistSetting:
        """
        获取指定设置。

        :param key: 设置的键值
        """
        settings = self.get()
        for s in settings:
            if s['key'] == key:
                return s
        raise KeyError(f'setting \'{key}\' not found')

    def save(self, settings: list):
        """
        保存设置

        :param settings: AlistSetting列表
        :return: 保存成功返回True
        """
        endpoint = f'{self.endpoint}/settings'
        return self.alist.post(endpoint, json=[s for s in settings])

    def _get_or_update(self, key, new = None):
        """
        获取或更新设置的值，内部API

        :param key:
        :param new:
        :return: 设置的值
        """
        s = self.get_setting(key)
        old = s.get_value()
        if new is None or new == old:
            return old
        else:
            s.set_value(new)
            self.save([s])
            return new

    def _factory_get_or_update(self, key):
        def _get_or_update_wrapper(new = None):
            return self._get_or_update(key, new)
        return _get_or_update_wrapper

    def _factory_get(self, key):
        def _get_wrapper():
            return self._get_or_update(key)
        return _get_wrapper

    def delete(self):
        """删除设置。未实现。"""
        endpoint = f'{endpoint}/setting'
        pass

class AlistPublicSettings(object):
    settings = ['version', 'title', 'logo', 'favicon', 'icon color',
                'announcement', 'text types', 'audio types', 'video types',
                'hide files', 'music cover', 'site beian', 'global readme url',
                'pdf viewer url', 'autoplay video', 'autoplay audio',
                'home emoji', 'animation', 'check down link', 'artplayer whitelist'
                'artplayer autoSize', 'load type', 'default page size',
                'enable search', 'no cors', 'no upload']
    """公开设置的键值"""

    def __init__(self, alist, public, endpoint):
        self.alist = alist
        self.endpoint = endpoint

        for key in self.settings:
            attr = f"setting_{key.replace(' ', '_').replace('.', '_')}"
            setattr(public, attr, self._factory_get_setting(key))

    def get(self, group = None):
        """
        获取公开的设置

        :return: 公开的设置
        """
        endpoint = f'{self.endpoint}/settings'
        settings = self.alist.get(endpoint)
        return [AlistSetting(**s) for s in settings]

    def __call__(self, group = None):
        return self.get(group)

    def get_setting(self, key):
        """
        获取指定设置。

        :param key: 设置的键值
        """
        settings = self.get()
        for s in settings:
            if s['key'] == key:
                return s
        raise KeyError(f'setting \'{key}\' not found')

    def _factory_get_setting(self, key):
        def _get_setting_wrapper():
            return self.get_setting(key)
        return _get_setting_wrapper
