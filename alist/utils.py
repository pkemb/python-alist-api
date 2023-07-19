#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng

import time
from datetime import datetime
import hashlib

def get_timestamp():
    now = time.time()
    timestamp = datetime.fromtimestamp(now)
    tz = time.strftime('%z')[0:3] + ':00'
    return timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f000') + tz

def calc_authorization(password):
        """ 根据密码计算出 authorization
        :param password: 登录密码
        :returns: authorization
        """
        magic = f'https://github.com/Xhofe/alist-{password}'
        return hashlib.md5(magic.encode('utf8')).hexdigest()
