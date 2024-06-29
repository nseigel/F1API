import requests
import json
import codecs
import datetime
import zlib
import retrieve as r
import base64

# #testing requests
# URL = "https://livetiming.formula1.com/static/"
# response_2024 = requests.get("https://livetiming.formula1.com/static/2024/Index.json")
# response_Miami_2024 = requests.get("https://livetiming.formula1.com/static/2024/2024-05-05_Miami_Grand_Prix/2024-05-03_Practice_1/DriverList.jsonStream")
# #blah = json.loads(codecs.decode(response_Miami_2024.content, encoding='utf-8-sig'))
# blah = response_Miami_2024.text
# #print(blah)

# #testing timestamp processing
# date = '2024-03-02T14:20:35.019466Z'
# date_utc = date.replace('Z', '+00:00')
# date = datetime.datetime.fromisoformat(date_utc)
# print(date)

#testing different data streams
url = r.find_session("Race", "Hungaroring", 2018) + 'TeamRadio.jsonStream'
resp = requests.get(url)
print(resp.text)
print(url)


# print(r.decode64(resp, 1000))
# print(url)

# data = '7ed89990eb2a4d39870ff19793519937'
# decoded_data = zlib.decompress(base64.b64decode(data), -zlib.MAX_WBITS)

#row = resp.text.split('\r\n')[20]
#print(row)