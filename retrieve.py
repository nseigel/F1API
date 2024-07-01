import base64
import zlib
import json
import datetime
import requests
import info as l
import codecs
import laps
import paths as p

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
    url = p.find_session(session, circuit, year) + 'Position.z.jsonStream'
    resp = requests.get(url)
    x_data = []
    y_data = []
    utctimestamps = []
    centraltimestamps = []
    for i in range(start_index,end_index):
        central_timestamp, decoded_data = decode64(resp, i)
        centraltimestamps.append(central_timestamp)
        for x in range(len(decoded_data["Position"])):
            timestamp = convert_time(decoded_data["Position"][x]["Timestamp"])
            utctimestamps.append(timestamp)
            driver_data = decoded_data["Position"][x]["Entries"][str(driver_number)]
            x_data.append(driver_data['X'])
            y_data.append(driver_data['Y'])
    return(x_data, y_data, utctimestamps, centraltimestamps)

def find_time(times, target):
    target = target[:8]
    index = 0
    for i in range(len(times)):
        time = times[i][:8]
        if time == target:
            index = i
            break
    return index


def get_lap_positions(year, circuit, session, driver, lap):
    url = p.find_session(session, circuit, year) + 'Position.z.jsonStream'
    resp = requests.get(url)
    rows = resp.text.split('\r\n')
    times, positions = [], []
    for i in range(len(rows)):
        try:
            time, position, _ = rows[i].split('"')
            decoded_position = zlib.decompress(base64.b64decode(position), -zlib.MAX_WBITS)
            decoded_position = json.loads(decoded_position)
            times.append(time)
            positions.append(decoded_position)
        except ValueError:
            print('value error; index: ' + str(i) + ' length: ' + str(len(rows)))
    start_index = find_time(times, laps.get_lap_start(session, circuit, year, lap, driver))
    end_index = find_time(times, laps.get_lap_start(session, circuit, year, lap + 1, driver))
    driver_x = []
    driver_y = []
    utctimestamps = []
    for i in range(start_index, end_index + 1):
        for h in range(len(positions[i]["Position"])):
            x = positions[i]["Position"][h]['Entries'][l.drivers[driver]]['X']
            y = positions[i]["Position"][h]['Entries'][l.drivers[driver]]['Y']
            utctimestamp = positions[i]["Position"][h]["Timestamp"]
            utctimestamp = convert_time(utctimestamp)
            utctimestamps.append(utctimestamp)
            driver_x.append(x)
            driver_y.append(y)
    return(driver_x, driver_y, utctimestamps)