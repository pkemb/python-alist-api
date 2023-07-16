#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng

from copy import deepcopy
from typing_extensions import SupportsIndex
from alist import utils
# from alist import AlistClient

empty_account = {
    "name"              : None, # str
    "index"             : None, # int
    "type"              : None, # str
    "username"          : None, # str
    "password"          : None, # str
    "refresh_token"     : None, # str
    "access_token"      : None, # str
    "root_folder"       : None, # str, path
    "status"            : None, # str
    "CronId"            : None, # int
    "DriveId"           : None, # str
    "limit"             : None, # int
    "order_by"          : None, # str
    "order_direction"   : None, # str
    "updated_at"        : None, # str, eg 2023-06-11T11:03:03.684818327+08:00
    "search"            : None, # True / False
    "client_id"         : None, # str
    "client_secret"     : None, # str
    "zone"              : None, # str
    "redirect_uri"      : None, # str
    "site_url"          : None, # str
    "site_id"           : None, # str
    "internal_type"     : None, # str
    "webdav_proxy"      : None, # True / False
    "proxy"             : None, # True / False
    "webdav_direct"     : None, # True / False
    "down_proxy_url"    : None, # str
    "api_proxy_url"     : None, # str
    "bucket"            : None, # str
    "endpoint"          : None, # str
    "region"            : None, # str
    "access_key"        : None, # str
    "access_secret"     : None, # str
    "custom_host"       : None, # str
    "extract_folder"    : None, # str
    "bool_1"            : None, # True / False
    "algorithms"        : None, # str
    "client_version"    : None, # str
    "package_name"      : None, # str
    "user_agent"        : None, # str
    "captcha_token"     : None, # str
    "device_id"         : None, # str
}

class AlistAccount(dict):
    """
    描述Alist账户信息
    """
    # account = deepcopy(empty_account)
    def __init__(self, **kwargs):
        super().__init__(deepcopy(empty_account))
        for key in kwargs:
            try:
                self[key] = kwargs[key]
            except KeyError:
                pass

    def __setitem__(self, __key, __value):
        if __key in self.keys() or __key == 'id':
            return super().__setitem__(__key, __value)
        else:
            raise KeyError(__key)

    def __delitem__(self, __key) -> None:
        raise NotImplemented

class AlistAdminAccount(object):
    """
    /account/ 相关API的实现
    """
    def __init__(self, alist, endpoint: str):
        self.alist = alist
        self.endpoint = f'{endpoint}/account'

    def _post_create(self, account: AlistAccount):
        endpoint = f'{self.endpoint}/create'
        return self.alist.post(endpoint, json=account)

    def _create(self, **kwargs):
        # 检查必要的字段是否设置
        try:
            driver = self.alist.admin.drivers.get_driver(kwargs['type'])
        except KeyError:
            raise KeyError(f"{kwargs['type']} not support")

        required = driver.get_required()
        required.append('name')
        not_set = set(required) - set(kwargs.keys())
        if len(not_set) != 0:
            raise ValueError(f"{kwargs['type']} must set {','.join(not_set)}")

        kwargs['updated_at'] = utils.get_timestamp()
        account = AlistAccount(**kwargs)
        return self._post_create(account)


    def create_Onedrive(self,
                        name,
                        zone,
                        internal_type,
                        client_id,
                        client_secret,
                        redirect_uri,
                        refresh_token,
                        proxy=False,
                        webdav_proxy=False,
                        webdav_direct=False,
                        **kwargs):
        """
        创建一个Onedrive账号
        :param name:
        :param zone:
        :param internal_type:
        :param client_id:
        :param client_secret:
        :param redirect_uri:
        :param refresh_token:
        :param index:
        :param proxy:
        :param webdav_proxy:
        :param webdav_direct:

        :param down_proxy_url:
        :param extract_folder:
        :param site_id:
        :param root_folder:
        :param order_by:
        :param order_direction:
        """
        return self._create(type="Onedrive",
                            name=name,
                            zone=zone,
                            internal_type=internal_type,
                            client_id=client_id,
                            client_secret=client_secret,
                            redirect_uri=redirect_uri,
                            refresh_token=refresh_token,
                            proxy=proxy,
                            webdav_proxy=webdav_proxy,
                            webdav_direct=webdav_direct,
                            **kwargs)

    def create_Native(self,
                      name,
                      root_folder,
                      webdav_direct=False,
                      **kwargs):
        """
        创建一个本地账号
        :param name:
        :param root_folder:
        :param webdav_direct:
        :param down_proxy_url:
        :param extract_folder:
        :param order_by:
        :param order_direction:
        """
        return self._create(type='Native',
                            name=name,
                            root_folder=root_folder,
                            webdav_direct=webdav_direct,
                            **kwargs)

    def create_Alist(self,
                     name,
                     site_url,
                     access_token,
                     proxy=False,
                     webdav_proxy=False,
                     webdav_direct=False,
                     **kwargs):
        """
        创建一个Alist账号
        :param name:
        :param site_url:
        :param access_token:
        :param proxy:
        :param webdav_proxy:
        :param webdav_direct:
        :param down_proxy_url:
        :param extract_folder:
        :param root_folder:
        """
        return self._create(type='Alist',
                            name=name,
                            site_url=site_url,
                            access_token=access_token,
                            proxy=proxy,
                            webdav_proxy=webdav_proxy,
                            webdav_direct=webdav_direct,
                            **kwargs)

    def _delete(self, id):
        params = {'id': id}
        return self.alist.delete(self.endpoint, params = params)

    def delete(self, name):
        account = self.alist.admin.accounts.get_account(name)
        return self._delete(account['id'])

    def save(self, account: AlistAccount):
        """
        修改账号的设置并保存
        """
        endpoint = f'{self.endpoint}/save'
        return self.alist.post(endpoint, json = account)

class AlistAdminAccounts(object):
    """
    alist账号列表
    """
    accounts = list()
    def __init__(self, alist, endpoint):
        self.alist = alist
        self.endpoint = f'{endpoint}/accounts'
        self.accounts = deepcopy(self.accounts)

    def get(self):
        """获取账号列表并覆盖旧值
        """
        self.accounts.clear()

        results = self.alist.get(self.endpoint)
        for r in results:
            self.accounts.append(AlistAccount(**r))
        return self.accounts

    def get_account(self, id_or_name):
        accounts = self.get()
        for acc in accounts:
            if acc['id'] == id_or_name or acc['name'] == id_or_name:
                return acc
        raise KeyError(f'{id_or_name} not found')

    def __getitem__(self, index):
        return self.get()[index]

    def __delitem__(self, __key):
        raise NotImplemented

    def __call__(self, *args, **kwds):
        return self.get()

