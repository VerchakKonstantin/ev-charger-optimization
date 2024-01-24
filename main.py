import numpy as np
import pandas as pd
import math
import os
import matplotlib.pyplot as plt
from numpy import random
import config
from algorithms import *

optimum_load = pd.read_excel(config.optimum_load)['Load'].tolist()

print(optimum_load)
for i, load in enumerate(optimum_load):
    if load > config.maximum_load:
        optimum_load[i] = config.maximum_load
print(optimum_load)
# min_hours, optimum = get_min_hours(config.cars_start_time, optimum_load.copy(), config.maximum_mode,
#                                    config.cars_charge, config.maximum_load, config.car_capacity)
# print('Full charging min hours for every car', min_hours)
# print('Load after charging', optimum)
charging = {}
cars_charge = config.cars_charge
new_load = []
charging_cars = {}
for h, load in enumerate(optimum_load):
    maximum_load = config.maximum_load
    for i, time in enumerate(config.cars_start_time):
        if not charging.get(f'{i}'):
            charging.update(i={})
        if time <= h and cars_charge[i] < config.req_cars_charge[i]:
            print(h, cars_charge[i], load)
            delta, car_charge, load, maximum_load = get_delta_load(load, maximum_load, config.maximum_mode[i],
                                                                   cars_charge[i], config.req_cars_charge[i], h,
                                                                   config.cars_time[i], config.mode)
            load -= delta
            try:
                charging_cars[i]['time'].append(h)
                charging_cars[i]['charge'].append(delta)
            except:
                charging_cars[i] = {'time': [h], 'charge': [round(delta, 2)]}
            cars_charge[i] = car_charge

    new_load.append(load)
print(charging_cars)
print('Load after charging', new_load)
