# coding=utf8

"""logger for montanus"""

from utils import colored

import logging
import sys
from logging import Formatter
from logging import getLogger
from logging import StreamHandler
from datetime import datetime


class ColoredFormatter(Formatter):
    """colored output formatter"""

    def format(self, record):
        message = record.getMessage()

        mapping = {
            'CRITICAL': 'bgred',
            'ERROR': 'red',
            'WARNING': 'yellow',
            'SUCCESS': 'green',
            'INFO': 'cyan',
            'DEBUG': 'bggrey',
        }
        color = mapping.get(record.levelname, 'white')

        level = colored('%-8s' % record.levelname, color)
        time = colored(datetime.now().strftime("(%H:%M:%S)"), "magenta")
        return " ".join([level, time, message])


logger = getLogger('montanus')

# Add level 'success'
logging.SUCCESS = 25  # 25 is between WARNING(30) and INFO(20)
logging.addLevelName(logging.SUCCESS, 'SUCCESS')
logger.success = lambda msg, *args, **kwargs: logger.log(logging.SUCCESS, msg, *args, **kwargs)

# Add colored handler
handler = StreamHandler(sys.stdout)
formatter = ColoredFormatter()
handler.setFormatter(formatter)
logger.addHandler(handler)


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    logger.info('info')
    logger.success('success')
    logger.debug('debug')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')
