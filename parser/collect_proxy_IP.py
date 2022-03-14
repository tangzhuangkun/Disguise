#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Tang Zhuangkun

import time
import threading
import sys
sys.path.append('..')
import conf
import public.db_operator as db_operator
# import log.custom_logger as custom_logger
import parser.parse_IP_web_content as parse_IP_web_content
import parser.check_IP_availability as check_IP_availability

class CollectProxyIP:
    # 获取IP代理网站上的有用代理IP，并存入数据库parser_component 表 IP_availability
    # 运行频率：每天

    def __init__(self):
        pass

    def collect_web_content(self, db_name, pageNum):
        '''
        # 根据拼接处的网站地址
        # 多线程抓取
        # 挨个地址，挨页解析
        # 将解析出的内容存入数据库

        :param db_name: 创建哪个模块的数据库连接池， 默认应该为 parser_component
        :param pageNum: 抓取每个IP代理网站的前多少页
        :return: 抓取到的IP信息存入数据库
        '''

        # 获取配置文件中的IP代理网站地址
        ip_urls_list = conf.IP_URL_LIST
        
        # 遍历IP代理网站地址
        for url in ip_urls_list:
            # 启用多线程
            collect_web_page_running_threads = []
            # 拼接每个网站前x页的地址
            for pageIndex in range(1,pageNum):

                # 休眠1秒，抓取太快的话，ip代理网站会拒绝返回
                time.sleep(1)
                page_url = url[0]+str(pageIndex)+url[1]
                print(page_url)
                
                # 处理可能出现的ip代理网站链接异常的情况
                # 可抛出异常，然后继续执行
                try:
                    # set(tuple(ip地址:端口号，匿名类型，协议类型) ---- set(tuple(ipAndPort,anonymous_type,protocol),,,)
                    page_proxy_ip_detail_set = parse_IP_web_content.ParseIPWebContent().parse_web_content(page_url)
                    
                    # 检查代理的可用性，并把可用的存入数据库
                    self.check_ip_availability_and_save_to_db(db_name, page_proxy_ip_detail_set)
                    
                    # 日志记录
                    msg = page_url 
                    # custom_logger.CustomLogger().log_writter('Collected '+msg,lev='debug')
                    
                except Exception as e:
                    # 日志记录
                    msg = page_url + '  '+ str(e)
                    # custom_logger.CustomLogger().log_writter(msg, lev='error')


    def check_and_save_single_ip(self, db_name, ip_info):
        '''
        检查单个IP的可用性，可用的话，存入数据库
        :param db_name: db_name,需要插入数据库的名称， 默认应该为 parser_component
        :param ip_info: 单个ip信息的元组，('104.129.194.114:10605', '高匿', 'HTTP')
        :return:
        '''

        # 获取iP
        ip = ip_info[0]
        # ip类型，HTTP，HTTPS 或者 HTTP,HTTPS
        ip_type = ip_info[2]

        # 检查IP可用性
        # 0，代表不符合且不存活； 如果是1 代表符合且存活
        # 如{'is_https': 0, 'is_http': 0}
        result = check_IP_availability.CheckIPAvailability().check_single_ip_availability(ip)
        # SQL 插入语句
        sql = "INSERT INTO IP_availability(ip_address, is_http, is_https) " \
              "VALUES ('%s','%s','%s') " % (ip, result.get("is_http"), result.get("is_https"))
        # 如果 http 或者 https 可用，均存入数据库
        if result.get("is_http")==1 or result.get("is_https")==1:
            # 存入数据库
            db_operator.DBOperator().operate('insert', db_name, sql)

    def check_ip_availability_and_save_to_db(self, db_name, IP_set):
        # db_name,需要插入数据库的名称
        # IP_set,输入一个装有IP信息的set，如 {('104.129.194.114:10605', '高匿', 'HTTP'),,,,}
        # 批量检查输入的ip的可用性，
        # 如果可用，则存入数据库
        
        # 获取当前时间
        #today= time.strftime("%Y-%m-%d", time.localtime())

        # 启用多线程
        running_threads = []

        for ip_info in IP_set:
            #挨个检查IP活性

            # 创建新线程
            running_thread = threading.Thread(target=self.check_and_save_single_ip,
                                              args=(db_name, ip_info))
            running_threads.append(running_thread)

        # 开启新线程
        for mem in running_threads:
            mem.start()

        # 等待所有线程完成
        for mem in running_threads:
            mem.join()
    
    def main(self):
        # 抓取代理IP，存入 数据库 parser_component，抓取每个代理网站的前6页
        self.collect_web_content('parser_component', 6)
        # 日志记录
        msg = '收集完最新的代理IP'
        #  custom_logger.CustomLogger().log_writter(msg, 'info')
    
    
if __name__ == "__main__":
    time_start = time.time()
    go = CollectProxyIP()
    go.main()
    time_end = time.time()
    print('Time Cost: ' + str(time_end - time_start))