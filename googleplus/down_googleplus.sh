#!/bin/bash
#Author: timger <yishenggudou@gmail.com>
#weibo <http://t.sina.com/zhanghaibo>
#@yishenggudou http://twitter.com/yishenggudou
wget http://google-plus-python-starter.googlecode.com/files/google-plus-python-starter.zip
unzip google-plus-python-starter.zip
cp ./google-plus-python-starter/cli/* ./
rm google-plus-python-starter -R
rm google-plus-python-starter.zip
