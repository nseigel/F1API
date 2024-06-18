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

random_row = resp.text.split('\r\n')[1000]
timing, data, _ = random_row.split('"')
decoded_data = zlib.decompress(base64.b64decode(data), -zlib.MAX_WBITS)
decoded_data = json.loads(decoded_data)

#print(decoded_data)