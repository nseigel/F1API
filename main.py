import display_segment as segment
from turtle import *
import retrieve as r
import paths as p
import database as db
import sqlite3
import matplotlib.pyplot as plt
import normalise as n
import functions as f

#EXPLORING TABLES

# cur, con = db.createCursor(p.find_session('Race', 'Spa-Francorchamps', '2024'))

# for row in cur.execute("SELECT Central, LastLapTime, PersonalFastest FROM LastLapTimes WHERE Driver = '23'"):
#     print(row)



#GRAPHING CAR DATA
# cur, con = db.createCursor(p.find_session('Race', 'Spa-Francorchamps', '2024'))

# rows = []
# for row in cur.execute("SELECT Brake, Throttle FROM CarData WHERE DriverNumber = '1'"):
#     rows.append(row)

# brakes = []
# throttle = []
# entries = []
# for i in range(20200, 20601):
#     brakes.append(rows[i][0])
#     throttle.append(rows[i][1])

# for i in range(0, 401):
#     entries.append(i)

# plt.plot(entries, brakes)
# plt.plot(entries, throttle)
# plt.legend(['Brakes', 'Throttle'])
# plt.savefig('THROTTLE', dpi=300, bbox_inches='tight')
# plt.show()

#GRAPHING PLOTS OF LAPS
# cur, con = db.createCursor(p.find_session('Race', 'Suzuka', '2023'))

# rows = []
# for row in cur.execute("SELECT X, Y FROM Positions WHERE DriverNumber = '1'"):
#     rows.append(row)

# x = []
# y = []
# for i in range(19400, 21001):
#     x.append(n.normalize_live(rows[i][0], 1, 'Suzuka'))
#     y.append(n.normalize_live(rows[i][1], 1, 'Suzuka'))

# plt.ylim((0.0, 1.0))
# plt.xlim((0.0, 1.0))
# plt.plot(x, y, 'blue', linewidth = 0.5)
# plt.show()



# GRAPHING POSITION DATA
# cur, con = db.createCursor(p.find_session("Race", 'Spa-Francorchamps', 2024))
# laps44 = []
# positions44 = []
# for row in cur.execute("SELECT Central, Driver, Lap, Position FROM LapSeries WHERE Driver = '44'"):
#     laps44.append(int(row[2]))
#     positions44.append(int(row[3]))

# laps63 = []
# positions63 = []
# for row in cur.execute("SELECT Lap, Position FROM LapSeries WHERE Driver = '63'"):
#     laps63.append(int(row[0]))
#     positions63.append(int(row[1]))

# laps81 = []
# positions81 = []
# for row in cur.execute("SELECT Lap, Position FROM LapSeries WHERE Driver = '81'"):
#     laps81.append(int(row[0]))
#     positions81.append(int(row[1]))

# laps16 = []
# positions16 = []
# for row in cur.execute("SELECT Lap, Position FROM LapSeries WHERE Driver = '16'"):
#     laps16.append(int(row[0]))
#     positions16.append(int(row[1]))

# laps1 = []
# positions1 = []
# for row in cur.execute("SELECT Lap, Position FROM LapSeries WHERE Driver = '1'"):
#     laps1.append(int(row[0]))
#     positions1.append(int(row[1]))

# laps11 = []
# positions11 = []
# for row in cur.execute("SELECT Lap, Position FROM LapSeries WHERE Driver = '11'"):
#     laps11.append(int(row[0]))
#     positions11.append(int(row[1]))

# laps14 = []
# positions14 = []
# for row in cur.execute("SELECT Lap, Position FROM LapSeries WHERE Driver = '14'"):
#     laps14.append(int(row[0]))
#     positions14.append(int(row[1]))

# laps55 = []
# positions55 = []
# for row in cur.execute("SELECT Lap, Position FROM LapSeries WHERE Driver = '55'"):
#     laps55.append(int(row[0]))
#     positions55.append(int(row[1]))

# plt.plot(laps44, positions44, "purple")
# plt.plot(laps63, positions63, "blue")
# plt.plot(laps81, positions81, 'orange')
# plt.plot(laps16, positions16, 'pink')
# plt.plot(laps1, positions1, 'navy')
# plt.plot(laps11, positions11, 'yellow')
# plt.plot(laps14, positions14, 'green')
# plt.plot(laps55, positions55, 'red')
# plt.title('Driver Position Data for the 2024 F1 Belgian Grand Prix')
# plt.xlabel('Lap')
# plt.ylabel('Position')
# plt.legend(['Lewis Hamilton', 'George Russel', 'Oscar Piastri', 'Charles Leclerc', 'Max Verstappen', 'Sergio Perez', 'Fernando Alonso', 'Carlos Sainz'], bbox_to_anchor = (1.2, -0.2), ncol = 4)
# plt.savefig('LAPSERIES', dpi=300, bbox_inches='tight')
# plt.show()