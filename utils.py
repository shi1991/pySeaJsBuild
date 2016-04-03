#!/usr/bin/env python
#coding:utf-8

import time
import urllib
import httplib
import json
import urllib2
from datetime import datetime

def timesince2():
    return '刚刚'

def timesince(dt, default="刚刚"):
    """
    返回人性化，时间字符串。e.g.:
    3 天前, 5小时前 etc.
    """
    now = datetime.utcnow()
    diff = now - dt

    periods = (
        (diff.days / 365, u"年"),
        (diff.days / 30, u"月"),
        (diff.days / 7, u"周"),
        (diff.days, u"天"),
        (diff.seconds / 3600, u"小时"),
        (diff.seconds / 60, u"分钟"),
        (diff.seconds, u"秒"),
    )

    for period, unit in periods:

        if period:
            return u"%d %s前" % (period, unit)

    return default

def timesincestr(dtstr, default="刚刚"):
    """
    返回人性化，时间字符串。e.g.:
    3 天前, 5小时前 etc.
    """
    dt = datetime.strptime(dtstr, "%Y-%m-%d %H:%M:%S.%f")
    now = datetime.utcnow()
    diff = now - dt

    periods = (
        (diff.days / 365, u"年"),
        (diff.days / 30, u"月"),
        (diff.days / 7, u"周"),
        (diff.days, u"天"),
        (diff.seconds / 3600, u"小时"),
        (diff.seconds / 60, u"分钟"),
        (diff.seconds, u"秒"),
    )

    for period, unit in periods:

        if period:
            return u"%d %s前" % (period, unit)

    return default

def pushmsg(platform,msgtype,msg,fromuser,touser):
    data = {}

    if platform == "android":
        #发送给所有人
        if touser == "":
                data = {
                        "data":{
                                "msgtype":msgtype,
                                "alert":msg
                        }
                }
        else:
            data = {
                    "where":{
                              "installationId":str(touser)
                    },
                    "data":{
                            "msgtype":msgtype,
                            "alert":msg,
                            "userid":fromuser
                    }
            }
    elif platform == "ios":
        if touser == "":
                data = {
                        "data":{
                            "ios":{
                                "alert":msg,
                                "badge":"Increment",
                                "msgtype":msgtype,
                                "msgid":fromuser
                            }
                        }
                }
        else:
            #"deviceToken":"a4a23e8818a550a101bc049a965746c3fe4b9dfa6f7259d7524e4571b371b544"
            data = {
                    "where":{
                              "deviceToken":touser
                    },
                    "data":{
                        "ios":{
                            "alert":msg,
                            "badge":"Increment",
                            "msgtype":msgtype,
                            "msgid":fromuser
                        }
                    }
            }

    req = urllib2.Request('https://leancloud.cn/1.1/push')
    req.add_header('Content-Type', 'application/json')
    # if usertype == "doctor":
    #     req.add_header('X-LC-Id', "N2rzkHxFxrRfnWa7TLcKbhPL")
    #     req.add_header('X-LC-Key', "2PD00Q6BM1kG0VlAwCOCe3i3")
    # else:
    req.add_header('X-LC-Id', "dfXMnN2BE5puS6CxONXBuAtI")
    req.add_header('X-LC-Key', "uOcFjgzUvrJJPy9gIXWMgWFn")

    response = urllib2.urlopen(req, json.dumps(data))

    print response
