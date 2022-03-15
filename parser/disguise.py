#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Tang Zhuangkun

import sys
sys.path.append("..")
import public.db_operator as db_operator

class Disguise:
	# 从数据库获取代理IP和用户代理隐匿 
	# 提供两种方法，从数据库中获取一个IP和一个UA  或者 从数据库中获取多个IP和多个UA
	
	def __init__(self):
		pass
	
	def get_one_IP_UA(self, protocol='https'):
		'''
		根据协议类型，从数据库中获取一个IP和一个UA
		:param protocol: 协议类型，默认 https, 也可选择http
		:return: 如 {'ip_address': '218.4.193.22:55834'} {'ua': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.517 Safari/537.36'}
		'''
		
		# 获取IP
		ip_address_sql = None
		if(protocol=='https'):
			ip_address_sql = "SELECT ip_address FROM IP_availability WHERE is_https = 1 ORDER BY RAND() LIMIT 1"
		elif(protocol=='http'):
			ip_address_sql = "SELECT ip_address FROM IP_availability WHERE is_http = 1 ORDER BY RAND() LIMIT 1"
		print(ip_address_sql)
		ip_address = db_operator.DBOperator().select_one('parser_component',ip_address_sql)
		
		# 获取UA
		ua_sql = "SELECT ua FROM fake_user_agent ORDER BY RAND() LIMIT 1"
		ua = db_operator.DBOperator().select_one('parser_component',ua_sql)
		
		return ip_address,ua
		

	def get_multi_IP_UA(self,num,protocol='https'):
		'''
		根据协议类型，从数据库中获取多个IP和多个UA
		:param num: 需要多少个IP和UA
		:param protocol: 协议类型，默认 https, 也可选择http
		:return: 多个IP和多个UA, 可能满足条件的IP会少于num
		如：[{'ip_address': '101.255.125.10:8080'}, {'ip_address': '103.124.89.221:55443'}][{'ua': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36'}, {'ua': 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36'}]
		'''
		
		# 获取多个IP
		ip_address_sql = None
		if (protocol == 'https'):
			ip_address_sql = "SELECT ip_address FROM IP_availability WHERE is_https = 1 LIMIT %s" %(str(num))
		elif (protocol == 'http'):
			ip_address_sql = "SELECT ip_address FROM IP_availability WHERE is_http = 1 LIMIT %s" % (str(num))
		ip_address_dict_list = db_operator.DBOperator().select_all('parser_component',ip_address_sql)

		# 获取多个UA
		ua_sql = "SELECT ua FROM fake_user_agent LIMIT %s" %(str(num))
		ua_dict_list = db_operator.DBOperator().select_all('parser_component',ua_sql)
		
		return ip_address_dict_list,ua_dict_list


if __name__ == "__main__":
	go = Disguise()
	#ip_address,ua = go.get_one_IP_UA('http')
	#print(ip_address,ua)
	ip_address_dict_list,ua_dict_list = go.get_multi_IP_UA(10)
	print(ip_address_dict_list,ua_dict_list)
		