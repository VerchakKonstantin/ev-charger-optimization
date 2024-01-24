# str path to excel data with optimum load per hours
optimum_load = 'optimum_load_data.xlsx'

# int maximum load for ev charger
maximum_load = 40

# int number of cars
n_cars = 2

# list int cars charge in % for every car
cars_charge = [30, 45]

# list int required cars charge in % for every car
req_cars_charge = [95, 90]

# list int cars charging time in h for every car
cars_time = [5, 8]

# list int cars start charging time in h for every car
cars_start_time = [2, 4]

# list bool maximum charging mode for every car
maximum_mode = [True, False]

# list float battery capacity for every car
car_capacity = [70.0, 82.0]

# dict with maximum kw mode of charging for various % of charge
mode = {'34-50': 8, '51-60': 3, '61-85': 13}
