#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/19 16:25
# @Author  : wxn
# @Site    : 
# @File    : md5_test.py
# @Software: PyCharm
# @Describe: 加密

import hashlib

md5=hashlib.md5()
sign_str="@admin123"
sign_bytes_utf8=sign_str.encode(encoding="utf-8")
md5.update(sign_bytes_utf8)
sign_md5=md5.hexdigest()
print(sign_md5)
