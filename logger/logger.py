import logging
import os
import datetime

logger = logging.getLogger("STORE")
logger.setLevel(logging.INFO)

log_directory = f'logger/dblogs/{datetime.date.today()}'
os.makedirs(log_directory, exist_ok=True)
dblogger = logging.getLogger('sqlalchemy.engine')
dblogger.setLevel(logging.INFO)
dblogger_file = logging.FileHandler(f'logger/dblogs/sqlalchemy{str(datetime.datetime.now().hour)}.log')
dblogger_file.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
dblogger.addHandler(dblogger_file)
