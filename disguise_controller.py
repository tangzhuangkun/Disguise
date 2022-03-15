#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Tang Zhuangkun

import sys
sys.path.append('..')
import parser.disguise as disguise
from flask import Flask, jsonify,request
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/get_one_ip_and_ua', methods=['GET'])
def get_one_ip_and_ua():
    '''
    根据协议类型，从数据库中获取一个IP和一个UA
    :param protocol: 协议类型，默认 https, 也可选择http
    :return:
    如 {
    "IP": "117.157.197.18:3128",
    "UA": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36"
    }
    '''
    # 协议类型，默认 https, 也可选择http
    protocol = request.args.get('protocol')

    ip, ua = disguise.Disguise().get_one_IP_UA(protocol)
    # 返回处理成 json格式
    return jsonify({"IP": ip["ip_address"], "UA":ua["ua"]})

@app.route('/get_multi_IP_UA', methods=['GET'])
def get_multi_IP_UA():
    '''
    根据协议类型，从数据库中获取多个IP和多个UA
    :param protocol: 协议类型，默认 https, 也可选择http
    :param num: 需要多少个IP和UA， 实际输出可能比num少
    :return:
    如 {
    "IPs": [
        "113.214.48.5:8000",
        "117.157.197.18:3128",
        "118.190.244.234:3128"
    ],
    "UAs": [
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.60 Safari/537.17",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0",
        "Mozilla/5.0 (Windows NT 6.2; Win64; x64; rv:27.0) Gecko/20121011 Firefox/27.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36"
    ]
}
    '''
    # 协议类型，默认 https, 也可选择http
    num = request.args.get('num')
    # 协议类型，默认 https, 也可选择http
    protocol = request.args.get('protocol')

    # 获取多个IP 和 UA
    ip_address_dict_list,ua_dict_list = disguise.Disguise().get_multi_IP_UA(num,protocol)
    # 将IP和UA从dict转为list，便于输出成json
    ip_address_list = []
    ua_list = []
    for address in ip_address_dict_list:
        ip_address_list.append(address["ip_address"])
    for ua in ua_dict_list:
        ua_list.append(ua["ua"])

    # 返回处理成 json格式
    return jsonify(IPs = ip_address_list, UAs=ua_list)

if __name__ == '__main__':
    app.run()
