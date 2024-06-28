import base64
import zlib
import json
import datetime
import requests
import locationid as l
import codecs

def convert_time(timestamp):
    timestamp = timestamp[0:26]
    timestamp = timestamp.replace('Z', '0')
    while len(timestamp) < 26:
        timestamp = timestamp + '0'
    timestamp = timestamp + '+00:00'
    time = datetime.datetime.fromisoformat(timestamp)
    return time

def get_position_data(year, circuit, session, driver_number, start_index, end_index):
    url = find_session(session, circuit, year) + 'Position.z.jsonStream'
    resp = requests.get(url)
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
    return(x_data, y_data, timestamps)

def find_meeting(circuit, year):
      url = 'http://livetiming.formula1.com/static/' + str(year) + '/Index.json'
      resp = requests.get(url)
      resp = json.loads(codecs.decode(resp.content, encoding='utf-8-sig'))
      key = l.circuits[circuit]
      meeting = {}
      for meet in resp['Meetings']:
            if meet["Code"] == key:
                  meeting = meet
      return meeting

def find_session(session, circuit, year):
      meeting = find_meeting(circuit, year)
      path = 'https://livetiming.formula1.com/static/'
      for sess in meeting["Sessions"]:
            if sess["Name"] == session:
                  path += sess["Path"]
      return path