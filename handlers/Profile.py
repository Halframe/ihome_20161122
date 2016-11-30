# coding=utf-8

import re
import logging

from .BaseHandler import BaseHandler
from utils.common import required_logined
from utils.response_code import RET
from utils.image_storage import storage
from config import image_url_prefix


class ProfileHandler(BaseHandler):
    """个人中心"""
    
    @required_logined
    def get(self):
        user_id = self.session.data["user_id"]
        try:
            ret = self.db.get(
                "select up_name, up_mobile, up_avatar from ih_user_profile where up_user_id=%(user_id)s", user_id=user_id)
        except Exception as e:
            logging.error(e)
            return self.write({"errno": RET.DBERR, "errmsg": "数据库查询错误"})
        if not ret:
            return self.write({"errno": RET.NODATA, "errmsg": "无该用户信息"})
        if ret["up_avatar"]:
            img_url = image_url_prefix + ret["up_avatar"]
        else:
            img_url = None

        data = {
            "user_id": user_id,
            "name": ret["up_name"],
            "mobile": ret["up_mobile"],
            "avatar": img_url,
        }
        return self.write({"errno": RET.OK, "errmsg": "OK", "data": data})


class AvatarHandler(BaseHandler):
    """用户头像修改"""

    @required_logined
    def post(self):
        user_id = self.session.data["user_id"]
        try:
            avatar = self.request.files["avatar"][0]["body"]
        except Exception as e:
            logging.error(e)
            return self.write({"errno": RET.PARAMERR, "errmsg": "参数错误"})
        try:
            avatar_name = storage(avatar)
        except Exception as e:
            logging.error(e)
            avatar_name = None
            return self.write({"errno": RET.THIRDERR, "errmsg": "Qiniu Error"})
        try:
            ret = self.db.execute(
                "update ih_user_profile set up_avatar=%(avatar)s where up_user_id=%(user_id)s", avatar=avatar_name, user_id=user_id)
        except Exception as e:
            logging.error(e)
            return self.write({"errno": RET.DBERR, "errmsg": "数据库错误"})
        avatar_url = image_url_prefix + avatar_name
        self.write({"errno": RET.OK, "errmsg": "OK", "avatar": avatar_url})


class NameHandler(BaseHandler):
    """
    修改用户名
    @param: user_id, 从session获取用户id，要求用户登录
    @param: user_name, 用户提交的新用户名
    @return: errno，返回的消息代码；errmsg，返回结果的消息，以及返回其他数据
    """

    @required_logined
    def post(self):
        user_id = self.session.data["user_id"]
        user_name = self.json_args.get("user_name")
        if user_name in (None, ""):
            return self.write({"errno": RET.PARAMERR, "errmsg": "修改的用户名不能为空"})
        try:
            self.db.execute("update ih_user_profile set up_name=%(user_name)s where up_user_id=%(user_id)s", user_name=user_name, user_id=user_id)
        except Exception as e:
            logging.error(e)
            return self.write({"errno": RET.DBERR, "errmsg": "用户名已存在"})
        self.session.data["name"] = user_name
        self.session.save()
        return self.write({"errno": RET.OK, "errmsg": "OK", "new_username": user_name})


class AuthHandler(BaseHandler):
    """
    用户实名认证

    """

    @required_logined
    def get(self):
        user_id = self.session.data["user_id"]
        try:
            ret = self.db.get("select up_real_name, up_id_card from ih_user_profile where up_user_id=%(user_id)s", user_id=user_id)
        except Exception as e:
            logging.error(e)
            return self.write({"errno": RET.DBERR, "errmsg": "数据库查询错误"})
        if ret["up_id_card"] not in (None, ""):
            id_card = ret["up_id_card"]
            id_card = id_card[:4] + "*"*len(id_card[4:-4]) + id_card[-4:]
            return self.write({"errno": RET.OK, "errmsg": "OK", "real_name": ret["up_real_name"], "id_card": id_card})

    @required_logined
    def post(self):
        real_name = self.json_args.get("real_name")
        id_card = self.json_args.get("id_card")
        if not all((real_name, id_card)):
            return self.write({"errno": RET.PARAMERR, "errmsg": "参数不完整"})

        user_id = self.session.data["user_id"]
        try:
            self.db.execute("update ih_user_profile set up_real_name=%(real_name)s, up_id_card=%(id_card)s where up_user_id=%(user_id)s", real_name=real_name, id_card=id_card, user_id=user_id)
        except Exception as e:
            logging.error(e)
            return self.write({"errno": RET.DBERR, "errmsg": "数据库更新失败"})
        id_card = id_card[:4] + "*"*len(id_card[4:-4]) + id_card[-4:]
        return self.write({"errno":RET.OK, "errmsg":"OK", "real_name": real_name, "id_card": id_card})





