#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng

import pytest
from alist import AlistClient
from alist import utils

BASE_URL = ''
PASSWORD = ''

@pytest.fixture
def base_url():
    return BASE_URL

@pytest.fixture
def password():
    return PASSWORD

@pytest.fixture
def authorization():
    return utils.calc_authorization(PASSWORD)

@pytest.fixture
def client_nologin():
    return AlistClient(BASE_URL)

@pytest.fixture
def client():
    return AlistClient(BASE_URL, password=PASSWORD)
