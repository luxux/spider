# -*- coding: utf-8 -*-
# @Author: koosuf
# @Date:   2017-03-17 13:07:50
# @Last Modified by:   koosuf
# @Last Modified time: 2017-03-17 22:20:18
import logging


logger = logging.getLogger('Hosts')
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler('AutoHosts.log')
fh.setLevel(logging.INFO)

# ch = logging.StreamHandler()
# ch.setLevel(logging.INFO)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# ch.setFormatter(formatter)

logger.addHandler(fh)
# logger.addHandler(ch)
