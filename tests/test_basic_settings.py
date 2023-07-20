#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng

import pytest

@pytest.mark.run(order=1)
def test_base_url(base_url):
    assert base_url != None
    assert base_url != ''

@pytest.mark.run(order=1)
def test_password(password):
    assert password != None
    assert password != ''
