import base64
import zlib
import json
from turtle import *

import requests

url = 'http://livetiming.formula1.com/static/2023/' \
      '2023-05-28_Monaco_Grand_Prix/2023-05-28_Race/' \
      'Position.z.jsonStream'
resp = requests.get(url)

def normalize(data):
    data_length = len(data)
    min_value = min(data)
    max_value = max(data)
    negative_values = min_value < 0
    data_range = max_value - min_value
    if negative_values:
        correction_factor = abs(min_value)
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
    x_data_processed = scale(normalize(x_data), factor)
    y_data_processed = scale(normalize(y_data), factor)
    return(x_data_processed, y_data_processed)

def draw_segment(x_data, y_data, colour):
    t.color(colour)
    t.penup()
    t.goto(x_data[0], y_data[0])
    t.pendown()

    for i in range(len(x_data)):
        t.goto(x_data[i], y_data[i])
    t.penup()

lewis_x, lewis_y = get_driver_data(44, 5000, 5130, 300)
bottas_x, bottas_y = get_driver_data(77, 5000, 5130, 300)
lando_x, lando_y = get_driver_data(4, 5000, 5130, 300)

screen = Screen()
screen.screensize(50, 50)
t = Turtle()

draw_segment(lewis_x, lewis_y, "blue")
draw_segment(bottas_x, bottas_y, "black")
draw_segment(lando_x, lando_y, "orange")

screen.exitonclick()