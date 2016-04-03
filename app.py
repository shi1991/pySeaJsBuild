#!/usr/bin/env python
#coding:utf-8


import os
import time
from datetime import datetime,timedelta

import uuid
import hashlib
import base64
import random
import qrcode
from chinese_pinyin import Pinyin

import pymongo
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.options
import tornado.gen
from utils import *
from pymongo import MongoClient
import json
from bson import json_util
from bson.objectid import ObjectId

from tornado import template
from tornado.options import define, options
from tornadomail.message import EmailMessage, EmailMultiAlternatives, EmailFromTemplate

from v2ex.babel.ua import *

define("host", default="http://127.0.0.1", help="host name")
define("port", default=8888, help="run on the given port", type=int)
define("mail_address", default="hello@aventlabs.com", help="mail address")
define("mail_password", default="helloaventlabs", help="mail password")
define("mail_from", default="AventLabs<hello@aventlabs.com>", help="mail address")
define("mail_title", default="[AventLabs]欢迎来到AventLabs", help="mail title")
define("mail_forgot_title", default="[AventLabs]密码重置", help="mail forgot title")
define("mail_message", default="欢迎来到AventLabs", help="mail message")
define("mail_smtp", default="smtp.ym.163.com", help="mail smtp")
define("mail_smtp_port", default=25, help="mail smtp port", type=int)


STATUS = {'NoPay':'1','Cancled':'2', 'Payed':'3', 'Confirm':'4', 'Finish':'5', 'HaveRefund':'6','RefundCommit':'7'}

class Application(tornado.web.Application):

    @property
    def mail_connection(self):
        return EmailBackend(
            options.mail_smtp, options.mail_smtp_port,
            options.mail_address, options.mail_password,
            True,
            template_loader=template.Loader(os.path.join(os.path.dirname(__file__), "tpl"))
        )

    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/index",IndexHandler),

        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "tpl"),
            static_path=os.path.join("static"),
            #xsrf_cookies=True,
            cookie_secret="__AVENTLABS__",
            login_url="/signin",
            debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        # Have one global connection to the DB across all handlers
        client = MongoClient()
        self.db = client.shi

class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def input(self):
        data = dict()
        args = self.request.arguments
        for a in args:
            print a
            data[a] = self.get_argument(a)
        return data

    def dashboard(self):
        cardid = self.get_secure_cookie("current_process_cardid")
        data = dict()
        data['cardid'] = cardid
        if cardid != None and cardid != '':
            data = self.db.people.find_one({"cardid":cardid})

        path = os.path.join(os.path.dirname(__file__), 'portion', 'userentrance.html')
        userfuncs = self.render_string(path,data=data)
        # if userid == '':
            # userfuncs = ''

        path = os.path.join(os.path.dirname(__file__), 'portion', 'dashboard.html')
        home = self.render_string(path,data=data,userfuncs=userfuncs,errormsg='')

        return home

    def member(self):
        username = self.get_secure_cookie("current_user")
        if not username or username == '': return None
        return self.db.staff.find_one({"username":str(username)})

    def validateAdmin(self):
        #确保登录的帐号有权限
        member = self.member()
        if member == None:
           self.redirect('/signin')
        if member['type'] != "admin":
           self.redirect('/')

    def validateManager(self):
        #确保登录的帐号有权限
        member = self.member()
        if member == None:
           self.redirect('/signin')
        if member['type'] != "manager":
           self.redirect('/')

    def timestamp(self):
        timestamp = str(int(time.time()))
        return '?timestamp=' + timestamp

    def createPagination(self , params, totalPages, pageNumber):
        params['totalPages'] = totalPages
        params['pageNumber'] = pageNumber
        # 是否是第一页
        params['isFirst'] = (pageNumber == 1)
        # 是否存在上一页
        params['hasPrevious'] = pageNumber > 1
        # 是否存在下一页
        params['hasNext'] = pageNumber < totalPages
        print params

        startSegmentPageNumber = pageNumber - 2
        endSegmentPageNumber = pageNumber + 2

        if startSegmentPageNumber < 1: startSegmentPageNumber = 1

        if endSegmentPageNumber > totalPages: endSegmentPageNumber = totalPages
        segment = []
        i = startSegmentPageNumber
        for i in range(startSegmentPageNumber, endSegmentPageNumber + 1): segment.append(i);

        params['segment'] = segment
        params['segmentLen'] = len(segment)

class IndexHandler(BaseHandler):
    def get(self):
        print "首页"



class MainHandler(BaseHandler):
    def get(self):
        browser = detect(self.request)
        self.redirect("/index")

class UAHandler(BaseHandler):
    def get(self):
        browser = detect(self.request)
        self.write(browser)



def main():
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
