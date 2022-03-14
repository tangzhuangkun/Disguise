#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Tang Zhuangkun

import time
import sys
sys.path.append('..')
import public.db_operator as db_operator
# import log.custom_logger as custom_logger
import threading
import parser.check_IP_availability as check_ip_availability


class CheckSavedIPAvailability:
	# 检查数据库中保存的所有IP的可用性
	# 不可用的删除掉
	# 运行频率：每天
	
	def __init__(self):
		pass
		
	def get_all_db_IPs(self,db_name):
		# 获取所有的存量IP
		# db_name: 需要查询数据库的名称， 来自 db_config.py 的 DATABASES
		# 输出：IP_dict_list，如[{'ip_address': '95.216.228.204:3128'},,,,]
		
		# sql query查询所有已存的ip地址		
		sql = "SELECT ip_address from IP_availability"
		# 从数据库取出
		IP_dict_list = db_operator.DBOperator().select_all(db_name,sql)
		
		return IP_dict_list
		
	def update_ip_status(self,db_name,ip, result):
		'''
		更新ip状态
		:param db_name: 需要查询数据库的名称,默认应该为 parser_component
		:param ip: 地址+端口号 例如 61.145.48.100:9999
		:param result: 如 {'is_https': 0, 'is_http': 0}， 0，代表不符合且不存活； 如果是1 代表符合且存活
		:return:
		'''
		
		#更新ip状态
		sql = "UPDATE IP_availability SET is_https = {is_https}, is_http = {is_http} where ip_address = " \
			  "'{ip}'".format(is_https=result.get("is_https"), is_http=result.get("is_http"), ip=ip)
		print(sql)
		db_operator.DBOperator().operate('update', db_name, sql)
		
		# 日志记录	
		msg = sql
		# CustomLogger().log_writter(msg,'debug')
		
	
	def check_ip_availability_and_update_IP_status_on_DB(self,db_name,IP_dict_list):
		'''
		检查查询到的所有ip的可用性，如果不可用，则在数据库中更新状态
		:param db_name: 需要查询数据库的名称,默认应该为 parser_component
		:param IP_dict_list: 输入的是一个list，里面装有dict，形式如：[{'ip_address': '1.24.185.60:9999'}, ,,,]
		:return:
		'''

		# 遍历这些IP
		for ip_dict in IP_dict_list:
			#result 如 {'is_https': 0, 'is_http': 0}， 0，代表不符合且不存活； 如果是1 代表符合且存活
			result = check_ip_availability.CheckIPAvailability().check_single_ip_availability(ip_dict['ip_address'])
			print(ip_dict['ip_address'], result)
			print()
			# 更新已存储的IP存活状态
			self.update_ip_status(db_name, ip_dict['ip_address'],result)
				
	def multiple_threading_checking_saved_ips(self,db_name):
		'''
		# 多线程检查数据库中ip的有效性
		:param db_name: 需要查询数据库的名称,默认应该为 parser_component
		:return:
		'''

		# 数据库中输出的是一个list，里面装有dict，形式如：[{‘ip_address’:'61.145.48.100:9999'},,,,,]
		IP_dict_list = self.get_all_db_IPs('parser_component')
		
		# 数据库中查询到的ip平均分成多份，每份至多处理15个
		every_section_has_ip_num = 15
		
		divided_ips_list_into_sections = []
		# 将查询到的ip分成以每个子list存有最多10个ip的大list   [[10个ip],[10个ip]...]
		for i in range(0, len(IP_dict_list), every_section_has_ip_num):
			divided_ips_list_into_sections.append(IP_dict_list[i:i + every_section_has_ip_num])	
		
		# 启用多线程
		running_threads = []
		for section_index in range(len(divided_ips_list_into_sections)):
			# 创建新线程
			running_thread = threading.Thread(target=self.check_ip_availability_and_update_IP_status_on_DB,args=(db_name,divided_ips_list_into_sections[section_index]))
			running_threads.append(running_thread)	
		
		# 开启新线程
		for mem in running_threads:
			mem.start()
			
		# 等待所有线程完成
		for mem in running_threads:
			mem.join()
		
		# 日志记录	
		msg = "Checked all saved IPs in multiple threading way "
		# custom_logger.CustomLogger().log_writter(msg,'info')
	
	
	def main(self):
		self.multiple_threading_checking_saved_ips('parser_component')
		# 日志记录
		msg = 'Just checked saved IPs availability'
		# custom_logger.CustomLogger().log_writter(msg, 'info')


if __name__ == "__main__":
	time_start = time.time()
	go = CheckSavedIPAvailability()
	go.main()
	time_end = time.time()
	print('Time Cost: ' + str(time_end - time_start))
		