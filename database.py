import sqlite3
import paths as p
import requests
import json
import codecs

def manageKey(dict, keys):
    data = []
    for key in keys:
        try:
            value = dict[key]
        except KeyError:
            value = None
        data.append(value)
    return data

def splitTiming(rows):
    data = []
    timings = []
    for row in rows:
        split = row.split('{', 1)
        timing = split[0]
        value = json.loads('{' + split[1])
        data.append(value)
        timings.append(timing)
    return timings, data

def createCursor(path):
    url = path + "SessionInfo.jsonStream"
    resp = requests.get(url)
    timing, data = resp.text.split('{', 1)
    data = json.loads("{" + data)
    session = data['Name']
    db_name = session + '_' + path.split('/')[5]

    con = sqlite3.connect('db/' + db_name)
    cur = con.cursor()
    return cur, con


def saveSessionInfo(path):
    url = path + "SessionInfo.json"
    resp = requests.get(url)
    data = json.loads(codecs.decode(resp.content, encoding='utf-8-sig'))

    cur, con = createCursor(path)

    cur.execute('CREATE TABLE SessionInfo(Name, OfficialName, Location, Country, Circuit, SessionName, StartDate, EndDate, Path)')
    to_enter = [
        (data['Meeting']['Name'], data['Meeting']['OfficialName'], data['Meeting']['Location'], data['Meeting']['Country']["Name"], data['Meeting']['Circuit']['ShortName'], data['Name'], data['StartDate'], data['EndDate'], data['Path'])
    ]

    cur.executemany('INSERT INTO SessionInfo VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', to_enter)
    con.commit()
    return cur, con

def saveArchiveStatus(path):
    url = path + 'ArchiveStatus.json'
    resp = requests.get(url)
    data = json.loads(codecs.decode(resp.content, encoding='utf-8-sig'))
    cur, con = createCursor(path)

    cur.execute('CREATE TABLE ArchiveStatus(Status)')
    to_enter = [
        (data["Status"],)
    ]

    cur.executemany('INSERT INTO ArchiveStatus VALUES(?)', to_enter)
    con.commit()
    return cur, con

def saveContentStreams(path):
    url = path + 'ContentStreams.json'
    resp = requests.get(url)
    data = json.loads(codecs.decode(resp.content, encoding='utf-8-sig'))
    
    cur, con = createCursor(path)

    streams = data['Streams']
    rows = []
    for stream in streams:
        type_, name, language, uri, path, utc = manageKey(stream, ["Type", "Name", "Language", "Uri", "Path", "Utc"])
        row = (type_, name, language, uri, path, utc)
        rows.append(row)

    cur.execute('CREATE TABLE ContentStreams(Type, Name, Language, Uri, Path, Utc)')
    cur.executemany('INSERT INTO ContentStreams VALUES(?, ?, ?, ?, ?, ?)', rows)
    con.commit()
    return cur, con

def saveTrackStatus(path):
    url = path + 'TrackStatus.jsonStream'
    resp = requests.get(url)
    entries = resp.text.split('\r\n')
    del(entries[len(entries) - 1])
    timing, data = splitTiming(entries)
    
    cur, con = createCursor(path)
    rows = []

    for i in range(len(timing)):
        streamtiming = timing[i]
        status, message = manageKey(data[i], ["Status", "Message"])
        row = (streamtiming, status, message)
        rows.append(row)

    cur.execute('CREATE TABLE TrackStatus(Stream Timestamp, Status, Message)')
    cur.executemany('INSERT INTO TrackStatus VALUES(?, ?, ?)', rows)
    con.commit()
    return cur, con