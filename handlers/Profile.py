# coding=utf-8

from .BaseHandler import BaseHandler
from utils.common import required_logined
from utils.session import Session


class ProfileHandler(BaseHandler):
    """个人中心"""
    @required_logined
    def get(self):
        user_id = self.session.data["user_id"]
    # try:
    #     ret = self.db.get("select ")
