import base64
import zlib
import json
from turtle import *
import datetime
import time

import requests

url = 'http://livetiming.formula1.com/static/2023/' \
      '2023-07-30_Belgian_Grand_Prix/2023-07-30_Race/' \
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

def convert_time(timestamp):
    timestamp = timestamp[0:26]
    timestamp = timestamp.replace('Z', '0')
    while len(timestamp) < 26:
        timestamp = timestamp + '0'
    timestamp = timestamp + '+00:00'
    time = datetime.datetime.fromisoformat(timestamp)
    return time

def get_driver_data(driver_number, start_index, end_index, factor):
    x_data = []
    y_data = []
    timestamps = []
    for i in range(start_index,end_index):
        row = resp.text.split('\r\n')[i]
        timing, data, _ = row.split('"')
        decoded_data = zlib.decompress(base64.b64decode(data), -zlib.MAX_WBITS)
        decoded_data = json.loads(decoded_data)
        for x in range(len(decoded_data["Position"])):
            timestamp = convert_time(decoded_data["Position"][x]["Timestamp"])
            timestamps.append(timestamp)
            driver_data = decoded_data["Position"][x]["Entries"][str(driver_number)]
            x_data.append(driver_data['X'])
            y_data.append(driver_data['Y'])
    abs_min, abs_max = min_max_value(x_data, y_data)
    x_data_processed = scale(normalize(x_data, abs_min, abs_max), factor)
    y_data_processed = scale(normalize(y_data, abs_min, abs_max), factor)
    return(x_data_processed, y_data_processed, timestamps)

def draw_segment(start_time, end_time, driver_number, scale, colour, visualize):
    driver_x, driver_y, timestamps = get_driver_data(driver_number, start_time, end_time, scale)
    t.color(colour)
    t.penup()
    t.goto(driver_x[0], driver_y[0])
    t.pendown()
    for i in range(len(driver_x)):
        t.goto(driver_x[i], driver_y[i])

    t.penup()
    if visualize:
        t.goto(driver_x[0], driver_y[0])
        #t.shape('circle')
        prev_timestamp = 0
        for i in range(len(driver_x)):
            timestamp = timestamps[i]
            if i != 0:
                time_delta = timestamp - prev_timestamp
                total_delta = time_delta.microseconds + time_delta.seconds * 1000000
                time.sleep(total_delta/1000000)
            t.goto(driver_x[i], driver_y[i])
            prev_timestamp = timestamp

screen = Screen()
screen.screensize(50, 50)
t = Turtle()

#draw_segment(5000, 5130, 55, 300, "red", False)
draw_segment(5000, 5130, 44, 300, "red", True)

screen.exitonclick()