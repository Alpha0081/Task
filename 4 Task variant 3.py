#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fdtd.fdtd import FDTD
from fdtd.layer import Layer
from fdtd.source import SourceGauss
from fdtd.boundary import ABCSecondLeft, ABCSecondRight
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    fdtd = FDTD(1, 5e-4, 1e-8, 1)
    fdtd.add_layer(Layer((0.7, 0.76), 3.5))
    fdtd.add_layer(Layer((0.76, 0.82), 2.2))
    fdtd.add_layer(Layer((0.82, 0.92), 4))
    fdtd.add_layer(Layer((0.92, 1), 6))
    fdtd.set_left_boundary(ABCSecondLeft())
    fdtd.set_right_boundary(ABCSecondRight())
    fdtd.add_probes([0.125, 0.375])
    F_max = 5e9
    A_0 = 1e12
    A_max = 1e4
    wg = np.log(A_max) ** .5 / (np.pi * F_max)
    dg = wg * np.log(A_0) ** .5
    fdtd.add_source(SourceGauss(0.25, dg, wg))
    fdtd.analyze()
    fdtd.show_probe_signals()
    probe = fdtd.get_probe()
    frequency = np.fft.fftfreq(int(1e-8 // fdtd.dt))
    signal_full = probe[1].E
    signal_reflect = probe[0].E
    signal = np.zeros(signal_full.size)
    delay_arg = 2 * int(0.125 // fdtd.dx) + int((wg + dg) // fdtd.dt) - 1
    signal[:delay_arg] = signal_full[:delay_arg]

    t = np.arange(0, 1e-8 - fdtd.dt , fdtd.dt)

    plt.plot(t * 1e9, signal, label="Падающий сигнал")
    plt.plot(t * 1e9, signal_reflect, label="Отражённый сигнал")
    plt.xlabel("Время, нс")
    plt.ylabel("Сигнал")
    plt.legend(loc="upper right")
    plt.grid()
    plt.show()

    spectr_2 = np.fft.fft(signal)
    spectr_1 = np.fft.fft(signal_reflect)



    plt.plot(frequency / fdtd.dt, abs(spectr_1), label = "Спектр отражённой волны")
    plt.plot(frequency / fdtd.dt, abs(spectr_2), label = "Спектр падающей волны")
    plt.grid()
    plt.xlim((-F_max, F_max))
    plt.xlabel("Частота, Гц")
    plt.ylabel("Амплитуда")
    plt.legend(loc="upper right")
    plt.show()


    plt.plot(frequency / fdtd.dt, abs(spectr_1) / abs(spectr_2))
    plt.ylabel("Модуль коэффициента отражения")
    plt.xlabel("Частота, Гц")
    plt.grid()
    plt.xlim((0, F_max))
    plt.ylim((0, 1))
    plt.show()
