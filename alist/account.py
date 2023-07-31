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
    描述Alist账户信息。不同账户需要的信息各不相同。
    更详细的信息请参考 :class:`AlistAdminDrivers <alist.driver.AlistAdminDrivers>`。
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
    ``/api/admin/account`` API的实现。创建、删除、修改账号。
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
        创建一个Onedrive账号。

        :param name: 账号名字。即虚拟地址。
        :param zone: 区域。可以是 ``global``、``cn``、``us`` 或 ``de``。
        :param internal_type: ``onedrive`` 或 ``sharepoint``。
        :param client_id: client id
        :param client_secret: client secret
        :param redirect_uri: 重定向URI
        :param refresh_token: 刷新token
        :param proxy: 是否开启代码。默认为False。
        :param webdav_proxy: 默认为False。
        :param webdav_direct: 默认为False。
        :param down_proxy_url: 可选参数，默认为None。
        :param extract_folder: 可选参数，默认为None。可以填 ``front`` 或 ``back``。
        :param site_id: 可选参数。sharepoint站点ID。默认为None。
        :param root_folder: 可选参数。根目录路径。默认为None。
        :param order_by: 可选参数。排序依据。默认为None。可以填 ``name``、``size`` 、``lastModifiedDateTime``。
        :param order_direction: 可选参数。排序方向。默认为None。可以填 ``asc`` 或 ``desc``。
        :return: 创建成功返回True。否则触发异常。
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
        创建一个本地账号。

        .. code-block:: python

            client.admin.account.create_Native('/native_tmp', '/tmp')

        :param name: 账号名字。即虚拟地址。
        :param root_folder: 根目录路径。
        :param webdav_direct: 默认为False。
        :param down_proxy_url: 可选参数，默认为None。
        :param extract_folder: 可选参数，默认为None。可以填 ``front`` 或 ``back``。
        :param order_by: 可选参数。排序依据。默认为None。可以填 ``name``、``size`` 、``lastModifiedDateTime``。
        :param order_direction: 可选参数。排序方向。默认为None。可以填 ``asc`` 或 ``desc``。
        :return: 创建成功返回True。否则触发异常。
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

        .. code-block:: python

            client.admin.account.create_Alist('/another_alist', 'http://alist.xxxx.com', 'xxxxxx')

        :param name: 账号名字。即虚拟地址。
        :param site_url: Alist网站的URL。
        :param access_token: 访问网站的token。
        :param proxy: 是否开启代码。默认为False。
        :param webdav_proxy: 默认为False。
        :param webdav_direct:  默认为False。
        :param down_proxy_url: 可选参数，默认为None。
        :param extract_folder: 可选参数，默认为None。可以填 ``front`` 或 ``back``。
        :param root_folder: 可选参数。根目录路径。
        :return: 创建成功返回True。否则触发异常。
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
        """
        删除一个账户。

        .. code-block:: python

            client.admin.account.delete('/another_alist')

        :param name: 账号名字。即虚拟地址。
        :return: 删除成功返回True。否则触发异常。
        """
        account = self.alist.admin.accounts.get_account(name)
        return self._delete(account['id'])

    def save(self, account: AlistAccount):
        """
        保存修改后的账户。

        .. code-block:: python

            # 首先获取已有的账号。
            account = client.admin.accounts.get_account('/native_tmp')
            # 将 root_folder 修改为 /var
            account['root_folder'] = '/var'
            # 保存
            client.admin.account.save(account)

        :param account: 修改后的账号。
        :return: 修改成功返回True。否则触发异常。
        """
        endpoint = f'{self.endpoint}/save'
        return self.alist.post(endpoint, json = account)

class AlistAdminAccounts(object):
    """
    alist账号列表。获取账号。
    """
    accounts = list()
    def __init__(self, alist, endpoint):
        self.alist = alist
        self.endpoint = f'{endpoint}/accounts'
        self.accounts = deepcopy(self.accounts)

    def get(self) -> list:
        """
        获取账号列表。

        .. code-block:: python

            accounts = client.admin.accounts.get()
            # or
            accounts = client.admin.accounts()

        :return: 账号列表。:class:`AlistAccount <alist.account.AlistAccount>` 组成的列表。
        """
        self.accounts.clear()

        results = self.alist.get(self.endpoint)
        for r in results:
            self.accounts.append(AlistAccount(**r))
        return self.accounts

    def get_account(self, id_or_name) -> AlistAccount:
        """
        根据账号ID或名字获取账号。

        :param id_or_name: 账号ID或名字。
        :return: 账号。
        """
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

