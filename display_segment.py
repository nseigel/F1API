from turtle import *
import datetime
import time
import normalise as n
import retrieve as r

import requests

def visualize_segment(driver_x, driver_y, timestamps):
    t.goto(driver_x[0], driver_y[0])
    prev_timestamp = 0
    for i in range(len(driver_x)):
        timestamp = timestamps[i]
        if i != 0:
            time_delta = timestamp - prev_timestamp
            total_delta = time_delta.microseconds + time_delta.seconds * 1000000
            time.sleep(total_delta/1000000)
        t.goto(driver_x[i], driver_y[i])
        prev_timestamp = timestamp

def draw_segment(year, circuit, session, start_time, end_time, driver_number, factor, colour, visualize):
    driver_x, driver_y, timestamps = r.get_position_data(year, circuit, session, driver_number, start_time, end_time)
    processed_data = n.normalize([driver_x, driver_y], factor)
    driver_x = processed_data[0]
    driver_y = processed_data[1]
    t.color(colour)
    t.penup()
    t.goto(driver_x[0], driver_y[0])
    t.pendown()
    for i in range(len(driver_x)):
        t.goto(driver_x[i], driver_y[i])

    t.penup()
    if visualize:
        visualize_segment(driver_x, driver_y, timestamps)

screen = Screen()
screen.screensize(50, 50)
t = Turtle()

#draw_segment(5000, 5130, 55, 300, "red", False)
draw_segment(2023, 'Spa-Francorchamps', 'Sprint', 1000, 1100, 44, 300, "red", False)

screen.exitonclick()