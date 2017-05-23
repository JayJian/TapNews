import logging
from logging.handlers import RotatingFileHandler

#create logger
logger = logging.getLogger('tap_news')
logger.setLevel(logging.DEBUG)

fileName = './system_log.log'

logHandler = RotatingFileHandler(fileName, mode='a', maxBytes=0, backupCount=0, encoding=None, delay=0)
logHandler.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
logHandler.setFormatter(formatter)

# add ch to logger
logger.addHandler(logHandler)

# 'application' code
# logger.debug('debug message')
# logger.info('info message')
# logger.warn('warn message')
# logger.error('error message')
# logger.critical('critical message')
