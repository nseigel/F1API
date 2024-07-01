import retrieve as r
import math
import numpy as np
from numpy.polynomial import Polynomial as P
import matplotlib.pyplot as plt

def get_distance_between(point_a, point_b):
    x = point_b[0] - point_a[0]
    y = point_b[1] - point_a[1]
    distance = math.sqrt((x * x) + (y * y))
    return abs(distance)

def get_time_between(time_a, time_b):
    time_delta = time_b - time_a
    seconds = time_delta.microseconds/1000000 + time_delta.seconds
    return seconds

def get_distance_points(year, circuit, session, driver, lap):
    driver_x, driver_y, timestamps = r.get_lap_positions(year, circuit, session, driver, lap)
    distances = []
    times = []
    total_distance = 0
    previous_point = [driver_x[0], driver_y[0]]
    for i in range(len(driver_x)):
        distance_between = get_distance_between(previous_point, [driver_x[i], driver_y[i]])
        total_distance += distance_between
        distances.append(total_distance)
        times.append(get_time_between(timestamps[0], timestamps[i]))
        previous_point = [driver_x[i], driver_y[i]]
    return(times, distances)

def get_pol_function(x, y):
    #plt.plot(x, y)
    distance = P.fit(x, y, 30) # 14 is the degree of the polynomial
    dx, dy = distance.linspace(100)  # generate 100 sample points on this graph
    #plt.plot(dx, dy)  # plot the calculated polynomial
    speed = P.deriv(distance)
    sx, sy = speed.linspace(100)
    #plt.plot(sx, sy)
    acc = P.deriv(speed)
    ax, ay = acc.linspace(100)
    plt.plot(ax, ay)

    plt.show()
x, y = get_distance_points(2023, "Hungaroring", "Race", "VER", 20)
get_pol_function(x, y)