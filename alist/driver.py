#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng

from copy import deepcopy
from typing import Any

class AlistDriverAttribute(object):
    """
    驱动属性
    """

    def __init__(self, **attr):

        self.name        = attr.get('name')
        self.label       = attr.get('label')
        self.type        = attr.get('type')
        self.default     = attr.get('default')
        self.values      = attr.get('values')
        self.required    = attr.get('required')
        self.description = attr.get('description')
        self.value       = None

    def set_value(self, value):
        if self.type == 'bool' and value not in ['true', 'false']:
            raise ValueError('type is bool, value must be true or false')
        if self.type == 'select' and value not in self.values.split(','):
            raise ValueError(f'type is select, value must be in {self.values}')

        self.value = value

    def get_value(self):
        return self.value

    def get_name(self):
        return self.name

    def __str__(self) -> str:
        return f'attr: {self.get_name()} value: {self.get_value()} required: {self.required}'

    def __repr__(self) -> str:
        return self.__str__()

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
            if name == attr.get_name():
                return attr.get_value()
        raise KeyError(f"{name} not found")

    def set_addr(self, name, value):
        for attr in self.attrs:
            if name == attr.get_name():
                return attr.set_value(value)
        raise KeyError(f"{name} not found")

    def get_name(self):
        return self.name

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

        results = self.alist.get(self.endpoint)
        for name in results:
            self.drivers.append(AlistDriver(name, results[name]))
            func_name = f"driver_{name.replace('.', '_')}"
            setattr(alist, func_name, self._factory_get_by_name(name))

    def get(self):
        """ 获取驱动列表，包含驱动需要配置的字段列表
        :returns:
            驱动列表
        """
        return self.drivers

    def __call__(self) -> Any:
        return self.get()

    def get_by_name(self, name):
        drivers = self.get()
        for d in drivers:
            if d.get_name() == name:
                return d
        raise KeyError(f'driver \'{name}\' not found')

    def  _factory_get_by_name(self, name):
        def get_driver():
            return self.get_by_name(name)
        return get_driver

