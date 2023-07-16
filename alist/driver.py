#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng

from copy import deepcopy
from typing import Any

class AlistDriverAttribute(dict):
    """
    驱动属性
    """

    def __init__(self, **attr):
        super().__init__()

        for key in ['name', 'label', 'type', 'default',
                    'values', 'required', 'description']:
            super().__setitem__(key, attr[key])

    def get_name(self):
        return self['name']

    def is_required(self):
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
    驱动
    """
    def __init__(self, name, attrs):
        self.name = name
        self.attrs = list()
        for attr in attrs:
            self.attrs.append(AlistDriverAttribute(**attr))

    def get_attr(self, name):
        for attr in self.attrs:
            if name == attr['name']:
                return attr
        raise KeyError(f"{name} not found")

    def get_name(self):
        return self.name

    def get_required(self):
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
    驱动列表
    """
    drivers = list()

    def __init__(self, alist, endpoint) -> None:
        self.alist = alist
        self.endpoint = f'{endpoint}/drivers'
        self.drivers = deepcopy(self.drivers)

    def get(self):
        """ 获取驱动列表，包含驱动需要配置的字段列表
        :returns:
            驱动列表
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

    def get_driver(self, name):
        drivers = self.get()
        for d in drivers:
            if d.get_name() == name:
                return d
        raise KeyError(f'driver \'{name}\' not found')

    def  _factory_get_driver(self, name):
        def get_driver_wrapper():
            return self.get_driver(name)
        return get_driver_wrapper

