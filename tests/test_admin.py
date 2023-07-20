#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng

import pytest

def test_settings_get(client):
    settings = client.admin.settings.get()
    assert len(settings) != 0

def test_settings_frontend(client):
    settings = client.admin.settings.frontend()
    assert len(settings) != 0

def test_settings_backend(client):
    settings = client.admin.settings.backend()
    assert len(settings) != 0

def test_settings_other(client):
    settings = client.admin.settings.other()
    assert len(settings) != 0

def test_settings_enable_search(client):
    enable_search = client.admin.setting_enable_search()
    assert enable_search in ['true', 'false']

def test_settings_update(client):
    enable_search = client.admin.setting_enable_search()
    old_value = enable_search
    new_value = 'false' if old_value == 'true' else 'true'

    assert client.admin.setting_enable_search(new_value) == new_value
    assert client.admin.setting_enable_search(old_value) == old_value

def test_settings_save(client):
    setting = client.admin.settings.get_setting('enable search')

    old_value = setting['value']
    new_value = 'false' if old_value == 'true' else 'true'

    setting['value'] = new_value
    assert client.admin.settings.save([setting]) == True
    assert client.admin.setting_enable_search() == new_value

    setting['value'] = old_value
    assert client.admin.settings.save([setting]) == True
    assert client.admin.setting_enable_search() == old_value




def test_drivers_get(client):
    drivers = client.admin.drivers.get()
    assert len(drivers) > 0

def test_drivers_get_driver(client):
    driver = client.admin.drivers.get_driver('Native')
    assert driver != None




def test_accounts_get(client):
    # 可能没有设置账号
    accounts = client.admin.accounts.get()
    assert accounts != None

account_name = '/__test_native'

def test_account_create(client):
    r = client.admin.account.create_Native(account_name, '/tmp')
    assert r == True

@pytest.mark.run(after='test_account_create')
def test_accounts_get_account(client):
    account = client.admin.accounts.get_account(account_name)
    assert account != None

@pytest.mark.run(after='test_accounts_get_account')
def test_accounts_save(client):
    account = client.admin.accounts.get_account(account_name)
    new_webdav_direct = not account['webdav_direct']

    account['webdav_direct'] = new_webdav_direct
    assert client.admin.account.save(account) == True

    new_account = client.admin.accounts.get_account(account_name)
    assert new_account['webdav_direct'] == new_webdav_direct

@pytest.mark.run(after='test_accounts_save')
def test_accounts_delete(client):
    r = client.admin.account.delete(account_name)
    assert r == True




meta_path = '/__test_meta_path__'

def test_metas_get(client):
    metas = client.admin.metas.get()
    assert metas != None

def test_meta_create(client):
    r = client.admin.meta.create(meta_path)
    assert r == True

@pytest.mark.run(after='test_meta_create')
def test_metas_get_meta(client):
    meta = client.admin.metas.get_meta(meta_path)
    assert meta != None

@pytest.mark.run(after='test_metas_get_meta')
def test_meta_save(client):
    meta = client.admin.metas.get_meta(meta_path)
    new_upload = not meta['upload']

    meta['upload'] = new_upload
    r = client.admin.meta.save(meta)
    assert r == True

    new_meta = client.admin.metas.get_meta(meta_path)
    assert new_meta['upload'] == new_upload

@pytest.mark.run(after='test_meta_save')
def test_meta_delete(client):
    r = client.admin.meta.delete(meta_path)
    assert r == True



def test_clear_cache(client):
    r = client.admin.clear_cache()
    assert r == True

@pytest.mark.parametrize('path', [('')])
def test_link(client, path):
    pytest.skip()

@pytest.mark.parametrize('path,names', [('', [])])
def test_files(client, path, names):
    pytest.skip()

@pytest.mark.parametrize('path', [('')])
def test_mkdir(client, path):
    pytest.skip()

@pytest.mark.parametrize('path,name', [('', '')])
def test_rename(client, path, name):
    pytest.skip()

@pytest.mark.parametrize('src_dir,dst_dir,names', [('', '', [])])
def test_move(client, src_dir, dst_dir, names):
    pytest.skip()

@pytest.mark.parametrize('src_dir,dst_dir,names', [('', '', [])])
def test_copy(client, src_dir, dst_dir, names):
    pytest.skip()

@pytest.mark.parametrize('path', [('')])
def test_folder(client, path):
    pytest.skip()

@pytest.mark.parametrize('path', [('')])
def test_refresh(client, path):
    pytest.skip()
