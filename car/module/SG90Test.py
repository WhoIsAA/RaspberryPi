from car.module import SG90
import json

with open("config.json") as file:
    config = json.load(file)

sg90 = SG90(config["sg90"]["horizontal"])
sg90.move_to(120)