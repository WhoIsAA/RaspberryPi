#!/usr/bin/env python3
# coding=utf-8

import os
import requests
import time
from picamera import PiCamera
from qiniu import Auth, put_file, etag


class Camera:

    def __init__(self):
        self.camera_path = "/home/pi/rspi_images/"
        self.camera_resolution = (1280, 720)
        self.camera_rotation = 180
        if not os.path.exists(self.camera_path):
            os.mkdir(self.camera_path)

    def _get_image_filename(self):
        """
        获得拍照文件名
        :return:
        """
        timeArray = time.localtime(time.time())
        timestr = time.strftime("%Y-%m-%d-%H-%M-%S", timeArray)
        return "img_%s.jpg" % timestr

    def _get_video_filename(self):
        """
        获得录像文件名
        :return:
        """
        timeArray = time.localtime(time.time())
        timestr = time.strftime("%Y-%m-%d-%H-%M-%S", timeArray)
        return "video_%s.h264" % timestr

    def take_picture(self):
        """
        拍一张图片
        :return:
        """
        with PiCamera() as camera:
            camera.resolution = self.camera_resolution
            camera.rotation = self.camera_rotation
            camera.start_preview()
            #捕获图片前，至少要给传感器两秒钟时间感光
            time.sleep(2)
            filename = self._get_image_filename()
            camera.capture("%s%s" % (self.camera_path, filename))
            print(filename)
        return filename

    def continuous_photo(self, count, delay):
        """
        连续拍多张图片
        :param count: 要拍多少张
        :param delay: 拍照间隔时间
        :return:
        """
        if count < 2 or delay < 2:
            return

        img_list = []
        with PiCamera() as camera:
            camera.resolution = self.camera_resolution
            camera.rotation = self.camera_rotation
            camera.start_preview()
            # 捕获图片前，至少要给传感器两秒钟时间感光
            time.sleep(2)
            for i, filename in enumerate(camera.capture_continuous('img_{timestamp:%Y-%m-%d-%H-%M-%S}.jpg')):
                print(filename)
                img_list.append(filename)
                time.sleep(delay)
                if i == count:
                    break;
        return img_list

    def record_video(self, seconds):
        """
        录制一段视频
        :param seconds: 录制时长
        :return:
        """
        if seconds < 10:
            return

        with PiCamera() as camera:
            filename = self._get_video_filename()
            camera.resolution = self.camera_resolution
            camera.start_recording(filename)
            camera.wait_recording(seconds)
            camera.stop_recording()
        return filename

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
    print("上传完成")
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


if __name__ == '__main__':
    camera = Camera()
    pic = camera.take_picture()
    upload_file(camera.camera_path, pic)
    download_file(pic, "/home/pi/Desktop/")