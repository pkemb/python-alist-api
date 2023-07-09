#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng
__version__ = "0.0.2"

from requests import Session
from requests import HTTPError
import json
from urllib.parse import urlparse
from alist.public import AlistPublic
from alist.admin import AlistAdmin
import hashlib
import alist.setting


class AlistClient(object):
    """
    Python wrapper for the Alist API.
    """
    def __init__(
        self,
        base_url,
        password = None,
        authorization = None,
        ssl_verify = True,
        cert = None,
    ):
        self.base_url = base_url.rstrip('/')
        self.public = AlistPublic(self)
        self.admin  = None
        self.session = Session()
        self.password = ""
        self.ssl_verify = ssl_verify
        self.cert = cert

        self.url = urlparse(self.base_url)

        self.authorization = None
        self.login(password, authorization)

    def calc_authorization(self, password):
        """ 根据密码计算出 authorization
        :param password: 登录密码
        :returns: authorization
        """
        magic = f'https://github.com/Xhofe/alist-{password}'
        return hashlib.md5(magic.encode('utf8')).hexdigest()

    def login(self, password = None, authorization = None):
        """ 登录
        :returns:
            登录成功返回Ture，登录失败触发异常。
        """
        if self.is_login():
            return True

        self.authorization = authorization
        self.password = password
        if self.password != None and self.authorization == None:
            self.authorization = self.calc_authorization(self.password)

        if self.authorization:
            self.admin = AlistAdmin(self)
            return self.admin.login()
        return False

    def is_login(self):
        """ 是否登录
        :returns:
            如果已登录，返回True；否则返回Flase。
        """
        return self.authorization != None

    @staticmethod
    def decode_response(response):
        """decode a response.
        :returns:
            Decoded JSON content as a dict, or raw text if content could not be
            decoded as JSON.
        :raises:
            requests.HTTPError if the response contains an HTTP error status code.
        """
        content_type = response.headers.get("content-type", "")

        content = response.content.strip()
        if response.encoding:
            content = content.decode(response.encoding)
        if not content:
            return content
        if content_type.split(";")[0] != "application/json":
            return content

        try:
            content = json.loads(content)
        except ValueError:
            raise ValueError(f"Invalid json content: {content}")
        if content['code'] != 200:
            response.status_code = content['code']
            raise HTTPError(content['code'], content['message'], response=response)

        if content['data'] is None:
            return True
        else:
            return content['data']

    def get_request_dict(self, method, endpoint, **kwargs):
        """
        :param kwargs:
        :return:
        """
        headers = {
            "Method": method,
            "Path": self.get_api_url(endpoint),
            "Authority": self.url.hostname,
            "Scheme": self.url.scheme,
            "Accept": "application/json, text/plain, */*",
            "Origin": self.base_url,
            "Authorization": self.authorization,
            # "Content-Type": "application/json;charset=UTF-8", # requests 自动填充
        }
        request_kwargs = kwargs
        if "headers" in request_kwargs:
            request_kwargs["headers"].update(headers)
        else:
            request_kwargs["headers"] = headers
        request_kwargs['verify'] = self.ssl_verify
        request_kwargs['cert']   = self.cert

        return request_kwargs

    def get_api_url(self, endpoint):
        """
        Return the api url including host and port for a given endpoint.
        :param endpoint: service endpoint as str
        :return: api url (including host and port) as str
        """
        return f'/api{endpoint}'

    def get_endpoint_url(self, endpoint):
        """
        Return the complete url including host and port for a given endpoint.
        :param endpoint: service endpoint as str
        :return: complete url (including host and port) as str
        """

        return f'{self.base_url}{self.get_api_url(endpoint)}'

    def get(self, endpoint, **kwargs):
        """
        Send HTTP GET to the endpoint.

        :param endpoint: The endpoint to send to.
        :return:
        """
        request_kwargs = self.get_request_dict("GET", endpoint, **kwargs)
        response = self.session.get(self.get_endpoint_url(endpoint), **request_kwargs)
        return self.decode_response(response)

    def post(self, endpoint, **kwargs):
        """
        Send HTTP POST to the endpoint.

        :param endpoint: The endpoint to send to.
        :return:
        """
        request_kwargs = self.get_request_dict("POST", endpoint, **kwargs)
        response = self.session.post(self.get_endpoint_url(endpoint), **request_kwargs)
        # return response
        return self.decode_response(response)

    def delete(self, endpoint, **kwargs):
        """
        Send HTTP DELETE to the endpoint.

        :param endpoint: The endpoint to send to.
        :return:
        """
        request_kwargs = self.get_request_dict("DELETE", endpoint, **kwargs)
        response = self.session.delete(self.get_endpoint_url(endpoint), **request_kwargs)
        # return response
        return self.decode_response(response)

