import sqlite3
import paths as p
import requests
import json
import codecs
import zlib
import base64
import datetime

def convert_time(timestamp):
    timestamp = timestamp[0:26]
    timestamp = timestamp.replace('Z', '0')
    while len(timestamp) < 26:
        timestamp = timestamp + '0'
    timestamp = timestamp + '+00:00'
    time = datetime.datetime.fromisoformat(timestamp)
    return time

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

def saveName(session, circuit, year, path):
    url = path + "SessionInfo.jsonStream"
    resp = requests.get(url)
    timing, data = resp.text.split('{', 1)
    data = json.loads("{" + data)
    session = data['Name']
    db_name = session + '_' + path.split('/')[5]
    rows = [
        (session, circuit, year, db_name),
        ]
    con = sqlite3.connect('db/SessionLookup.db')
    cur = con.cursor()
    try:
        cur.execute('CREATE TABLE DbName(Session, Circuit, Year, DbName)')
    except sqlite3.OperationalError:
        pass
    cur.executemany('INSERT INTO DbName VALUES(?, ?, ?, ?)', rows)
    con.commit()


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

    cur.execute('CREATE TABLE TrackStatus(Central, Status, Message)')
    cur.executemany('INSERT INTO TrackStatus VALUES(?, ?, ?)', rows)
    con.commit()
    return cur, con

def saveSessionData(path):
    url = path + 'SessionData.jsonStream'
    resp = requests.get(url)
    rows = resp.text.split('\r\n')
    del(rows[len(rows) - 1])
    central, data = splitTiming(rows)
    laprows = []
    trackrows = []
    sessionrows = []
    index = 0
    for entry in data:
        try:
            lap = entry['Series']
            for key in lap:
                utc = lap[key]['Utc']
                lapnum = lap[key]['Lap']
                row = (central[index], utc, lapnum)
                laprows.append(row)
        except KeyError:
            pass

        try: 
            status = entry['StatusSeries']
            for key in status:
                if index == 0:
                    trackstatus = status[0]['TrackStatus']
                    utc = status[0]['Utc']
                else:
                    trackstatus = status[key]['TrackStatus']
                    utc = status[key]['Utc']
                row = (central[index], utc, trackstatus)
                trackrows.append(row)
        except KeyError:
            pass

        try: 
            status = entry['StatusSeries']
            for key in status:
                if index == 0:
                        sessionstatus = status[0]['SessionStatus']
                        utc = status[0]['Utc']
                else:
                    sessionstatus = status[key]['SessionStatus']
                    utc = status[key]['Utc']
                row = (central[index], utc, sessionstatus)
                sessionrows.append(row)
        except KeyError:
            pass
        index += 1
    
    cur, con = createCursor(path)
    cur.execute('CREATE TABLE SessionLaps(Central, Utc, Lap)')
    cur.execute('CREATE TABLE SessionTrackStatus(Central, Utc, TrackStatus)')
    cur.execute('CREATE TABLE SessionStatus(Central, Utc, SessionStatus)')
    cur.executemany('INSERT into SessionLaps VALUES(?, ?, ?)', laprows)
    cur.executemany('INSERT into SessionTrackStatus VALUES(?, ?, ?)', trackrows)
    cur.executemany('INSERT into SessionStatus VALUES(?, ?, ?)', sessionrows)
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

def saveAudioStreams(path):
    url = path + 'AudioStreams.json'
    resp = requests.get(url)
    data = json.loads(codecs.decode(resp.content, encoding='utf-8-sig'))
    
    cur, con = createCursor(path)

    streams = data['Streams']
    rows = []
    for stream in streams:
        name, language, uri, path, utc = manageKey(stream, ["Name", "Language", "Uri", "Path", "Utc"])
        row = (name, language, uri, path, utc)
        rows.append(row)

    cur.execute('CREATE TABLE AudioStreams(Name, Language, Uri, Path, Utc)')
    cur.executemany('INSERT INTO AudioStreams VALUES(?, ?, ?, ?, ?)', rows)
    con.commit()
    return cur, con

def saveChampionshipPrediction(path):
    url = path + 'ChampionshipPrediction.jsonStream'
    resp = requests.get(url)
    rows = resp.text.split('\r\n')
    del(rows[len(rows) - 1])
    central, data = splitTiming(rows)
    driverrows = []
    teamrows = []

    index = 0
    for entry in data:
        try:
            for key in entry['Drivers']:
                driver = key
                time = central[index]
                position, points = manageKey(entry['Drivers'][key], ['PredictedPosition', 'PredictedPoints'])
                row = (time, driver, position, points)
                driverrows.append(row)
        except KeyError:
            pass
        try:
            for key in entry['Teams']:
                team = key
                time = central[index]
                position, points = manageKey(entry['Teams'][key], ['PredictedPosition', 'PredictedPoints'])
                row = (time, team, position, points)
                teamrows.append(row)
        except KeyError:
            pass
        index += 1

    cur, con = createCursor(path)
    cur.execute("CREATE TABLE DriversChampionshipPrediction(Central, Driver, PredictedPosition, PredictedPoints)")
    cur.execute("CREATE TABLE TeamsChampionshipPrediction(Central, Team, PredictedPosition, PredictedPoints)")
    cur.executemany("INSERT INTO DriversChampionshipPrediction VALUES(?, ?, ?, ?)", driverrows)
    cur.executemany("INSERT INTO TeamsChampionshipPrediction VALUES(?, ?, ?, ?)", teamrows)
    con.commit()
    return cur, con

def saveExtrapolatedClock(path):
    url = path + 'ExtrapolatedClock.jsonStream'
    resp = requests.get(url)
    rows = resp.text.split('\r\n')
    del(rows[len(rows) - 1])
    central, data = splitTiming(rows)
    rows = []

    index = 0
    for entry in data:
        utc, remaining, extrapolating = manageKey(entry, ['Utc', 'Remaining', 'Extrapolating'])
        time = central[index]
        row = (time, utc, remaining, extrapolating)
        rows.append(row)
        index += 1

    cur, con = createCursor(path)
    cur.execute('CREATE TABLE ExtrapolatedClock(Central, Utc, Remaining, Extrapolating)')
    cur.executemany("INSERT INTO ExtrapolatedClock VALUES(?, ?, ?, ?)", rows)
    con.commit()

    return cur, con

def savePosition(path):
    url = path + 'Position.z.jsonStream'
    resp = requests.get(url)
    entries = resp.text.split('\r\n')
    del(entries[len(entries) - 1])
    
    timings = []
    data = []
    for entry in entries:
        timing, datum, _ = entry.split('"')
        timings.append(timing)
        data.append(json.loads(zlib.decompress(base64.b64decode(datum), -zlib.MAX_WBITS)))
    
    rows = []
    index = 0
    for line in data:
        for entry in line['Position']:
            timestamp = entry['Timestamp']
            central = timings[index]
            for key in entry['Entries']:
                time = timestamp
                driver_number = key
                status, x, y, z, = manageKey(entry['Entries'][key], ['Status', 'X', 'Y', 'Z'])
                row = (central, time, driver_number, x, y, z)
                rows.append(row)
        index += 1
    
    cur, con = createCursor(path)
    cur.execute('CREATE TABLE Positions(Central, Utc, DriverNumber, X, Y, Z)')
    cur.executemany('INSERT INTO Positions VALUES(?, ?, ?, ?, ?, ?)', rows)
    con.commit()

    return cur, con

#channel predictions
#Zero: RPM
#Two: speed
#FortyFive: DRS
#Three: Gear
#Four: Throttle?
#Five: Brakes?
def saveCarData(path):
    url = path + 'CarData.z.jsonStream'
    resp = requests.get(url)
    entries = resp.text.split('\r\n')
    del(entries[len(entries) - 1])
    
    timings = []
    data = []
    for entry in entries:
        timing, datum, _ = entry.split('"')
        timings.append(timing)
        data.append(json.loads(zlib.decompress(base64.b64decode(datum), -zlib.MAX_WBITS)))

    rows = []
    index = 0
    for line in data:
        for entry in line['Entries']:
            central = timings[index]
            utc = entry['Utc']
            for key in entry['Cars']:
                driver_number = key
                chan0, chan2, chan3, chan4, chan5, chan45 = manageKey(entry['Cars'][key]['Channels'], ['0', '2', '3', '4', '5', '45'])
                row = (central, utc, driver_number, chan0, chan2, chan3, chan4, chan5, chan45)
                rows.append(row)
        index += 1

    cur, con = createCursor(path)
    cur.execute('CREATE TABLE CarData(Central, Utc, DriverNumber, RPM, Speed, Gear, Throttle, Brake, DRS)')
    cur.executemany('INSERT INTO CarData VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)', rows)
    con.commit()
    
    return cur, con

def saveLapCount(path):
    url = path + 'LapCount.jsonStream'
    resp = requests.get(url)
    rows = resp.text.split('\r\n')
    del(rows[len(rows) - 1])
    central, data = splitTiming(rows)

    rows = []
    index = 0
    for entry in data:
        time = central[index]
        current, total = manageKey(entry, ['CurrentLap', 'TotalLaps'])
        row = (time, current, total)
        rows.append(row)
        index += 1
    
    cur, con = createCursor(path)
    cur.execute("CREATE TABLE LapCount(Central, CurrentLap, TotalLaps)")
    cur.executemany("INSERT INTO LapCount VALUES(?, ?, ?)", rows)
    con.commit()

    return cur, con

def saveDriverRaceInfo(path):
    url = path + 'DriverRaceInfo.jsonStream'
    resp = requests.get(url)
    rows = resp.text.split('\r\n')
    del(rows[len(rows) - 1])
    central, data = splitTiming(rows)

    rows = []
    index = 0
    for entry in data:
        for key in entry:
            driver_number = key
            gap, interval, catching = manageKey(entry[key], ['Gap', 'Interval', 'Catching'])
            time = central[index]
            row = (time, driver_number, gap, interval, catching)
            rows.append(row)
        index += 1
    
    cur, con = createCursor(path)
    cur.execute('CREATE TABLE DriverRaceInfo(Central, Driver, Gap, Interval, Catching)')
    cur.executemany("INSERT INTO DriverRaceInfo VALUES(?, ?, ?, ?, ?)", rows)
    con.commit()
    return cur, con

def saveTyreStintSeries(path):
    url = path + 'TyreStintSeries.jsonStream'
    resp = requests.get(url)
    rows = resp.text.split('\r\n')
    del(rows[len(rows) - 1])
    central, data = splitTiming(rows)
    
    rows = []
    index = 0
    for entry in data:
        for key in entry['Stints']:
            try:
                driver_number = key
                time = central[index]
                for stint in entry['Stints'][key]:
                    stint_number = stint
                    compound, new, tyresnotchanged, totallaps, startlaps = manageKey(entry["Stints"][key][stint], ["Compound", "New", 'TyresNotChanged', 'TotalLaps', 'StartLaps'])
                    row = (time, driver_number, stint_number, compound, new, tyresnotchanged, totallaps, startlaps)
                    rows.append(row)
            except TypeError:
                pass
        index += 1

    cur, con = createCursor(path)
    cur.execute('CREATE TABLE TyreStintSeries(Central, Driver, Stint, Compound, New, TyresNotChanged, TotalLaps, StartLaps)')
    cur.executemany("INSERT INTO TyreStintSeries VALUES(?, ?, ?, ?, ?, ?, ?, ?)", rows)
    con.commit()
    return cur, con


def saveHeartbeat(path):
    url = path + 'Heartbeat.jsonStream'
    resp = requests.get(url)
    rows = resp.text.split('\r\n')
    del(rows[len(rows) - 1])
    central, utc = splitTiming(rows)
    start = central[0]
    end = central[len(central) - 1]
    i = 0
    while i < len(central):
        if central[i] == start or central[i] == end:
            del(central[i])
            del(utc[i])
        else:
            i += 1
    rows = []
    for i in range(len(central)):
        utc[i] = convert_time(utc[i]['Utc'])
        row = (central[i], str(utc[i]))
        rows.append(row)

    cur, con = createCursor(path)
    cur.execute('CREATE TABLE Heartbeat(Central, Utc)')
    cur.executemany("INSERT INTO Heartbeat VALUES(?, ?)", rows)
    con.commit()
    return cur, con

def saveLapSeries(path):
    url = path + 'LapSeries.jsonStream'
    resp = requests.get(url)
    rows = resp.text.split('\r\n')
    del(rows[len(rows) - 1])
    del(rows[0])
    central, data = splitTiming(rows)
    
    rows = []
    index = 0
    for entry in data:
        time = central[index]
        for key in entry:
            driver = key
            for lap in entry[key]['LapPosition']:
                position = entry[key]['LapPosition'][lap]
                row = (time, driver, lap, position)
                rows.append(row)
    
    cur, con = createCursor(path)
    cur.execute('CREATE TABLE LapSeries(Central, Driver, Lap, Position)')
    cur.executemany('INSERT INTO LapSeries VALUES(?, ?, ?, ?)', rows)
    con.commit()

    return cur, con

def saveSession(session, circuit, year):
    path = p.find_session(session, circuit, year)
    saveName(session, circuit, year, path)
    saveSessionInfo(path)
    saveArchiveStatus(path)
    saveTrackStatus(path)
    saveSessionData(path)
    saveContentStreams(path)
    saveAudioStreams(path)
    #saveChampionshipPrediction(path)
    saveExtrapolatedClock(path)
    savePosition(path)
    saveCarData(path)
    saveLapCount(path)
    saveDriverRaceInfo(path)
    saveTyreStintSeries(path)
    saveHeartbeat(path)
    saveLapSeries(path)

def saveTimingData(path):
    url = path + 'TimingData.jsonStream'
    resp = requests.get(url)
    rows = resp.text.split('\r\n')
    del(rows[len(rows) - 1])
    central, data = splitTiming(rows)
    #print(data)
    sectors = []
    speedtraps = []
    bestlaptimes = []
    lastlaptimes = []
    index = 0
    for row in data:
        for driver in row['Lines']:
            # gapLeader, numLaps, inPit, status = manageKey(row['Lines'][driver], ['GapToLeader', 'NumberOfLaps', 'InPit', 'Status'])
            # interval, catching = manageKey(row['Lines'][driver]['IntervalToPositionAhead'], ['Value', 'Catching'])
            try:
                lastLapTime, personalFastest = manageKey(row['Lines'][driver]['LastLapTime'], ['Value', 'PersonalFastest'])
                lastlaptimes.append([central[index], driver, lastLapTime, personalFastest])
            except KeyError:
                pass
            try:
                bestlaptime, lapnum = manageKey(row['Lines'][driver]['BestLapTime'], ['Value', 'Lap'])
                bestlaptimes.append([central[index], driver, bestlaptime, lapnum])
            except KeyError:
                pass
            # try:
            #     for sector in row['Lines'][driver]['Sectors']:
            #         sectorValue, personalFastest, previousValue = manageKey(row['Lines'][driver]['Sectors'][sector], ['Value', 'PersonalFastest', 'PreviousValue'])
            #         sectors.append(central[index], driver, sector, sectorValue, personalFastest, previousValue)
            # except KeyError:
            #     pass
            try:
                for speed in row['Lines'][driver]['Speeds']:
                    speedValue, personalFastest = manageKey(row['Lines'][driver]['Speeds'][speed], ['Value', 'PersonalFastest'])
                    speedtraps.append([central[index], driver, speed, speedValue, personalFastest])
            except KeyError:
                pass

        index += 1

    cur, con = createCursor(path)
    cur.execute('CREATE TABLE SpeedTraps(Central, Driver, SpeedTrap, SpeedValue, PersonalFastest)')
    cur.executemany('INSERT INTO SpeedTraps VALUES(?, ?, ?, ?, ?)', speedtraps)
    cur.execute('CREATE TABLE BestLapTimes(Central, Driver, BestLapTime, LapNum)')
    cur.executemany('INSERT INTO BestLapTimes VALUES(?, ?, ?, ?)', bestlaptimes)
    cur.execute('CREATE TABLE LastLapTimes(Central, Driver, LastLapTime, PersonalFastest)')
    cur.executemany('INSERT INTO LastLapTimes VALUES(?, ?, ?, ?)', lastlaptimes)
    con.commit()

#ADD SEGMENT DATA
#ADD SECTOR DATA
#ADD INTERVALS
#ADD BESTLAPTIME


def test(path):
    url = path + 'TimingDataF1.jsonStream'
    resp = requests.get(url)
    print(resp.text)
    
#saveTimingData(p.find_session("Race", 'Spa-Francorchamps', 2024))

# saveSession('Race', 'Spielberg', 2024)