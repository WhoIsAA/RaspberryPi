from threading import Thread
from RPi import GPIO

class Infrared(Thread):

    #左：13
    #右：12

    def __init__(self, config):
        super().__init__()
        self.left_pin = config["left"]
        self.right_pin = config["right"]
        GPIO.setup([self.left_pin, self.right_pin], GPIO.IN)
        self.status = self.check_obstacle()
        self.running = True

    def run(self):
        while self.running:
            self.status = self.check_obstacle()

    def stop(self):
        self.running = False

    def get_infrared_status(self):
        return self.status

    def left(self):
        return GPIO.input(self.left_pin) == GPIO.LOW

    def right(self):
        return GPIO.input(self.right_pin) == GPIO.LOW

    def check_obstacle(self):
        if self.left() and self.right():
            # 左右都有障碍物
            return "all"
        elif self.left():
            # 左边有障碍物
            return "left"
        elif self.right():
            # 右边有障碍物
            return "right"
        else:
            # 没有障碍物
            return "none"