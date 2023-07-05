#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng

from collections.abc import Iterator
import json
from copy import deepcopy

group_front = 0
group_back  = 1
group_other = 2

class AlistSetting(dict):
    content = {
        # 只有 value 是RW，其他都是RO
        "key": None,
        "value": None,
        "description": None,
        "type": None,
        "group": None,
        "access": None,
        "values": None,
        "version": None
    }
    def __init__(self, **kwargs):
        if 'key' not in kwargs:
            raise ValueError("must set \"key\"")

        self.content = deepcopy(self.content)
        for item in kwargs:
            if item in self.content:
                self.content[item] = kwargs[item]

    def __len__(self):
        return 1

    def __getitem__(self, __key):
        if __key in self.content:
            return self.content[__key]
        else:
            raise KeyError(f'key must be in \'{" ".join(self.content.keys())}\'')

    def __setitem__(self, __key, __value):
        if __key != 'value':
            raise KeyError(f'only value allow modify')
        return self.set_value(__value)

    def __delitem__(self, __key):
        raise NotImplementedError("can't delete any item")

    def __iter__(self) -> Iterator:
        yield from self.content.items()

    def __str__(self) -> str:
        return json.dumps(self.content)

    def __repr__(self) -> str:
        return self.__str__()

    def to_dict(self):
        return self.content

    def get_value(self):
        """ 根据设置的类型，对value进行适当的转换，然后返回转换后的值
        :returns:
            转换后的值。
        """
        stype = self.content['type'] # maybe bool, string, text, select
        if stype == 'bool':
            return self.content['value'] == 'true'
        else:
            return self.content['value']

    def set_value(self, new):
        # 根据类型，对新值new进行适当的转换，保存，并返回新值
        """ 根据设置的类型，对新值new进行适当的转换、检查，然后更新值
        :returns:
            新值new。
        """
        stype = self.content['type']
        if stype == 'bool':
            self.content['value'] = 'true' if new else 'false'
        elif stype == 'select':
            if new in self.content['values'].split(','):
                self.content['value'] = new
            else:
                raise ValueError(f"for select setting, value must be {self.content['values']}")
        else:
            self.content['value'] = new
        return self.content['value']


class AlistAaminSettings(object):

    def __init__(self, alist, endpoint):
        self.alist = alist
        self.endpoint = endpoint

    def get(self, group = None):
        """ 获取管理员的设置
        :param group: 获取指定设置组。如果留空，返回所有设置。
        :returns:
            管理员设置信息
        """
        endpoint = f'{self.endpoint}/settings'
        if group is None:
            settings = self.alist.get(endpoint)
        else:
            settings = self.alist.get(endpoint, params = {'group': group})

        return [AlistSetting(**s) for s in settings]

    def __call__(self, group = None):
        return self.get(group)

    def frontend(self):
        return self.get(group=self.group_front)

    def backend(self):
        return self.get(group=self.group_back)

    def other(self):
        return self.get(group=self.group_other)

    def get_by_key(self, key):
        settings = self.get()
        for s in settings:
            if s['key'] == key:
                return s
        raise KeyError(f'setting \'{key}\' not found')

    def save(self, settings):
        """ 保存设置
        :param settings: AlistSetting列表
        :returns:
            保存成功返回True
        """
        endpoint = f'{self.endpoint}/settings'
        return self.alist.post(endpoint, json=[s.to_dict() for s in settings])

    def _get_or_update(self, key, new = None):
        """ 获取或更新设置的值，内部API
        :param key:
        :param new:
        :returns:
            设置的值
        """
        s = self.get_by_key(key)
        old = s.get_value()
        if new is None or new == old:
            return old
        else:
            s.set_value(new)
            self.save([s])
            return new

    def version(self):
        """只读设置
        """
        return self._get_or_update('version')

    def title(self, new = None):
        return self._get_or_update('titile', new)

    def logo(self, new = None):
        return self._get_or_update('logo', new)

    def favicon(self, new = None):
        return self._get_or_update('favicon', new)

    def icon_color(self, new = None):
        return self._get_or_update('icon color', new)

    def announcement(self, new = None):
        return self._get_or_update('announcement', new)

    def text_types(self, new = None):
        return self._get_or_update('text types', new)

    def audio_types(self, new = None):
        return self._get_or_update('audio types', new)

    def video_types(self, new = None):
        return self._get_or_update('video types', new)

    def hide_files(self, new = None):
        return self._get_or_update('hide files', new)

    def music_cover(self, new = None):
        return self._get_or_update('music cover', new)

    def site_beian(self, new = None):
        return self._get_or_update('site beian', new)

    def global_readme_url(self, new = None):
        return self._get_or_update('global readme url', new)

    def pdf_viewer_url(self, new = None):
        return self._get_or_update('pdf viewer url', new)

    def autoplay_video(self, new = None):
        return self._get_or_update('autoplay video', new)

    def autoplay_audio(self, new = None):
        return self._get_or_update('autoplay audio', new)

    def customize_head(self, new = None):
        return self._get_or_update('customize head', new)

    def customize_body(self, new = None):
        return self._get_or_update('customize body', new)

    def home_emoji(self, new = None):
        return self._get_or_update('home emoji', new)

    def animation(self, new = None):
        return self._get_or_update('animation', new)

    def artplayer_whitelist(self, new = None):
        return self._get_or_update('artplayer whitelist', new)

    def artplayer_autoSize(self, new = None):
        return self._get_or_update('artplayer autoSize', new)

    def artplayer_autoSize(self, new = None):
        return self._get_or_update('artplayer autoSize', new)

    def load_type(self, new = None):
        return self._get_or_update('load type', new)

    def default_page_size(self, new = None):
        return self._get_or_update('default page size', new)


    def password(self, new = None):
        return self._get_or_update('password', new)

    def d_proxy_types(self, new = None):
        return self._get_or_update('d_proxy types', new)

    def check_parent_folder(self, new = None):
        return self._get_or_update('check parent folder', new)

    def check_down_link(self, new = None):
        return self._get_or_update('check down link', new)

    def WebDAV_username(self, new = None):
        return self._get_or_update('WebDAV username', new)

    def WebDAV_password(self, new = None):
        return self._get_or_update('WebDAV password', new)

    def Visitor_WebDAV_username(self, new = None):
        return self._get_or_update('Visitor WebDAV username', new)

    def Visitor_WebDAV_password(self, new = None):
        return self._get_or_update('Visitor WebDAV password', new)

    def ocr_api(self, new = None):
        return self._get_or_update('ocr api', new)

    def enable_search(self, new = None):
        return self._get_or_update('enable search', new)

    def Aria2_RPC_url(self, new = None):
        return self._get_or_update('Aria2 RPC url', new)

    def Aria2_RPC_secret(self, new = None):
        return self._get_or_update('Aria2 RPC secret', new)


    def delete(self):
        endpoint = f'{endpoint}/setting'
        pass

class AlistPublicSettings(object):
    def __init__(self, alist, endpoint):
        self.alist = alist
        self.endpoint = endpoint

    def get(self, group = None):
        """ 获取公开的设置
        :returns:
            公开的设置
        """
        endpoint = f'{self.endpoint}/settings'
        settings = self.alist.get(endpoint)
        return [AlistSetting(**s) for s in settings]

    def __call__(self, group = None):
        return self.get(group)

    def get_by_key(self, key):
        settings = self.get()
        for s in settings:
            if s['key'] == key:
                return s
        raise KeyError(f'setting \'{key}\' not found')

    def version(self):
        return self.get_by_key('version').get_value()

    def title(self):
        return self.get_by_key('title').get_value()

    def logo(self):
        return self.get_by_key('logo').get_value()

    def favicon(self):
        return self.get_by_key('favicon').get_value()

    def icon_color(self):
        return self.get_by_key('icon color').get_value()

    def announcement(self):
        return self.get_by_key('announcement').get_value()

    def text_types(self):
        return self.get_by_key('text types').get_value()

    def audio_types(self):
        return self.get_by_key('audio types').get_value()

    def video_types(self):
        return self.get_by_key('video types').get_value()

    def hide_files(self):
        return self.get_by_key('hide files').get_value()

    def music_cover(self):
        return self.get_by_key('music cover').get_value()

    def site_beian(self):
        return self.get_by_key('site beian').get_value()

    def global_readme_url(self):
        return self.get_by_key('global readme url').get_value()

    def pdf_viewer_url(self):
        return self.get_by_key('pdf viewer url').get_value()

    def autoplay_video(self):
        return self.get_by_key('autoplay video').get_value()

    def autoplay_audio(self):
        return self.get_by_key('autoplay audio').get_value()

    def home_emoji(self):
        return self.get_by_key('home emoji').get_value()

    def animation(self):
        return self.get_by_key('animation').get_value()

    def check_down_link(self):
        return self.get_by_key('check down link').get_value()

    def artplayer_whitelist(self):
        return self.get_by_key('artplayer whitelist').get_value()

    def artplayer_autoSize(self):
        return self.get_by_key('artplayer autoSize').get_value()

    def load_type(self):
        return self.get_by_key('load type').get_value()

    def default_page_size(self):
        return self.get_by_key('default page size').get_value()

    def enable_search(self):
        return self.get_by_key('enable search').get_value()

    def no_cors(self):
        return self.get_by_key('no cors').get_value()

    def no_upload(self):
        return self.get_by_key('no upload').get_value()

