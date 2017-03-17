#!python3
# -*- coding: utf-8 -*-
# @Author: koosuf
# @Date:   2017-03-17 12:00:21
# @Last Modified by:   koosuf
# @Last Modified time: 2017-03-17 22:22:27

import os
import sys
import shutil
import requests
import platform
import configparser
from log import logger

config_path = 'hostconfig.ini'


def check_system():
    global hosts_folder
    global hosts_location
    if platform.system() == 'Windows':
        hosts_folder = os.environ['SYSTEMROOT'] + "\\System32\\drivers\\etc\\"
    elif platform.system() == 'Linux' or platform.system() == 'Darwin':
        hosts_folder = "/etc/"
    else:
        sys.exit()
    hosts_location = hosts_folder + "hosts"


def backup_hosts():
    try:
        if (not os.path.isfile(hosts_folder + 'hosts.backup')) and \
                os.path.isfile(hosts_folder + 'hosts'):
            shutil.copy(hosts_folder + 'hosts', hosts_folder +
                        'hosts.backup')
        if os.path.isfile(hosts_folder + 'hosts'):
            shutil.copy(hosts_folder + 'hosts', hosts_folder +
                        'hosts.backup')
    except BaseException as e:
        logger.error(str(e))
        sys.exit()


def download_hosts():
    try:
        hosts = open("hosts", "a")
        for url in host_url_list:
            data = requests.get(url)
            hosts.write(data.text)
    except BaseException as e:
        logger.info(str(e))


def get_config():
    global host_url_list
    if os.path.exists('hostconfig.ini'):
        try:
            config = configparser.ConfigParser()
            # 配置有BOM(如Windows下用记事本指定为utf-8带中文的)，就需要这个utf-8-sig
            config.read('hostconfig.ini', encoding="utf-8-sig")
            source_id = config.get('source_urls', 'source_id')
            host_url_list = source_id.split(",")
            for i in range(len(host_url_list)):
                host_url_list[i] = config.get(
                    'source_urls', 'source' + str(i))
        except BaseException as e:
            logger.error(str(e))
            sys.exit()


def move_hosts():
    try:
        shutil.move("hosts", hosts_location)
    except BaseException as e:
        logger.error(str(e))
        sys.exit()

if __name__ == '__main__':
    check_system()
    backup_hosts()
    get_config()
    download_hosts()
    move_hosts()
