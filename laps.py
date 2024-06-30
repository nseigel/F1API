import json
import requests
import paths as p
import info

def split(data):
    length = len(data)
    timings = []
    rows = []
    for i in range(length):
        try:
            timing, datum = data[i].split('{', 1)
            timings.append(timing)
            rows.append(json.loads('{' + datum))
        except ValueError:
            print('value error; index: ' + str(i) + ' length: ' + str(length))
    return(timings, rows)


def get_lap_start(session, circuit, year, lap_number, driver):
    url = p.find_session(session, circuit, year) + 'LapSeries.jsonStream'
    resp = requests.get(url)
    rows = resp.text.split('\r\n')
    timing, data = split(rows)
    del data[0]
    del timing[0]
    length = len(data)
    start_time = ""
    for i in range(length):
        lap = ''
        try:
            for key in data[i][info.drivers[driver]]["LapPosition"]:
                lap = key
        except KeyError:
            pass
        if lap == str(lap_number):
            start_time = timing[i]
            break
    return(start_time)