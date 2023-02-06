from typing import List, Tuple

import numpy as np


def get_min_hours(cars_start_time: list, optimum: list, maximum_mode: list, cars_charge: list,
                  maximum_load: int, cars_capacity: list) -> tuple[list[int], list[float]]:
    hours = []
    hour = 0
    for car, time in enumerate(cars_start_time):
        cars_charge[car] *= cars_capacity[car] / 100
        for h, load in enumerate(optimum[time:]):
            hour += 1
            if maximum_mode[car]:
                cars_charge[car] += maximum_load
            else:
                cars_charge[car] += load
            optimum[h + time] = 0
            if cars_charge[car] >= cars_capacity[car]:
                optimum[h + time] += (cars_charge[car] - cars_capacity[car])
                cars_charge[car] = cars_capacity[car]
                break
        hours.append(hour)
        optimum = [round(elem, 1) for elem in optimum]
    return hours, optimum


def get_delta_load(optimum_load: int, maximum_load: int, car_charge: float,
                   req_car_charge: float, time: int, end: int, mode: dict):
    delta = (req_car_charge - car_charge) / (end - time)
    if delta > optimum_load:
        delta = optimum_load
    for i in mode:
        charge = i.split('-')
        if int(charge[0]) <= car_charge <= int(charge[1]) and delta > mode[i]:
            delta = mode[i]
    car_charge += delta
    optimum_load -= delta
    maximum_load -= delta
    return delta, round(car_charge, 2), optimum_load, maximum_load
