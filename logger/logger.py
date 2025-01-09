import logging
import os
import datetime
import sys


# logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("STORE")
consoleHandler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
consoleHandler.setFormatter(formatter)
logger.addHandler(consoleHandler)

logger.setLevel(logging.INFO)

log_directory = f'logger/dblogs/{datetime.date.today()}'
os.makedirs(log_directory, exist_ok=True)
dblogger = logging.getLogger('sqlalchemy.engine')
dblogger.setLevel(logging.DEBUG)
dblogger_file = logging.FileHandler(f'{log_directory}/sqlalchemy{str(datetime.datetime.now().hour)}.log')
dblogger_file.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
dblogger.addHandler(dblogger_file)
