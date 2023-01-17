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
min_hours = get_min_hours(config.cars_start_time, optimum_load, config.maximum_mode,
                          config.cars_charge, config.maximum_load, config.car_capacity)
print(min_hours)
