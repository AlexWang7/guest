#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/18 17:30
# @Author  : wxn
# @Site    : 
# @File    : interface_test.py
# @Software: PyCharm
# @Describe:web api 测试
import requests

# 查询发布会接口
url = "http://127.0.0.1:8002/api/get_event_list/"
r = requests.get(url, params={'eid': 1})
result = r.json()
print(result)
assert result['status'] == 200
assert result['message'] == "success"
assert result['data']['name'] == "小米发布会"
assert result['data']['address'] == "水立方"
assert result['data']['start_time'] == "2018-09-12T10:04:01Z"
