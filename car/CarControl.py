import curses
import json
import atexit
from RPi import GPIO
from car.smartcar import SmartCar

# 初始化GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
atexit.register(GPIO.cleanup)

red_left = 13
red_right = 12
GPIO.setup((red_left, red_right), GPIO.IN)

# 读取配置文件
with open("config.json") as file:
    config = json.load(file)

car = SmartCar(config)

# 初始化curses
stdscr = curses.initscr()
# 开启键盘模式
stdscr.keypad(1)
# 清除屏幕
stdscr.clear()
stdscr.addstr(0, 0, 'w:小车前进\ts:小车后退\na:小车左转\td:小车右转\n* 上下左右控制舵机方向\n* q:退出\n', curses.A_NORMAL)

while True:
    if GPIO.input(red_left) == GPIO.LOW and GPIO.input(red_right) == GPIO.LOW:
        # print("左右都有障碍物")
        car.car_backward()
    elif GPIO.input(red_left) == GPIO.LOW:
        # print("左边有障碍物")
        car.car_turnright()
    elif GPIO.input(red_right) == GPIO.LOW:
        # print("右边有障碍物")
        car.car_turnleft()
    else:
        # print("没有障碍物")
        car.car_forward()

    key = stdscr.getkey()
    # 退出
    if key == 'q': break
    # 小车前进
    if key == 'w': car.car_forward()
    # 小车后退
    if key == 's': car.car_backward()
    # 小车左转
    if key == 'a': car.car_turnleft()
    # 小车右转
    if key == 'd': car.car_turnright()
    # 小车停止
    if key == 'e': car.car_stop()
    # 舵机向上
    if key == 'i': car.servo_upward()
    # 舵机向下
    if key == 'k': car.servo_downward()
    # 舵机左转
    if key == 'j': car.servo_turnleft()
    # 舵机右转
    if key == 'l': car.servo_turnright()
    # 舵机角度重置
    if key == 'o': car.servo_reset()
