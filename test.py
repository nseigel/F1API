import requests
import json
import codecs

URL = "https://livetiming.formula1.com/static/"

response_2024 = requests.get("https://livetiming.formula1.com/static/2024/Index.json")
response_Miami_2024 = requests.get("https://livetiming.formula1.com/static/2024/2024-05-05_Miami_Grand_Prix/2024-05-03_Practice_1/DriverList.jsonStream")
#blah = json.loads(codecs.decode(response_Miami_2024.content, encoding='utf-8-sig'))
blah = response_Miami_2024.text
print(blah)