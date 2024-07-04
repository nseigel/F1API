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

# db.saveSessionData(p.find_session("Race", 'Spielberg', 2024))
# cur, con = db.createCursor(p.find_session("Race", 'Spielberg', 2024))
# for row in cur.execute("SELECT Utc, Lap Number FROM RaceLaps"):
#     print(row)

# for row in cur.execute("SELECT Utc, Track Status, Session Status FROM TrackSessionStatus"):
#     print(row)