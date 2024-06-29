import base64
import zlib
import json
import datetime
import requests
import info as l
import codecs

def convert_time(timestamp):
    timestamp = timestamp[0:26]
    timestamp = timestamp.replace('Z', '0')
    while len(timestamp) < 26:
        timestamp = timestamp + '0'
    timestamp = timestamp + '+00:00'
    time = datetime.datetime.fromisoformat(timestamp)
    return time

def decode64(resp, index):
    row = resp.text.split('\r\n')[index]
    timing, data, _ = row.split('"')
    decoded_data = zlib.decompress(base64.b64decode(data), -zlib.MAX_WBITS)
    decoded_data = json.loads(decoded_data)
    return(timing, decoded_data)

def get_position_data(year, circuit, session, driver_number, start_index, end_index):
    url = find_session(session, circuit, year) + 'Position.z.jsonStream'
    resp = requests.get(url)
    x_data = []
    y_data = []
    timestamps = []
    for i in range(start_index,end_index):
        decoded_data = decode64(resp, i)[1]
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
            try:
                  if sess["Name"] == session:
                        path += sess["Path"]
            except KeyError:
                  print('KeyError')
      return path

def get_live_positions(session, circuit, year):
      url = find_session(session, circuit, year) + 'Position.z.jsonStream'
      resp = requests.get(url)
      rows = resp.text.split('\r\n')
      latest_position = decode64(resp, len(rows) - 2)[1]
      positions = latest_position['Position']
      index = len(positions) - 1
      data = {}
      for driver in l.drivers:
            x_data = positions[index]['Entries'][l.drivers[driver]]['X']
            y_data = positions[index]['Entries'][l.drivers[driver]]['Y']
            data[driver] = [x_data, y_data]
      return data