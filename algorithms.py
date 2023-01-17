import numpy as np


def get_min_hours(cars_start_time: list, optimum_load: list, maximum_mode: list, cars_charge: list,
                  maximum_load: int, cars_capacity: list) -> list:
    hours = []
    hour = 0
    for car, time in enumerate(cars_start_time):
        cars_charge[car] *= cars_capacity[car] / 100
        for h, load in enumerate(optimum_load[time:]):
            hour += 1
            if maximum_mode[car]:
                cars_charge[car] += maximum_load
            else:
                cars_charge[car] += load
            optimum_load[h + time] = 0
            if cars_charge[car] >= cars_capacity[car]:
                optimum_load[h + time] += (cars_charge[car] - cars_capacity[car])
                cars_charge[car] = cars_capacity[car]
                break
        hours.append(hour)
    return hours
