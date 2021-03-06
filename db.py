#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
    Copyright 2011 timger
    
    +Author timger
    +Gtalk&Email yishenggudou@gmail.com
    +Msn yishenggudou@msn.cn
    +Weibo http://t.sina.com/zhanghaibo

    Licensed under the MIT License, Version 2.0 (the "License");
'''

import os
import sys
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DIR_PATH = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
print DIR_PATH
NAME_FILE = os.path.relpath(__file__)
#sys.path[-2:-1]=[DIR_PATH]
#from conf import DBURL, DBTEST
DBURL = "sqlite:///%s/db.db" %DIR_PATH
print DBURL
DBTEST = True

engine = create_engine(DBURL, echo=DBTEST)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class TWDBS(Base):
    __tablename__ = 'TWDBS'

    id = Column(Integer, primary_key=True)
    server_name = Column(String)
    server_user_name = Column(String) #如sina微博的用户名
    server_user_pix = Column(String)    #如sina微博的用户的url后缀
    user_name = Column(String)  #用户对于本系统的标示，当传入全部推送的时候，根据这个字段关联其在本站内拥有的信息,xx_xx[xx网站的xx用户]
    consumer_key = Column(String)
    consumer_secret = Column(String)
    request_token = Column(String)
    access_token_key = Column(String)
    access_token_secret = Column(String)
    access_token = Column(String)
    login_name = Column(String)  #当不是oauth实现的同步的时候有效
    login_passwd = Column(String) #当不是oauth实现的同步方式的时候有效
    
    def __init__(self, server_name='',user_name='',server_user_name='',server_user_pix='',consumer_key='',consumer_secret='',request_token='',access_token_key='',access_token_secret='',access_token='',login_name='',login_passwd=''):
        self.server_name = server_name
        self.user_name = user_name
        self.server_user_name = server_user_name
        self.server_user_pix = server_user_pix 
        self.consumer_key = consumer_key 
        self.consumer_secret = consumer_secret 
        self.request_token = request_token 
        self.access_token_key = access_token_key 
        self.access_token_secret = access_token_secret 
        self.access_token = access_token
        self.login_name = login_name
        self.login_passwd = login_passwd

    def __repr__(self):
        return "<TWDBS('%s','%s', '%s')>" % (self.server_name, self.user_name, self.server_user_pix)


if __name__ == "__main__":
    Base.metadata.create_all(engine) 



