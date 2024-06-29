from turtle import *
import datetime
import time
import normalise as n
import retrieve as r

import requests

def visualize_segment(driver_x, driver_y, timestamps, turtle):
    turtle.goto(driver_x[0], driver_y[0])
    prev_timestamp = 0
    for i in range(len(driver_x)):
        timestamp = timestamps[i]
        if i != 0:
            time_delta = timestamp - prev_timestamp
            total_delta = time_delta.microseconds + time_delta.seconds * 1000000
            time.sleep(total_delta/1000000)
        turtle.goto(driver_x[i], driver_y[i])
        prev_timestamp = timestamp

def draw_segment(year, circuit, session, start_time, end_time, driver_number, factor, colour, visualize, turtle):
    driver_x, driver_y, timestamps = r.get_position_data(year, circuit, session, driver_number, start_time, end_time)
    processed_data = n.normalize([driver_x, driver_y], factor)
    driver_x = processed_data[0]
    driver_y = processed_data[1]
    turtle.color(colour)
    turtle.penup()
    turtle.goto(driver_x[0], driver_y[0])
    turtle.pendown()
    for i in range(len(driver_x)):
        turtle.goto(driver_x[i], driver_y[i])

    turtle.penup()
    if visualize:
        visualize_segment(driver_x, driver_y, timestamps)