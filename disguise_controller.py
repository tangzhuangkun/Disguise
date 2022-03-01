#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Tang Zhuangkun

import sys
sys.path.append('..')
import parser.disguise as disguise
from flask import Flask, jsonify
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/get_one_ip_and_ua', methods=['GET'])
def get_one_ip_and_ua():
    '''
    获取一个IP和一个UA
    :return:
    返回例如：{'ip_address': '218.4.193.22:55834'} {'ua': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'}
    '''
    ip, ua = disguise.Disguise().get_one_IP_UA()
    # 返回处理成 json格式
    return jsonify({"ip": ip["ip_address"], "ua":ua["ua"]})

if __name__ == '__main__':
    app.run()
