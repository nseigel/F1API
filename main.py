import display_segment as segment
from turtle import *
import retrieve as r
import paths as p
import database as db
import sqlite3

# screen = Screen()
# screen.screensize(500, 500)
# t = Turtle()

#segment.draw_segment(5000, 5130, 55, 300, "red", False)
#segment.draw_segment(2023, 'Spielberg', 'Sprint', 4000, 4100, 1, 300, "purple", False, t)
#segment.draw_lap('Race', 'Spielberg', 2024, 63, 'NOR', 300, 'orange', t)
# segment.draw_lap('Race', 'Spielberg', 2024, 63, 'VER', 300, 'blue', t)
# segment.draw_lap('Race', 'Spielberg', 2024, 63, 'RUS', 300, 'green', t)
# t.hideturtle()

#live.display_drivers('Sprint', 'Spielberg', 2024, [["HAM", 'red'], ["VER", 'blue']], 0.5, 300)

# timestamps = r.get_position_data(2024, 'Spielberg', 'Race', 1, 5000, 5100)[3]
# print(timestamps)

#db.saveCarData(p.find_session("Race", 'Monza', 2023))
#db.savePosition(p.find_session("Race", 'Spielberg', 2024))
# db.saveSessionInfo(p.find_session("Race", 'Spielberg', 2024))
#db.saveSessionData(p.find_session("Race", 'Spielberg', 2024))
# db.saveHeartbeat(p.find_session("Race", 'Spielberg', 2024))
#db.saveTrackStatus(p.find_session("Race", 'Spielberg', 2024))
#db.saveAudioStreams(p.find_session("Race", 'Spielberg', 2024))
#db.saveChampionshipPrediction(p.find_session("Race", 'Spielberg', 2024))
#db.saveExtrapolatedClock(p.find_session("Race", 'Spielberg', 2024))
#db.saveLapCount(p.find_session("Race", 'Spielberg', 2024))
#db.saveDriverRaceInfo(p.find_session("Race", 'Spielberg', 2024))
#db.saveTyreStintSeries(p.find_session("Race", 'Spielberg', 2024))
#db.saveLapSeries(p.find_session("Race", 'Spielberg', 2024))
#db.saveName("Race", "Spielberg", 2024, p.find_session("Race", 'Spielberg', 2024))
# cur, con = db.createCursor(p.find_session("Race", 'Spielberg', 2024))
# for row in cur.execute("SELECT Driver, Lap FROM LapSeries"):
#     print(row)

# for row in cur.execute("SELECT Central, Status, Message FROM TrackStatus"):
#     print(row)

#db.saveSession('Race', 'Yas Marina Circuit', 2023)