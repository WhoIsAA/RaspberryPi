#!/usr/bin/env python3
# coding=utf-8

import os
from time import sleep, time
from picamera import PiCamera

class Camera:

    def __init__(self):
        self.qiniu_config = {
            "base_url":"",
            "access_key":"",
            "secret_key":"",
            "bucket_name":"",
        }
        self.camera_path = "/home/pi/rspi_images/"
        self.camera_resolution = (1280, 720)
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
            camera.start_preview()
            #捕获图片前，至少要给传感器两秒钟时间感光
            sleep(2)
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
            camera.start_preview()
            # 捕获图片前，至少要给传感器两秒钟时间感光
            sleep(2)
            for i, filename in enumerate(camera.capture_continuous('img_{timestamp:%Y-%m-%d-%H-%M-%S}.jpg')):
                print(filename)
                img_list.append(filename)
                sleep(delay)
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
