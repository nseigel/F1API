import display_segment as segment
import display_live as live
from turtle import *

screen = Screen()
screen.screensize(50, 50)
t = Turtle()

#segment.draw_segment(5000, 5130, 55, 300, "red", False)
segment.draw_segment(2023, 'Spielberg', 'Sprint', 4000, 4100, 1, 300, "purple", False, t)
t.hideturtle()

#live.display_drivers('Sprint', 'Spielberg', 2024, [["HAM", 'red'], ["VER", 'blue']], 0.5, 300)

#screen.exitonclick()