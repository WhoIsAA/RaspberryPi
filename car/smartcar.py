import atexit
from RPi import GPIO
from car.module import SG90, Infrared, L298N, Camera


class SmartCar(object):

    def __init__(self, config):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        atexit.register(GPIO.cleanup)

        self.init_l298n(config["l298n"])
        self.init_sg90(config["sg90"])
        self.init_infrared(config["infrared_obstacle"])
        self.init_camera()

    def init_l298n(self, config):
        self._l298n = L298N.L298N(config)

    def init_sg90(self, config):
        self._sg90_vt = SG90.SG90(config["vertical"])
        self._sg90_hr = SG90.SG90(config["horizontal"])

    def init_infrared(self, config):
        self._infrared = Infrared.Infrared(config)
        self._infrared.start()

    def init_camera(self):
        self._camera = Camera.Camera()

    def get_servo_angle_hr(self):
        #获得水平舵机当前角度
        return self._sg90_hr.get_current_angle()

    def get_servo_angle_vt(self):
        #获得垂直舵机当前角度
        return self._sg90_vt.get_current_angle()

    def car_forward(self):
        #左右没有障碍物
        if self._infrared.get_infrared_status() != "all":
            self._l298n.forward()

    def car_backward(self):
        self._l298n.backward()

    def car_front_turnleft(self):
        #左边没有障碍物
        if self._infrared.get_infrared_status() != "left":
            self._l298n.car_front_turnleft()

    def car_front_turnright(self):
        #右边没有障碍物
        if self._infrared.get_infrared_status() != "right":
            self._l298n.car_front_turnright()


    def car_back_turnleft(self):
        self._l298n.car_back_turnleft()

    def car_back_turnright(self):
        self._l298n.car_back_turnright()

    def car_stop(self):
        self._l298n.stop()

    def servo_hr_move_to(self, angle):
        self._sg90_hr.move_to_new(angle)

    def servo_vt_move_to(self, angle):
        self._sg90_vt.move_to_new(angle)

    def servo_upward(self):
        angle = self._sg90_vt.get_current_angle() - 10
        self._sg90_vt.move_to(angle)

    def servo_downward(self):
        angle = self._sg90_vt.get_current_angle() + 10
        self._sg90_vt.move_to(angle)

    def servo_turnleft(self):
        angle = self._sg90_hr.get_current_angle() + 10
        self._sg90_hr.move_to(angle)

    def servo_turnright(self):
        angle = self._sg90_hr.get_current_angle() - 10
        self._sg90_hr.move_to(angle)

    def servo_reset(self):
        self._sg90_hr.reset()
        self._sg90_vt.reset()

    def take_picture(self):
        return self._camera.take_picture()

    def continuous_photo(self, count, delay):
        return self._camera.continuous_photo(count, delay)

    def record_video(self, seconds):
        return self._camera.record_video(seconds)

    def preview(self, type):
        return self._camera.preview(type)

