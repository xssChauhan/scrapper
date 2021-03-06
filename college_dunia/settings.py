# -*- coding: utf-8 -*-
# Scrapy settings for college_dunia project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'college_dunia'
USER_AGENT = "Googlebot/2.1 (+http://www.googlebot.com/bot.html)"
SPIDER_MODULES = ['college_dunia.spiders']
NEWSPIDER_MODULE = 'college_dunia.spiders'
CONCURRENT_REQUESTS = 100
LOG_LEVEL = 'INFO'
# DOWNLOAD_DELAY = 100
ITEM_PIPELINES = {'college_dunia.pipelines.InstituteDBPipeline' : 1 }
