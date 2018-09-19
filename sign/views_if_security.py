#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/9/19 17:05
# @Author  : wxn
# @Site    : 
# @File    : views_if_security.py
# @Software: PyCharm
# @Describe: 接口签名
import hashlib
import time


def user_sign(request):
    client_time = request.POST.get('time', '')
    client_sign = request.POST.get('sign', '')
    if client_sign == '' or client_time == '':
        return "sign null"

    # 服务器时间
    now_time = time.time()
    server_time = str(now_time).split('.')[0]
    # 获取时间差
    time_difference = int(server_time) - int(client_time)
    if time_difference >= 60:
        return "timeout"

    # 签名检查
    md5 = hashlib.md5()
    sign_str = client_time + "&Guest-Bugmaster"
    sign_bytes_utf8 = sign_str.encode(encoding="utf-8")
    md5.update(sign_bytes_utf8)
    sever_sign = md5.hexdigest()
    if sever_sign!=client_sign:
        return "sign error"
    else:
        return "sign right"
