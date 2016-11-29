# -*- coding: utf-8 -*-
# flake8: noqa

import logging

from qiniu import Auth, put_file, etag, urlsafe_base64_encode
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
access_key = 'iD5yHFaRnVIJ3p6_ptXpWOQ9YXQ4t3m4MZT7dR9l'
secret_key = 'DkkSDGf36IHwvcQiaOgYJcYDhXPfkBne9u2HUBn2'


def storage(data):
    if not data:
        return None

    try:

        # 构建鉴权对象
        q = Auth(access_key, secret_key)

        # 要上传的空间
        bucket_name = 'ihome'

        # 上传到七牛后保存的文件名
        # key = 'my-python-logo.png';

        # 生成上传 Token，可以指定过期时间等
        token = q.upload_token(bucket_name)

        # 要上传文件的本地路径
        # localfile = './sync/bbb.jpg'

        ret, info = put_file(token, None, data)
        # print(info)
        # assert ret['key'] == key
        # assert ret['hash'] == etag(localfile)

    except Exception as e:
        logging.error(e)
        raise Exception("上传文件到七牛发生错误")

    if info and info.status_code != 200:
        raise Exception("上传文件到七牛发生错误")

    return ret["key"]


if __name__ == '__main__':
    file_name = raw_input("输入上传的文件")
    file = open(file_name, 'rb')
    data = file.read()
    key = storage(data)
    print key
    file.close()
