#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng
__version__ = "0.0.1"

from requests import Session
from requests import HTTPError
import json
from urllib.parse import urlparse
from alist.public import AlistPublic
from alist.admin import AlistAdmin

class AlistClient(object):
    """
    Python wrapper for the Alist API.
    """
    def __init__(
        self,
        base_url
    ):
        self.base_url = base_url.rstrip('/')
        self.public = AlistPublic(self)
        self.admin  = AlistAdmin(self)
        self.session = Session()
        self.password = ""

        self.url = urlparse(self.base_url)

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
            # raise HTTPError(content['message'], code=content['code'], response=response)
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
            "Content-Type": "application/json;charset=UTF-8",
        }
        request_kwargs = kwargs
        if "headers" in request_kwargs:
            request_kwargs["headers"].update(headers)
        else:
            request_kwargs["headers"] = headers
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

