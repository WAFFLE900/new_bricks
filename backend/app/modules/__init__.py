#API 會用到的套件裝這！

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from fuzzywuzzy import fuzz
import hashlib
import jwt
import logging
from flask import Flask, jsonify, request, current_app
from time import time
from sqlalchemy import create_engine, text
from models import *
from sqlalchemy.orm import *
from flask_httpauth import HTTPTokenAuth

#資料庫設定
'''
db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_name = os.environ.get('DB_NAME')
'''

db_username = 'bricks'
db_password = 'NCCUgdsc1234!'
db_host = '35.194.196.179'
db_port = '3306'
db_name = 'bricksdata_test'

db_url = f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"
# db_url = f"mysql+pymysql://{db_username}:@{db_host}:{db_port}/{db_name}"
engine = create_engine(db_url, echo=True)
Session=sessionmaker(bind=engine)
session=Session()

#HTTPauth設定
auth = HTTPTokenAuth(scheme='Bearer')
# current_app.config.from_object(__name__)

