from RPi import GPIO
from time import sleep

class L298N:

    # 右轮
    # in1 = 31
    # in2 = 33
    # 左轮
    # in3 = 35
    # in4 = 37

    def __init__(self, config):
        self.pinlist = config["pin"]
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.pinlist, GPIO.OUT, initial=GPIO.LOW)


    def forward(self, sleep_time=0.1):
        GPIO.output(self.pinlist, (GPIO.LOW, GPIO.HIGH, GPIO.HIGH, GPIO.LOW))
        sleep(sleep_time)
        self.stop()


    def backward(self, sleep_time=0.1):
        GPIO.output(self.pinlist, (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.HIGH))
        sleep(sleep_time)
        self.stop()


    def car_front_turnleft(self, sleep_time=0.1):
        GPIO.output(self.pinlist, (GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.LOW))
        sleep(sleep_time)
        self.stop()


    def car_front_turnright(self, sleep_time=0.1):
        GPIO.output(self.pinlist, (GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.LOW))
        sleep(sleep_time)
        self.stop()


    def car_back_turnleft(self, sleep_time=0.1):
        GPIO.output(self.pinlist, (GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.LOW))
        sleep(sleep_time)
        self.stop()


    def car_back_turnright(self, sleep_time=0.1):
        GPIO.output(self.pinlist, (GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.HIGH))
        sleep(sleep_time)
        self.stop()


    def stop(self):
        GPIO.output(self.pinlist, GPIO.LOW)


if __name__ == "__main__":
    pass
