#!/bin/bash
#Author: timger <yishenggudou@gmail.com>
#weibo <http://t.sina.com/zhanghaibo>
hg clone https://code.google.com/p/buzz-python-client/
cp ./buzz-python-client/buzz.py ./
cp ./buzz-python-client/third_party -R ./
rm ./buzz-python-client -R
