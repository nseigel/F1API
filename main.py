import display_segment as segment
from turtle import *
import retrieve as r

screen = Screen()
screen.screensize(50, 50)
t = Turtle()

#segment.draw_segment(5000, 5130, 55, 300, "red", False)
#segment.draw_segment(2023, 'Spielberg', 'Sprint', 4000, 4100, 1, 300, "purple", False, t)
segment.draw_lap('Race', 'Spielberg', 2024, 63, 'NOR', 300, 'orange', t)
# segment.draw_lap('Race', 'Spielberg', 2024, 63, 'VER', 300, 'blue', t)
# segment.draw_lap('Race', 'Spielberg', 2024, 63, 'RUS', 300, 'green', t)
# t.hideturtle()

#live.display_drivers('Sprint', 'Spielberg', 2024, [["HAM", 'red'], ["VER", 'blue']], 0.5, 300)

screen.exitonclick()

# timestamps = r.get_position_data(2024, 'Spielberg', 'Race', 1, 5000, 5100)[3]
# print(timestamps)