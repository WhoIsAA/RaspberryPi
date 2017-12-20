from RPi import GPIO
from time import sleep


class SG90:
    def __init__(self, config):
        GPIO.setup(config["pin"], GPIO.OUT, initial=GPIO.LOW)
        self.servo = GPIO.PWM(config["pin"], 50)
        self.servo.start(0)
        self.current_angle = config["angle"]
        self.init_angle = self.current_angle
        self.reset()

    def reset(self):
        self.move_to_new(self.init_angle)

    def get_current_angle(self):
        return self.current_angle

    def move_to(self, angle):
        duty_cycle = 2.5 + 10 * angle / 180
        if duty_cycle > 12.5 or duty_cycle < 2.5:
            return

        for i in range(0, 5, 1):
            self.servo.ChangeDutyCycle(duty_cycle)
            sleep(0.02)
            self.servo.ChangeDutyCycle(0)

        self.servo.ChangeDutyCycle(0)
        self.current_angle = angle

    def move_to_new(self, angle):
        if angle > 180 or angle < 0 or angle % 10 != 0:
            return

        if self.get_current_angle() > angle:
            step = -10
        else:
            step = 10

        for i in range(self.get_current_angle(), angle, step):
            self.servo.ChangeDutyCycle(2.5 + 10 * i / 180)
            sleep(0.02)
            self.servo.ChangeDutyCycle(0)
            sleep(0.1)
        self.current_angle = angle


if __name__ == '__main__':
    pass