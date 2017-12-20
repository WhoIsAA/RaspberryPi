import atexit
from RPi import GPIO
from car.module import SG90, Infrared, L298N


class SmartCar(object):

    def __init__(self, config):
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        atexit.register(GPIO.cleanup)

        self.init_l298n(config["l298n"])
        self.init_sg90(config["sg90"])
        self.init_infrared(config["infrared_obstacle"])

    def init_l298n(self, config):
        self.l298n = L298N.L298N(config)
        self.running = False

    def init_sg90(self, config):
        self.sg90_vt = SG90.SG90(config["vertical"])
        self.sg90_hr = SG90.SG90(config["horizontal"])

    def init_infrared(self, config):
        self.infrared = Infrared.Infrared(config)
        self.infrared.start()

    def car_forward(self):
        #左右没有障碍物
        if self.infrared.get_infrared_status() != "all":
            self.l298n.forward()

    def car_backward(self):
        self.l298n.backward()

    def car_front_turnleft(self):
        #左边没有障碍物
        if self.infrared.get_infrared_status() != "left":
            self.l298n.car_front_turnleft()


    def car_front_turnright(self):
        #右边没有障碍物
        if self.infrared.get_infrared_status() != "right":
            self.l298n.car_front_turnright()


    def car_back_turnleft(self):
        self.l298n.car_back_turnleft()


    def car_back_turnright(self):
        self.l298n.car_back_turnright()

    def car_stop(self):
        self.l298n.stop()

    def servo_upward(self):
        angle = self.sg90_vt.get_current_angle() - 10
        self.sg90_vt.move_to(angle)

    def servo_downward(self):
        angle = self.sg90_vt.get_current_angle() + 10
        self.sg90_vt.move_to(angle)

    def servo_turnleft(self):
        angle = self.sg90_hr.get_current_angle() + 10
        self.sg90_hr.move_to(angle)

    def servo_turnright(self):
        angle = self.sg90_hr.get_current_angle() - 10
        self.sg90_hr.move_to(angle)

    def servo_reset(self):
        self.sg90_hr.reset()
        self.sg90_vt.reset()