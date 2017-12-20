import json
from bottle import run, request, post
from car.smartcar import SmartCar

# 读取配置文件
with open("config.json") as file:
    config = json.load(file)
car = SmartCar(config)

def control(action):
    control = {
        'car_forward': lambda: car.car_forward(),
        'car_backward': lambda: car.car_backward(),
        'car_front_turnleft': lambda: car.car_front_turnleft(),
        'car_front_turnright': lambda: car.car_front_turnright(),
        'car_back_turnleft': lambda: car.car_back_turnleft(),
        'car_back_turnright': lambda: car.car_back_turnright(),
        'car_stop': lambda: car.car_stop(),
        'servo_upward': lambda: car.servo_upward(),
        'servo_downward': lambda: car.servo_downward(),
        'servo_turnleft': lambda: car.servo_turnleft(),
        'servo_turnright': lambda: car.servo_turnright(),
        'servo_reset': lambda: car.servo_reset()
    }
    return control[action]()

@post('/carpi/control')
def car_control():
    request.POST.decode('utf-8')
    action = request.POST.get('action')
    control(action)
    return "action：%s success" % action


@post('/carpi/connect_test')
def connect_test():
    return "success"


run(host="0.0.0.0", port=5208, debug=False)
