import base64
import zlib
import json
from turtle import *

import requests

url = 'http://livetiming.formula1.com/static/2024/' \
      '2024-03-02_Bahrain_Grand_Prix/2024-03-02_Race/' \
      'Position.z.jsonStream'
resp = requests.get(url)
x_data = []
y_data = []

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
        data[i] = data[i]/data_range
    return data

def scale(data, factor):
    for i in range(len(data)):
        data[i] = data[i] * factor
    return data


for i in range(1000,1200):
      random_row = resp.text.split('\r\n')[i]
      timing, data, _ = random_row.split('"')
      decoded_data = zlib.decompress(base64.b64decode(data), -zlib.MAX_WBITS)
      decoded_data = json.loads(decoded_data)
      max_data = decoded_data["Position"][0]["Entries"]["1"]
      x_data.append(max_data['X'])
      y_data.append(max_data['Y'])

#print(x_data)
x_data_processed = scale(normalize(x_data), 200)
y_data_processed = scale(normalize(y_data), 200)
#print(x_data_normalized)

screen = Screen()

screen.screensize(50, 50)

t = Turtle()
t.penup()
t.goto(x_data_processed[0], y_data_processed[0])
t.pendown()

for i in range(len(x_data_processed)):
    t.goto(x_data_processed[i], y_data_processed[i])

screen.exitonclick()