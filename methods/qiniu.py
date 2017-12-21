#!/usr/bin/env python3
# coding=utf-8

import os
import requests
from qiniu import Auth, put_file, etag

qiniu_config = {
    "base_url": "",
    "access_key": "",
    "secret_key": "",
    "bucket_name": "",
}

def upload_file(path, filename):
    """
    将文件上传到七牛
    :param file_path: 文件绝对路径
    :return:
    """
    if not os.path.isfile(path + filename):
        return

    # 构建鉴权对象
    qn = Auth(qiniu_config["access_key"], qiniu_config["secret_key"])
    # 生成上传 Token，可以指定过期时间等
    token = qn.upload_token(qiniu_config["bucket_name"], filename)
    # 上传文件到七牛
    ret, info = put_file(token, filename, path + filename)
    print(info)
    # 等待上传成功
    assert ret["key"] == filename
    assert ret["hash"] == etag(path + filename)
    return filename


def download_file(filename, localpath):
    """
    下载文件
    :param filename:
    :param localpath:
    :return:
    """
    if not filename or not localpath:
        return

    if not os.path.isdir(localpath):
        os.mkdir(localpath)

    # 构建鉴权对象
    qn = Auth(qiniu_config["access_key"], qiniu_config["secret_key"])
    downloadUrl = qn.private_download_url(qiniu_config["base_url"] + filename)
    print("正在下载：", downloadUrl)
    # 下载文件
    resp = requests.get(downloadUrl)
    filepath = localpath + filename
    with open(filepath, 'wb+') as f:
        f.write(resp.content)
    print("下载完成")
