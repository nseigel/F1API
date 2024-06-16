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

for i in range(1000,1200):
      random_row = resp.text.split('\r\n')[i]
      timing, data, _ = random_row.split('"')
      decoded_data = zlib.decompress(base64.b64decode(data), -zlib.MAX_WBITS)
      decoded_data = json.loads(decoded_data)
      max_data = decoded_data["Position"][0]["Entries"]["1"]
      x_data.append(max_data['X'])
      y_data.append(max_data['Y'])

x_min = min(x_data)
x_max = max(x_data)
y_min = min(y_data)
y_max = max(y_data)

print(min(x_data))
print(max(x_data))
print(min(y_data))
print(max(y_data))

width = x_max - x_min
height = y_max - y_min

print(width)
print(height)

screen = Screen()

screen.screensize(width/50, height/50)

t = Turtle()
t.penup()
t.goto((x_data[0] - x_min)/50, (y_data[0] - y_min)/50)
t.pendown()

entries = len(x_data)

for i in range(entries):
      t.goto((x_data[i] - x_min)/50, (y_data[i] - y_min)/50)

screen.exitonclick()