import PySimpleGUI as sg
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import config
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def draw_plot(path_excel: str, window):
    df = pd.read_excel(path_excel)
    data = df.values.tolist()
    index_list = list(df.index.values)
    fig, ax = plt.subplots()
    ax.plot(index_list, data, label='Optimum load')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title('Load on charger')
    ax.legend()
    canvas = window['-CANVAS-'].TKCanvas
    fig_agg = FigureCanvasTkAgg(fig, canvas)
    fig_agg.draw()
    fig_agg.get_tk_widget().pack(side='top', fill='both', expand=1)


def main():
    layout = [[sg.Text('Choose excel file'), sg.InputText(default_text=str(config.optimum_load),
                                                          key='-excel-'), sg.FileBrowse(), sg.Button('Draw plot')],
              [sg.Canvas(key='-CANVAS-')],
              [sg.Button('Exit'), sg.Button('Calculate')],
              [sg.Text('Enter car start charge'), sg.Input(default_text=str(config.cars_charge), key='-INPUT_CHARGE-')]]

    window = sg.Window('My Window Title', layout, finalize=True)



    # interface process
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED or event == 'Exit':
            break
        elif event == 'Calculate':
            print('cool')
            cars_charge = values['-INPUT_CHARGE-']
            print(cars_charge)
        elif event == 'Draw plot':
            path_excel = values['-excel-']
            print(path_excel)
            draw_plot(path_excel, window)

    window.close()


# Executes main
if __name__ == '__main__':
    main()
