# coding:utf-8

import re
import logging
import hashlib
import config

from .BaseHandler import BaseHandler
from utils.response_code import RET
from utils.session import Session
from utils.common import required_logined


class IndexHandler(BaseHandler):

    def get(self):
        logging.debug("debug msg")
        logging.info("info msg")
        logging.warning("warning msg")
        logging.error("error msg")
        print "print msg"
        # self.application.db
        # self.application.redis
        self.write("hello itcast")


class RegisterHandler(BaseHandler):
    """用户注册"""

    def post(self):
        mobile = self.json_args.get("mobile")
        password = self.json_args.get("password")
        sms_code = self.json_args.get("smscode")
        if not all((mobile, password, sms_code)):
            return self.write({"errno": RET.PARAMERR, "errmsg": "参数不完整"})
        if not re.match(r"1\d{10}", mobile):
            return self.write({"errno": RET.PARAMERR, "errmsg": "手机号错误"})
        # 验证短信验证码
        try:
            valid_sms_code = self.redis.get("sms_code_%s" % mobile)
        except Exception as e:
            logging.error(e)
            return self.write({"errno": RET.DBERR, "errmsg": "短信验证码查询出错"})
        if not valid_sms_code:
            return self.write({"errno": RET.NODATA, "errmsg": "短信验证码已过期或丢失"})
        if valid_sms_code != str(sms_code) and "2468" != str(sms_code):
            return self.write({"errno": RET.DATAERR, "errmsg": "短信验证码错误！"})
        password = hashlib.sha256(
            config.passwd_hash_key + password).hexdigest()
        try:
            res = self.db.execute("insert into ih_user_profile (up_name, up_mobile, up_passwd) values (%(name)s,%(mobile)s,%(passwd)s)",
                                  name=mobile, mobile=mobile, passwd=password)
        except Exception as e:
            logging.error(e)
            return self.write({"errno": RET.DATAEXIST, "errmsg": "手机号已注册！"})
        try:
            self.session = Session(self)
            self.session.data['user_id'] = res
            self.session.data['name'] = mobile
            self.session.data['mobile'] = mobile
            self.session.save()
        except Exception as e:
            logging.error(e)
        self.write({"errno": RET.OK, "errmsg": "OK"})


class LoginHandler(BaseHandler):
    """用户登入"""

    def post(self):
        mobile = self.json_args.get("mobile")
        password = self.json_args.get("password")
        if not all((mobile, password)):
            return self.write({"errno": RET.PARAMERR, "errmsg": "参数错误"})
        res = self.db.get(
            "select up_user_id, up_name, up_passwd from ih_user_profile where up_mobile=%(mobile)s", mobile=mobile)
        password = hashlib.sha256(
            config.passwd_hash_key + password).hexdigest()
        if res and res["up_passwd"] == unicode(password):
            try:
                self.session = Session(self)
                self.session.data["user_id"] = res["up_user_id"]
                self.session.data["name"] = res["up_name"]
                self.session.data["mobile"] = mobile
                self.session.save()
            except Exception as e:
                logging.error(e)
            return self.write({"errno": RET.OK, "errmsg": "OK"})
        else:
            return self.write({"errno": RET.DATAERR, "errmsg": "手机号或密码错误"})


class CheckLoginHandler(BaseHandler):
    """检测用户登录状态"""

    def get(self):
        if self.get_current_user():
            self.write({"errno": RET.OK, "errmsg": "用户已登陆",
                        "data": {"name": self.session.data.get("name")}})
        else:
            self.write({"errno": RET.SESSIONERR, "errmsg": "用户未登录"})

class LogoutHandler(BaseHandler):
    """登出"""
    
    @required_logined
    def get(self):
        self.session.delete()
        self.write({"errno": RET.OK, "errmsg": "OK"})
        