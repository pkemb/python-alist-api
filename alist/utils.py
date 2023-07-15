#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Kai Peng

import time
from datetime import datetime

def get_timestamp():
    now = time.time()
    timestamp = datetime.fromtimestamp(now)
    tz = time.strftime('%z')[0:3] + ':00'
    return timestamp.strftime('%Y-%m-%dT%H:%M:%S.%f000') + tz
