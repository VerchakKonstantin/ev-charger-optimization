def get_min_hours(cars_start_time: list, optimum: list, maximum_mode: list, cars_charge: list,
                  maximum_load: int, cars_capacity: list) -> tuple[list[int], list[float]]:
    """
    function for calculate min hours for full charge
    :param cars_start_time: start time for every car
    :param optimum: list of optimum load
    :param maximum_mode: bool mode for using maximum load
    :param cars_charge: start charge for every car
    :param maximum_load: maximum load of charger
    :param cars_capacity: capacity of battery for every car
    :return: hours for every car and load after charging
    """
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


def get_delta_load(optimum_load: int, maximum_load: int, maximum_mode: list, car_charge: float,
                   req_car_charge: float, time: int, end: int, mode: dict = 0):
    """
    function calculate delta load for charging the car
    :param optimum_load: optimum load at present hour
    :param maximum_load: maximum load of charger
    :param car_charge: start charge of car
    :param req_car_charge: requirement charge of car
    :param time: present hour
    :param end: end time of car
    :param mode: mode of charging
    :return: delta load, car charge, optimum load and maximum load
    """
    delta = round((req_car_charge - car_charge) / (end - time), 2)
    if delta > optimum_load:
        if maximum_mode:
            delta = maximum_mode
        else:
            delta = optimum_load
    if mode != 0:
        for i in mode:
            charge = i.split('-')
            if int(charge[0]) <= car_charge <= int(charge[1]) and delta > mode[i]:
                delta = mode[i]
    car_charge += delta
    maximum_load -= delta
    return delta, round(car_charge, 2), maximum_load
