from turtle import *
import time
import normalise as n
import retrieve as r
import display_segment as d
import info as l

def init_turtles(drivers):
    for driver in drivers:
        driver.append(Turtle())
        driver[2].color(driver[1])
    return drivers

def driver_positions(session, circuit, year, drivers):
    positions = r.get_live_positions(session, circuit, year)
    for driver in drivers:
        driver[3] = positions[driver[0]][0]
        driver[4] = positions[driver[0]][1]
    return drivers

def display_drivers(session, circuit, year, drivers, interval):
    drivers = init_turtles(drivers)
    for driver in drivers:
        driver.append(0)
        driver.append(0)
    for i in range(10):
        drivers = driver_positions(session, circuit, year, drivers)
        for driver in drivers:
            driver[2].goto(driver[3], driver[4])
        time.sleep(interval)

