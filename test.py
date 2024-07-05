import requests
import json
import codecs
import datetime
import zlib
import retrieve as r
import base64
import speech_recognition as sr
import paths as p

# #testing requests
# URL = "https://livetiming.formula1.com/static/"
# response_2024 = requests.get("https://livetiming.formula1.com/static/2024/Index.json")
# response_Miami_2024 = requests.get("https://livetiming.formula1.com/static/2024/2024-05-05_Miami_Grand_Prix/2024-05-03_Practice_1/DriverList.jsonStream")
# #blah = json.loads(codecs.decode(response_Miami_2024.content, encoding='utf-8-sig'))
# blah = response_Miami_2024.text
# #print(blah)

#testing timestamp processing
date = '2024-03-02T14:20:35.019466Z'
date_utc = date.replace('Z', '+00:00')
# print(date_utc)
date = datetime.datetime.fromisoformat(date_utc)
# print(date)
# print(date.time())
# correcttiming = date.time()
timing = '2024-03-02T02:20:56.665000+00:00'
#         2024-03-02T14:20:35.019466+00:00
timing = datetime.datetime.fromisoformat(timing)
print(timing)
time_delta = date - timing
timing = timing + time_delta
print(timing)

#testing different data streams
# url = p.find_session("Race", "Spielberg", 2024) + 'LapCount.jsonStream'
# resp = requests.get(url)
# print(resp.text)

# print(resp.text)
# print(url)


# print(r.decode64(resp, 5000))
# print(url)

# data = '7ed89990eb2a4d39870ff19793519937'
# decoded_data = zlib.decompress(base64.b64decode(data), -zlib.MAX_WBITS)

#row = resp.text.split('\r\n')[20]
#print(row)

#testing audio transcription
# url = 'https://livetiming.formula1.com/static/2018/2018-07-29_Hungarian_Grand_Prix/2018-07-29_Race/TeamRadio/KIMRAI01_7_20180729_152713.mp3'
# file = requests.get(url)
# rec = sr.Recognizer()
# audio_file = sr.AudioFile('radio.wav')
# with audio_file as source:
#     audio = rec.record(source)
#     text = rec.recognize_google(audio)
#     print(text)