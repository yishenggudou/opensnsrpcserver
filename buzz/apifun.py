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

import os,sys
import conf as _conf
from weibopy import OAuthHandler
from lib import *

DIR_PATH = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
NAME_FILE = os.path.relpath(__file__)





__author__ = 'timger & yishenggudou@gmail.com'
__license__ = 'MIT'
__version__ = (0,0,0)



def get_authorization_url(user_name,server_user_name,server_user_pix='timger',server='sina',callback=None,consumer_key=_conf.consumer_key,consumer_secret=_conf.consumer_secret,):
    import sys 
    sys.path.append(os.path.join(DIR_PATH,'../'))
    from db import * 

    o = OAuthHandler(consumer_key, consumer_secret,callback=callback)
    authorization_url = o.get_authorization_url()
    request_token = o.request_token
    print request_token
    sdb = TWDBS(consumer_key=consumer_key,consumer_secret=consumer_secret,request_token=str(request_token))
    session.add(sdb)
    session.commit()
    session.close()
    res = {}
    res['request_token'] = request_token
    res['authorization_url'] = authorization_url
    
    print authorization_url 
    return res

def verify(user_name,server_user_name,verify,server_user_pix='timger',server='sina',callback='/login',consumer_key=_conf.consumer_key,consumer_secret=_conf.consumer_secret,):
    
    import sys 
    sys.path.append(os.path.join(DIR_PATH,'../'))
    from db import * 
    res = {}
    sdb = session.query(TWDBS).filter(TWDBS.consumer_key==consumer_key,TWDBS.consumer_secret==consumer_secret,TWDBS.user_name==user_name,TWDBS.server_user_name==server_user_name,TWDBS.server==server).all()[-1]
    o = OAuthHandler(consumer_key=consumer_key, consumer_secret=consumer_secret,callback=callback)
    request_token_key,request_token_sercet = [ i.split('=')[1]  for i in sdb.request_token.split('&')]
    o.request.token = oauth.OAuthToken(request_token_key,request_token_sercet)
    try:
        access_token = o.get_access_token(verifier)
        sdb.access_token_key = access_token.key
        sdb.access_token_secret = access_token.secret
        sdb.access_token = access_token.to_string()
        res.status = True
    except:
        res['status'] = False
    session.commit()
    session.close()
    return res

def get_api(consumer_key,consumer_sercet,access_token_key,access_token_sercet,access_token,user_name,server_user_name,server='sina'):

    import sys, os.path
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.path.append(os.path.join(DIR_PATH,'../'))
    from weibopy import OAuthHandler, API, WeibopError
    from db import * 
    sdb = session.query(TWDBS).filter(TWDBS.consumer_key==consumer_key,TWDBS.consumer_secret==consumer_secret,TWDBS.user_name==user_name,TWDBS.server_user_name==server_user_name,TWDBS.server==server).all()[-1]
    try:
        o = OAuthHandler(consumer_key, consumer_secret)
        o.setToken(sdb.access_token_key,sdb.access_token_secret)
    except KeyError, e:
        sys.stderr.write("you should run get_oauthed.py first.\n")
    return API(o)

def post(user_name,server_user_name,status,server_user_pix='timger',server='sina',callback='/login',consumer_key=_conf.consumer_key,consumer_secret=_conf.consumer_secret,):

    res = {}
    try:
        o = get_api(consumer_key,consumer_sercet,access_token_key,access_token_sercet,access_token,user_name,server_user_name,server='sina')
        o.update_status(status)
        res['status'] = True
    except:
        res['status'] = False
    return res

def get(user_name,server_user_name,status,server_user_pix='timger',server='sina',callback='/login',consumer_key=_conf.consumer_key,consumer_secret=_conf.consumer_secret,):

    res = {}
    try:
        o = get_api(consumer_key,consumer_sercet,access_token_key,access_token_sercet,access_token,user_name,server_user_name,server='sina')
        res['msgs'] = o.user_timeline(count=10, page=1)
        res['status'] = True
    except:
        res['status'] = False
    return res
    
if __name__ == "__main__":
    print sys.argv
    if sys.argv[1] == 'url':
        get_authorization_url('timger','timger',server_user_pix='timger',server='sina',callback=None,consumer_key=_conf.consumer_key,consumer_secret=_conf.consumer_secret,)
    if sys.argv[1] == 'verify':
        verify('timger','timger',sys.argv[2],server_user_pix='timger',server='sina',callback='/login',consumer_key=_conf.consumer_key,consumer_secret=_conf.consumer_secret)

