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
import conf as _conf
from weibopy import OAuthHandler
from lib import *

DIR_PATH = os.path.abspath(os.path.dirname(os.path.realpath(__file__)))
NAME_FILE = os.path.relpath(__file__)





__author__ = 'timger & yishenggudou@gmail.com'
__license__ = 'MIT'
__version__ = (0,0,0)



def get_authorization_url(user_name,server_user_name,server_user_pix='timger',server='sina',callback='/login',consumer_key=_conf.consumer_key,consumer_secret=_conf.consumer_secret,):
    import sys 
    sys.path.append(os.path.join(DIR_PATH,'../'))
    from db import * 

    o = OAuthHandler(consumer_key, consumer_secret)
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



def main():
    c = get_conf()
    o = OAuthHandler(c['consumer_key'], c['consumer_secret'])
    c['authorization_url'] = o.get_authorization_url()
    c['request_token'] = o.request_token
    print c['authorization_url']
    verifier = raw_input('click the url above, then input the verifier: ')
    verifier = verifier.strip()
    c['verifier'] = verifier
    try:
        access_token = o.get_access_token(verifier)
        c['access_token_key'] = access_token.key
        c['access_token_secret'] = access_token.secret
        c['access_token'] = access_token.to_string()
        set_conf(c)
        print 'oauth succeeded'
    except:
        print 'oauth failed'

if __name__ == '__main__':
    #main()
    get_authorization_url('timger','test_timger') 
