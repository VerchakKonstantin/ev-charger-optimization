import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
import ast
from algorithms import get_delta_load


def calculate_charge(optimum_load, maximum_load, cars_charge, cars_start_time,
                     req_cars_charge, maximum_mode, cars_time, mode):
    optimum = optimum_load.
    for i, load in enumerate(optimum):
        if load > maximum_load:
            optimum[i] = maximum_load
    charging_cars = {}
    max = maximum_load
    for h, load in enumerate(optimum):
        maximum_load = max
        for i, time in enumerate(cars_start_time):
            if time <= h and cars_charge[i] < req_cars_charge[i]:
                delta, car_charge, load, maximum_load = get_delta_load(load, maximum_load, maximum_mode[i],
                                                                       cars_charge[i], req_cars_charge[i], h,
                                                                       cars_time[i], mode)
                load -= delta
                cars_charge[i] = car_charge
                try:
                    charging_cars[i]['time'].append(h)
                    charging_cars[i]['charge'].append(delta)
                except:
                    charging_cars[i] = {'time': [h], 'charge': [round(delta, 2)]}
    return charging_cars


def update_plot(ax, plot_canvas, params):
    maximum_load, cars_charge, req_cars_charge, cars_start_time, cars_time, maximum_mode, car_capacity, mode = params

    try:
        maximum_load = float(maximum_load.get())
        cars_charge = ast.literal_eval(cars_charge.get())
        req_cars_charge = ast.literal_eval(req_cars_charge.get())
        cars_start_time = ast.literal_eval(cars_start_time.get())
        cars_time = ast.literal_eval(cars_time.get())
        maximum_mode = ast.literal_eval(maximum_mode.get())
        car_capacity = ast.literal_eval(car_capacity.get())
        mode = ast.literal_eval(mode.get())
    except ValueError:
        print('Yes')
    # maximum_load = 40

    # int number of cars
    n_cars = 2

    # list int cars charge in % for every car
    # cars_charge = [30, 45]

    # list int required cars charge in % for every car
    # req_cars_charge = [95, 90]

    # list int cars charging time in h for every car
    # cars_time = [5, 8]

    # list int cars start charging time in h for every car
    # cars_start_time = [2, 4]

    # list bool maximum charging mode for every car
    # maximum_mode = [True, False]

    # list float battery capacity for every car
    # car_capacity = [70.0, 82.0]

    # dict with maximum kw mode of charging for various % of charge
    mode = {'34-50': 8, '51-60': 3, '61-85': 13}
    df = pd.read_excel('optimum_load_data.xlsx')
    data = df['Load'].tolist()
    index_list = list(df.index.values)

    charging = calculate_charge(data, maximum_load, cars_charge, cars_start_time,
                                req_cars_charge, maximum_mode, cars_time, mode)
    print(charging)
    # charge = {'1': {'time': [2, 3, 4, 5], 'charge': [10, 15, 22, 10]},
    #           '2': {'time': [5, 6, 7], 'charge': [5, 10, 15]}}
    ax.clear()
    ax.plot(index_list, data, label='Оптимум')
    ax.axhline(y=maximum_load, color='r', linestyle='--', label='Максимальная нагрузка')
    for key, value in charging.items():
        ax.bar(value['time'], value['charge'], width=1, edgecolor="white", label=f'Машина {key}', linewidth=0.7)

    ax.set_xlabel('Время, ч')
    ax.set_ylabel('кВтч')
    ax.legend()

    plot_canvas.draw()


def exit_app(root):
    root.destroy()


def main():
    root = tk.Tk()
    root.title('Оптимизация зарядки электрокаров')
    root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))

    # Создаем виджеты
    maximum_load_label = ttk.Label(root, text='Максимальная нагрузка')
    maximum_load = ttk.Entry(root)

    cars_charge_label = ttk.Label(root, text='Начальный заряд электрокаров')
    cars_charge = ttk.Entry(root)

    req_cars_charge_label = ttk.Label(root, text='Требуемый конечный заряд')
    req_cars_charge = ttk.Entry(root)

    cars_start_time_label = ttk.Label(root, text='Время приезда автомобиля')
    cars_start_time = ttk.Entry(root)

    cars_time_label = ttk.Label(root, text='Время на зярядке')
    cars_time = ttk.Entry(root)

    maximum_mode_label = ttk.Label(root, text='Режим максимума')
    maximum_mode = ttk.Entry(root)

    car_capacity_label = ttk.Label(root, text='Ёмкость батареи электрокара')
    car_capacity = ttk.Entry(root)

    mode_label = ttk.Label(root, text='Режимы зарядки')
    mode = ttk.Entry(root)

    params = [maximum_load, cars_charge, req_cars_charge, cars_start_time,
              cars_time, maximum_mode, car_capacity, mode]

    calculate_button = ttk.Button(root, text='Рассчитать',
                                  command=lambda: update_plot(ax, plot_canvas, params))
    exit_button = ttk.Button(root, text='Выход', command=lambda: exit_app(root))

    # Создаем объект Figure и ось для графика
    fig = Figure(figsize=(root.winfo_screenwidth() / 100, root.winfo_screenheight() / 120), dpi=100)
    ax = fig.add_subplot(1, 1, 1)

    # Создаем холст для отображения графика в Tkinter
    plot_canvas = FigureCanvasTkAgg(fig, master=root)
    plot_canvas_widget = plot_canvas.get_tk_widget()
    plot_canvas_widget.grid(row=0, column=0, columnspan=10)

    # Размещаем виджеты с использованием grid
    maximum_load_label.grid(row=1, column=0, padx=10, pady=5)
    maximum_load.grid(row=2, column=0, padx=10, pady=5)

    cars_charge_label.grid(row=1, column=1, padx=10, pady=5)
    cars_charge.grid(row=2, column=1, padx=10, pady=5)

    req_cars_charge_label.grid(row=1, column=2, padx=10, pady=5)
    req_cars_charge.grid(row=2, column=2, padx=10, pady=5)

    cars_start_time_label.grid(row=1, column=3, padx=10, pady=5)
    cars_start_time.grid(row=2, column=3, padx=10, pady=5)

    cars_time_label.grid(row=1, column=4, padx=10, pady=5)
    cars_time.grid(row=2, column=4, padx=10, pady=5)

    maximum_mode_label.grid(row=1, column=5, padx=10, pady=5)
    maximum_mode.grid(row=2, column=5, padx=10, pady=5)

    car_capacity_label.grid(row=1, column=6, padx=10, pady=5)
    car_capacity.grid(row=2, column=6, padx=10, pady=5)

    mode_label.grid(row=1, column=7, padx=10, pady=5)
    mode.grid(row=2, column=7, padx=10, pady=5)

    calculate_button.grid(row=1, column=8, columnspan=3, pady=10)
    exit_button.grid(row=2, column=8, columnspan=3, pady=10)

    # Запускаем цикл обработки событий Tkinter
    root.mainloop()


if __name__ == '__main__':
    main()
