# coding=utf-8

import logging

from .BaseHandler import BaseHandler
from utils.common import required_logined
from utils.response_code import RET
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
        self.write({"errno": RET.OK, "errmsg": "OK", "url": avatar_url})


class NameHandler(BaseHandler):
    """修改用户名"""

    def post(self):
        pass