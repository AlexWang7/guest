#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/19 15:41
# @Author  : wxn
# @Site    : 
# @File    : get_event_list_test.py
# @Software: PyCharm
# @Describe: 测试带用户认证的接口
import base64

signMsg='8SxTqK29bsy7cJJUzKMqWaj5zJYKKVbou4IYL5OXil7OMuuaw5Ok1i4TbHjk3y%2FVS5pYlXHpMHUiwxUFbGdf53bviS4QseuRGjHApFvaYH7sD3wtqMKgiP637C%2FBLBgIvyQhNoC4ugXTTNjDP7dspg6WzlkonW52uP0Aint%2FhV0%3D'
auth_parts = base64.b64decode(signMsg).decode('iso-8859-1').partition(':')
print(auth_parts)