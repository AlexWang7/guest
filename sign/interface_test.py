#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/18 17:30
# @Author  : wxn
# @Site    : 
# @File    : interface_test.py
# @Software: PyCharm
# @Describe:web api 测试
import requests

import unittest

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


class GetEventListTest(unittest.TestCase):
    # 查询发布会接口测试
    def setUp(self):
        self.url = "http://127.0.0.1:8002/api/get_event_list"

    def test_get_event_null(self):
        """发布会id为空"""
        r = requests.get(self.url, params={'eid': ''})
        result = r.json()
        print(r)
        self.assertEqual(result['status'], 10021)
        self.assertEqual(result['message'], "parameter error")

    def test_get_event_success(self):
        """发布会id为1，查询成功"""
        r = requests.get(self.url, params={'eid': '1'})
        result = r.json()
        print(result)
        self.assertEqual(result['status'], 200)
        self.assertEqual(result['message'], 'success')
        self.assertEqual(result['data']['name'], '小米发布会')
        self.assertEqual(result['data']['address'], '水立方')
        self.assertEqual(result['data']['start_time'], '2018-09-12T10:04:01Z')


if __name__ == '__main__':
    unittest.main()
