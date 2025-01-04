from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import os
from urllib.parse import quote_plus

import logging

import pymysql
pymysql.install_as_MySQLdb()

dblogger = logging.getLogger('sqlalchemy').setLevel(level=logging.WARNING)

password = quote_plus(os.environ.get('MYSQL_DB_PASS'))
engine = create_engine(f"mysql+pymysql://root:{password}@127.0.0.1:3306/ulmdb")
Base = declarative_base()
