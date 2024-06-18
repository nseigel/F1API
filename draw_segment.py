import base64
import zlib
import json
from turtle import *

import requests

url = 'http://livetiming.formula1.com/static/2024/' \
      '2024-06-09_Canadian_Grand_Prix/2024-06-09_Race/' \
      'Position.z.jsonStream'
resp = requests.get(url)

def min_max_value(x_data, y_data):
    mins = [min(x_data), min(y_data)]
    abs_min = min(mins)
    maxes = [max(x_data), max(y_data)]
    abs_max = max(maxes)
    return(abs_min, abs_max)

def normalize(data, abs_min, abs_max):
    data_length = len(data)
    negative_values = abs_min < 0
    data_range = abs_max - abs_min
    if negative_values:
        correction_factor = abs(abs_min)
        for i in range(data_length):
            data[i] = data[i] + correction_factor
    for i in range(data_length):
        if data_range == 0:
            data[i] = 0
        else:
            data[i] = data[i]/data_range
    return data

def scale(data, factor):
    for i in range(len(data)):
        data[i] = data[i] * factor
    return data

def get_driver_data(driver_number, start_index, end_index, factor):
    x_data = []
    y_data = []
    for i in range(start_index,end_index):
        random_row = resp.text.split('\r\n')[i]
        timing, data, _ = random_row.split('"')
        decoded_data = zlib.decompress(base64.b64decode(data), -zlib.MAX_WBITS)
        decoded_data = json.loads(decoded_data)
        max_data = decoded_data["Position"][0]["Entries"][str(driver_number)]
        x_data.append(max_data['X'])
        y_data.append(max_data['Y'])
    abs_min, abs_max = min_max_value(x_data, y_data)
    x_data_processed = scale(normalize(x_data, abs_min, abs_max), factor)
    y_data_processed = scale(normalize(y_data, abs_min, abs_max), factor)
    return(x_data_processed, y_data_processed)

def draw_segment(x_data, y_data, colour):
    t.color(colour)
    t.penup()
    t.goto(x_data[0], y_data[0])
    t.pendown()

    for i in range(len(x_data)):
        t.goto(x_data[i], y_data[i])
    t.penup()

carlos_x, carlos_y = get_driver_data(55, 5000, 5130, 300)
alex_x, alex_y = get_driver_data(23, 5000, 5130, 300)
#lando_x, lando_y = get_driver_data(4, 5000, 5130, 50)

screen = Screen()
screen.screensize(50, 50)
t = Turtle()

draw_segment(carlos_x, carlos_y, "red")
draw_segment(alex_x, alex_y, "blue")
#draw_segment(lando_x, lando_y, "orange")

t.goto(0,0)
t.color('black')
t.pendown()
for i in range(4):
    t.forward(300)
    t.left(90)


screen.exitonclick()