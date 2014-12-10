#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""logger for montanus"""

import logging

# create logger
logger = logging.getLogger('montanus')

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(filename)s:%(lineno)d %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    logger.info('info')
    logger.debug('debug')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')
