#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# author: Tang Zhuangkun

from apscheduler.schedulers.blocking import BlockingScheduler
import sys
sys.path.append('..')
import parser.collect_proxy_IP as collect_proxy_IP
import parser.generate_save_user_agent as generate_save_user_agent
import parser.check_saved_IP_availability as check_saved_IP_availability


class Scheduler:
    # 任务调度器，根据时间安排工作
    def __init__(self):
        pass

    def schedule_plan(self):
        # 调度器，根据时间安排工作
        scheduler = BlockingScheduler()

        #####################  每日运行 ###################################################

        try:
            # 每半个小时检查已存储的IP的可用性，删除不可用的
            scheduler.add_job(func=check_saved_IP_availability.CheckSavedIPAvailability().main, trigger='cron',
                              month='1-12', day_of_week='mon,tue,wed,thu,fri,sat,sun', hour='0-23', minute='0,30',
                              id='CheckSavedIPAvailabilityEveryHalfHour')
        except Exception as e:
            # 抛错
            # custom_logger.CustomLogger().log_writter(e, 'error')
            pass

        try:
            # 每半个小时收集代理IP
            scheduler.add_job(func=collect_proxy_IP.CollectProxyIP().main, trigger='cron',
                              month='1-12', day_of_week='mon,tue,wed,thu,fri,sat,sun', hour='0-23', minute='0,30',
                              id='CollectProxyIPEveryHalfHour')
        except Exception as e:
            # 抛错
            # custom_logger.CustomLogger().log_writter(e, 'error')
            pass


        #####################   每周运行 ###################################################
        try:
            # 每个星期天晚上23:00重新生成一批假的user_agent
            scheduler.add_job(func=generate_save_user_agent.GenerateSaveUserAgent().main, trigger='cron',
                              month='1-12', day_of_week='sun', hour=23,
                              id='sundayGenerateFakeUserAgent')
        except Exception as e:
            # 抛错
            # custom_logger.CustomLogger().log_writter(e, 'error')
            pass

        # 启动调度器
        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass

if __name__ == "__main__":
    go = Scheduler()
    go.schedule_plan()