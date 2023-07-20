#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng

import pytest

def test_path(client):
    assert client.public.path('/') != None

@pytest.mark.parametrize('path', [('')])
def test_preview(client, path):
    pytest.skip()

@pytest.mark.parametrize('path,keyword', [('', '')])
def test_search(client, path, keyword):
    pytest.skip()

@pytest.mark.parametrize('files,path', [([], '')])
def test_upload(client, files, path):
    pytest.skip()

def test_settings(client):
    r = client.public.settings.get()
    assert len(r) > 0

    r = client.public.settings.get_setting('version')
    assert r != None

    r = client.public.setting_version()
    assert r != None

