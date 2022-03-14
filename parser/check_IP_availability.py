#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Tang Zhuangkun

import sys
sys.path.append("..")
# import log.custom_logger as custom_logger
import requests


class CheckIPAvailability:
	# 检查单个IP的活性
	
	def __init__(self):
		pass
		
		
	def check_single_ip_availability(self,ip):
		'''
		输入单个IP，检测IP格式及活性, 是否仍然有效
		:param ip: 地址+端口号 例如 61.145.48.100:9999
		:return:符合HTTP 还是HTTPS协议， 是否存活，
		# 0，代表不符合且不存活； 如果是1 代表符合且存活
		如 {'is_https': 0, 'is_http': 0}
		'''

		# 是否符合 符合HTTP 还是HTTPS协议， 默认0，代表不符合； 如果是1 代表符合
		result = dict()
		result["is_https"] = 0
		result["is_http"] = 0

		# 监测是否符合 https 或者 http协议
		is_https = self.is_https_protocol(ip)
		is_http = self.is_http_protocol(ip)

		if(is_https):
			result["is_https"] = 1
		if(is_http):
			result["is_http"] = 1

		return result

	def is_https_protocol(self, ip):
		'''
		输入单个IP，检测IP活性, 是否为https,是否仍然有效
		:param ip: 地址+端口号 例如 61.145.48.100:9999
		:return: true: 符合http协议，且存活； false：不符合http协议，且不存活；
		'''

		# 请求响应头
		headers = {
			"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36"}

		# 再检测列表中IP活性
		try:
			proxy = {"https": "https://" + ip}
			url = "https://pv.sohu.com/cityjson?ie=utf-8"
			# 设定timeout=1,即在1秒内，未收到响应就断开连接
			res = requests.get(url=url, proxies=proxy, headers=headers, stream=True, timeout=1)
			res.encoding = "utf-8"
			# 查看请求的IP
			ip_and_port = res.raw._connection.sock.getpeername()
			print("https ip: " + ip + "    ip_and_port " + str(ip_and_port))
			return True
		except BaseException as e:
			# 日志记录
			msg = ip + " 不可用，不符合http协议 " + str(e)
			# custom_logger.CustomLogger().log_writter(msg,lev="debug")
			return False


	def is_http_protocol(self, ip):
		'''
		输入单个IP，检测IP活性, 是否为http,是否仍然有效
		:param ip: 地址+端口号 例如 61.145.48.100:9999
		:return: true: 符合http协议，且存活； false：不符合http协议，且不存活；
		'''

		# 请求响应头
		headers = {
			"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.124 Safari/537.36"}

		# 再检测列表中IP活性
		try:
			proxy = {"http": "http://" + ip}
			url = "http://icanhazip.com/"
			# 设定timeout=1,即在1秒内，未收到响应就断开连接
			res = requests.get(url=url, proxies=proxy, headers=headers, stream=True, timeout=1)
			res.encoding = "utf-8"
			# 查看请求的IP
			ip_and_port = res.raw._connection.sock.getpeername()
			print("http ip: " + ip + "    ip_and_port " + str(ip_and_port))
			return True
		except BaseException as e:
			# 日志记录
			msg = ip + " 不可用，不符合http协议 " +str(e)
			# custom_logger.CustomLogger().log_writter(msg,lev="debug")
			return False
	

if __name__ == "__main__":
	go = CheckIPAvailability()
	result = go.check_single_ip_availability("120.42.46.226:6666")
	print(result)