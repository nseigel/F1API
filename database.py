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
    for row in rows:
        timing, value = text.split('{', 1)
        value = json.loads("{" + data)
        data.append(value)
    return data

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
    url = path + "SessionInfo.jsonStream"
    resp = requests.get(url)
    data = splitTiming(resp.text)[0]

    cur, con = createCursor(path)

    cur.execute('CREATE TABLE SessionInfo(Name, OfficialName, Location, Country, Circuit, SessionName, StartDate, EndDate, Path)')
    to_enter = [
        (data['Meeting']['Name'], data['Meeting']['OfficialName'], data['Meeting']['Location'], data['Meeting']['Country']["Name"], data['Meeting']['Circuit']['ShortName'], data['Name'], data['StartDate'], data['EndDate'], data['Path'])
    ]

    cur.executemany('INSERT INTO SessionInfo VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', to_enter)
    con.commit()
    return cur, con

def saveArchiveStatus(path):
    url = path + 'ArchiveStatus.jsonStream'
    resp = requests.get(url)
    data = splitTiming(resp.text)[0]
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