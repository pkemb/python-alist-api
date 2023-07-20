#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng

import pytest

@pytest.mark.run(order=2)
def test_password(client_nologin, password):
    r = client_nologin.login(password=password)
    assert r == True
    assert client_nologin.is_login() == True

@pytest.mark.run(order=2)
def test_authorization(client_nologin, authorization):
    r = client_nologin.login(authorization=authorization)
    assert r == True
    assert client_nologin.is_login() == True
