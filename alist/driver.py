#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng

from copy import deepcopy
from typing import Any

class AlistDriverAttribute(dict):
    """
    驱动属性。驱动包含 ``name``、``label``、``type``、``default``、
    ``values``、``required``、``description`` 等字段。所有字段初始化之后无法修改。
    """

    def __init__(self, **attr):
        super().__init__()

        for key in ['name', 'label', 'type', 'default',
                    'values', 'required', 'description']:
            super().__setitem__(key, attr[key])

    def get_name(self):
        """获取驱动属性的名字"""
        return self['name']

    def is_required(self):
        """属性是否必须提供。返回True表示必须提供。"""
        return self['required']

    def __str__(self) -> str:
        return f'attr: {self.get_name()} required: {self["required"]}'

    def __repr__(self) -> str:
        return self.__str__()

    def __setitem__(self, __key: Any, __value: Any) -> None:
        raise NotImplemented

    def __delitem__(self, __key: Any) -> None:
        raise NotImplemented

class AlistDriver(object):
    """
    描述Alist驱动。一个驱动包含若干个属性。
    """
    def __init__(self, name, attrs):
        self.name = name
        self.attrs = list()
        for attr in attrs:
            self.attrs.append(AlistDriverAttribute(**attr))

    def get_attr(self, name) -> AlistDriverAttribute:
        """
        获取驱动属性。

        :param name: 属性的名字
        """
        for attr in self.attrs:
            if name == attr['name']:
                return attr
        raise KeyError(f"{name} not found")

    def get_name(self):
        """获取驱动的名字"""
        return self.name

    def get_required(self):
        """获取驱动必须提供的属性"""
        required = list()
        for attr in self.attrs:
            if attr['required']:
                required.append(attr.get_name())
        return required

    def __str__(self) -> str:
        s = f"driver: {self.name}\n"
        for attr in self.attrs:
            s += f'{attr}\n'
        return s

    def __repr__(self) -> str:
        return self.__str__()

class AlistAdminDrivers(object):
    """
    驱动列表。api ``/api/admin/drivers`` 的实现。
    """
    drivers = list()

    def __init__(self, alist, endpoint) -> None:
        self.alist = alist
        self.endpoint = f'{endpoint}/drivers'
        self.drivers = deepcopy(self.drivers)

    def get(self):
        """ 获取所有驱动的列表，包含驱动必须提供的属性。

        :return: 驱动列表
        """
        if len(self.drivers) == 0:
            results = self.alist.get(self.endpoint)
            for name in results:
                self.drivers.append(AlistDriver(name, results[name]))
                func_name = f"driver_{name.replace('.', '_')}"
                setattr(self.alist, func_name, self._factory_get_driver(name))
        return self.drivers

    def __call__(self) -> Any:
        return self.get()

    def get_driver(self, name) -> AlistDriver:
        """
        获取指定名字的驱动。

        :param name: 驱动的名字。
        """
        drivers = self.get()
        for d in drivers:
            if d.get_name() == name:
                return d
        raise KeyError(f'driver \'{name}\' not found')

    def  _factory_get_driver(self, name):
        def get_driver_wrapper():
            return self.get_driver(name)
        return get_driver_wrapper

