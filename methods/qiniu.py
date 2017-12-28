#!/usr/bin/env python3
# coding=utf-8

import hashlib
import json
import os
import requests
import MySQLdb
from qiniu import Auth, put_file, etag, BucketManager

class Qiniu:

    def __init__(self):
        self._bucket_url = ""
        self._access_key = ""
        self._secret_key = ""
        self._bucket_name = ""
        self._default_local_path = os.getcwd()
        self._auth = Auth(self._access_key, self._secret_key)
        self.db = None
        self.cursor = None
        self.init_db()

    def __del__(self):
        """
        在程序退出时，关闭数据库操作流
        :return:
        """
        if self.db:
            self.db.close()
        if self.cursor:
            self.cursor.close()

    def init_db(self):
        """
        初始化本地数据库
        :return:
        """
        try:
            self.db = MySQLdb.connect(host="localhost", user="root", passwd="toor", db="rspi", port=3306, charset="utf8")
            self.cursor = self.db.cursor(cursorclass=MySQLdb.cursors.DictCursor)
            self.cursor.execute("CREATE TABLE IF NOT EXISTS qiniu("
                                "id INT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,"
                                "filename TEXT NOT NULL,"
                                "hash TEXT NOT NULL,"
                                "fkey TEXT NOT NULL,"
                                "url TEXT NOT NULL,"
                                "mimeType TEXT NOT NULL,"
                                "type INT UNSIGNED,"
                                "thumbnail TEXT,"
                                "duration INT UNSIGNED,"
                                "fsize INT UNSIGNED,"
                                "putTime TEXT NOT NULL);")
        except Exception as e:
            print("!!! init_db = ", e)

    def add_local_data(self, key, info):
        """
        将上传成功的返回值写入本地数据库
        :param key:
        :param info:
        :return:
        """
        filename = key.split('/')[-1]
        url = self.get_url(key)
        type = 1
        thumbnail = ""
        duration = 0
        if info['mimeType'].startswith('video'):
            type = 2
            thumbnail = self.get_video_thumbnail(key)
            duration = self.get_video_duration(key)
        try:
            sql = "INSERT INTO qiniu(filename, hash, fkey, url, mimeType, type, thumbnail, duration, fsize, putTime) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(filename, info['hash'], key, url, info['mimeType'], type, thumbnail, duration, info['fsize'], info['putTime'])
            self.cursor.execute(sql)
            self.db.commit()
            print("* 写入数据库成功：", key)
        except Exception as e:
            self.db.rollback()
            print("!!! add_local_data = ", e)

    def get_data_by_key(self, key):
        """
        根据key查询本地数据库
        :param key:
        :return:
        """
        if key:
            try:
                sql = "SELECT * FROM qiniu where fkey='{}'".format(key)
                self.cursor.execute(sql)
                rows = self.cursor.fetchall()
                if len(rows) > 0:return json.dumps(rows)
            except Exception as e:
                print("!!! get_data_by_key = ", e)

    def get_data_by_type(self, type):
        """
        根据type查询本地数据库
        :param key:
        :return:
        """
        if type:
            try:
                sql = "SELECT * FROM qiniu where type='{}'".format(int(type))
                self.cursor.execute(sql)
                rows = self.cursor.fetchall()
                if len(rows) > 0: return json.dumps(rows)
            except Exception as e:
                print("!!! get_data_by_type = ", e)

    def _get_file_key(self, prefix, filename):
        """
        拼接文件key
        :param prefix:
        :param filename:
        :return:
        """
        if prefix:return prefix + "/" + filename
        else:return filename

    def upload_file(self, path, filename, prefix=None):
        """
        上传文件到七牛云存储
        :param path: 文件所在目录
        :param filename: 文件名
        :param prefix: 前缀
        :return:
        """
        if os.path.isfile(path + filename):
            key = self._get_file_key(prefix, filename)
            # 生成上传 Token，可以指定过期时间等
            token = self._auth.upload_token(self._bucket_name, key)
            # 上传文件到七牛
            ret, info = put_file(token, key, path + filename)
            if ret and ret['key'] == key and ret['hash'] == etag(path + filename):
                stat = self.get_filestat(ret['key'])
                print("* 上传成功：", stat)
                self.add_local_data(ret['key'], stat)
                return self._bucket_url + key
        print("!!! 上传失败")
        return None

    def download_file(self, download_url, localpath=None):
        """
        下载文件
        :param filename: 文件名
        :param prefix: 前缀
        :param localpath: 文件下载目录
        :return:
        """
        if not download_url:
            return

        if not localpath:
            localpath = self._default_local_path

        filename = str(download_url).split("/")[-1]
        if filename:
            # 下载文件
            resp = requests.get(download_url)
            filepath = localpath + "/" + filename
            with open(filepath, 'wb+') as f:
                f.write(resp.content)
            print("* 下载完成：", filepath)
        print("!!! 下载失败")

    def list(self, prefix=None, limit=20, delimiter=None, marker=None):
        """
        获取指定前缀文件列表
        :param prefix:前缀
        :param limit:列举条目
        :param delimiter:列举出除'/'的所有文件以及以'/'为分隔的所有前缀
        :param marker:标记
        :return:
        """
        bucket = BucketManager(self._auth)
        ret, eof, info = bucket.list(self._bucket_name, prefix, marker, limit, delimiter)
        if ret and ret.get('items'):
            return ret
        return None

    def get_filestat(self, key):
        """
        获得文件状态信息
        :param key:
        :return:
        """
        bucket = BucketManager(self._auth)
        ret, info = bucket.stat(self._bucket_name, key)
        if ret and 'hash' in ret:
            return ret
        return None

    def get_video_thumbnail(self, key):
        """
        获得视频缩略图
        :param key:
        :return:
        """
        return self.get_url(key) + "?vframe/jpg/offset/1/w/480/h/360"

    def get_video_duration(self, key):
        """
        获得视频时长
        :param key:
        :return:
        """
        ret = 0
        url = self.get_url(key) + "?avinfo"
        resp = requests.get(url)
        if str(resp.status_code) == '200':
            duration = resp.json()['format']['duration']
            ret = int(float(duration))
        return ret

    def get_md5(self, filepath):
        """
        计算本地文件 md5
        :param filepath: str => path to file
        :return: str => md5
        """
        if os.path.exists(filepath):
            hash_md5 = hashlib.md5()
            with open(filepath, 'rb') as handle:
                for chuck in iter(lambda: handle.read(4096), b""):
                    hash_md5.update(chuck)
            return hash_md5.hexdigest()
        else:
            return None

    def get_url(self, key):
        """
        获得资源外链
        :param key:文件名
        :return:
        """
        return self._bucket_url + key
