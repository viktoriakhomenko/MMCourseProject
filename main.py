import numpy as np
from scipy import interpolate
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
from tkinter import filedialog as fd
import tkinter.messagebox as mb


def enter_data(file):
    x = []
    for i in range(2):
        cur = []
        cur.append(file['x1'][i])
        cur.append(file['x2'][i])
        cur.append(file['x3'][i])
        cur.append(file['x4'][i])
        cur.append(file['x5'][i])
        cur.append(file['x6'][i])
        cur.append(file['x7'][i])
        cur.append(file['x8'][i])
        cur.append(file['x9'][i])
        cur.append(file['x10'][i])
        cur.append(file['x11'][i])
        cur.append(file['x12'][i])
        x.append(cur)
    return x


def cler_data(x):
    difs = []
    for el in x:
        for i in range(len(el) - 1):
            xi = el[i]
            xii = el[i + 1]
            difs.append(abs(xii - xi))
    avg_dif = np.average(difs)

    x_clear = []
    for el in x:
        cur = [el[0]]
        for i in range(1, len(el)):
            if (abs(el[i - 1] - el[i]) / avg_dif >= 2):
                cur.append(np.average([el[i - 1], el[i]]))
            else:
                cur.append(el[i])
        x_clear.append(cur)
    return x_clear


def sezonnost(x):
    t = []
    for row in x:
        for el in row:
            t.append(el)

    coef = []
    cur = [0, 0, 0, 0, 0]
    k = 0
    for i in range(5, len(t) - 5):
        j = i
        if (i > 11):
            j = i - 12
            k = 1
        x_avg = np.average(t[i:i + 5])
        if (j < 11):
            cur.append(x[k][j] / x_avg)
        else:
            cur.append(x[k][j] / x_avg)
            coef.append(cur)
            cur = []
    for i in range(5):
        cur.append(0)
    coef.append(cur)

    sez_coef = []
    for i in range(len(x[0])):
        if i < len(x[0]) - 5:
            sez_coef.append(coef[1][i])
        else:
            sez_coef.append(coef[0][i])
    return sez_coef


def find_trend(x, c):
    x_trend = []
    for i in range(len(x[0])):
        x_trend.append(x[1][i] / c[i])
    return x_trend


def extrapolate(x):
    xx = [i for i in range(len(x))]
    yy = x
    f = interpolate.interp1d(xx, yy, fill_value="extrapolate")
    extap_trend = []
    for i in range(len(x)):
        tt = float(f(i + 12))
        extap_trend.append(tt)
    return extap_trend


def prediction(x, c):
    resuslt = []
    for i in range(len(x)):
        resuslt.append(round(x[i] * c[i], 1))
    return resuslt


def plot_draw(y):
    x = [i for i in range(1, 13)]
    plt.plot(x, y, 1, 0, 13, 60)
    plt.show()


def main():
    col_names = ["x1", "x2", "x3", "x4", "x5", "x6", "x7", "x8", "x9", "x10", "x11", "x12"]
    file = pd.read_csv("data.csv", names=col_names, sep=',', header=None)
    x = enter_data(file)
    x_clear = cler_data(x)
    sez = sezonnost(x_clear)
    trend = find_trend(x_clear, sez)
    extr = extrapolate(trend)
    p = prediction(extr, sez)
    return x, p


def clicked():
    x, p = main()
    lbl = Label(window, text='Entered data:\n' + str(x[0]) + '\n' + str(x[1]), font=("Arial Bold", 9))
    lbl.grid(column=0, row=1)
    lbl2 = Label(window, text='Prediction data:\n' + str(p), font=("Arial Bold", 9))
    lbl2.grid(column=0, row=2)
    plot_draw(p)


window = Tk()
window.geometry('400x300')
window.title("Prediction")
lb = Label(window, text='\tПрогнозування попиту на товари \n\tInput data: data.csv', font=("Arial Bold", 9))
lb.grid(column=0, row=0)
btn = Button(window, text="Predict", command=clicked)
btn.grid(column=0, row=1)
window.mainloop()