import sqlite3
import paths as p
import requests
import json

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
    timing, data = resp.text.split('{', 1)
    data = json.loads("{" + data)

    cur, con = createCursor(path)

    cur.execute('CREATE TABLE SessionInfo(Name, OfficialName, Location, Country, Circuit, SessionName, StartDate, EndDate, Path)')
    to_enter = [
        (data['Meeting']['Name'], data['Meeting']['OfficialName'], data['Meeting']['Location'], data['Meeting']['Country']["Name"], data['Meeting']['Circuit']['ShortName'], data['Name'], data['StartDate'], data['EndDate'], data['Path'])
    ]

    cur.executemany('INSERT INTO SessionInfo VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', to_enter)
    con.commit()
    return con

