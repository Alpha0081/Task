#!/usr/bin/env python
# -*- coding: utf-8 -*-

from fdtd.fdtd import FDTD
from fdtd.layer import Layer
from fdtd.boundary import ABCFirstLeft, ABCFirstRight
from fdtd.source import SourceModulatedGaussian
import numpy as np
import pyqtgraph as pg

if __name__ == "__main__":
    fdtd = FDTD(1.5, 5e-3, 2e-8, 1)
    fdtd.add_source(SourceModulatedGaussian(0.75, 1e-8, 1e-9, 0.6e-9, 0))
    fdtd.add_layer(Layer([0, 1.5], 4))
    fdtd.set_left_boundary(ABCFirstLeft())
    fdtd.set_right_boundary(ABCFirstRight())
    fdtd.add_probes([1.25])
    fdtd.analyze()
    fdtd.show_probe_signals()
    probe = fdtd.get_probe()
    frequency = np.fft.fftfreq(int(2e-8 // fdtd.dt))
    spectr = np.fft.fft(probe[0].E)
    p = pg.plot()
    p.plot(frequency / fdtd.dt, abs(spectr) / max(abs(spectr)))
    p.showGrid(x=True,y=True)
    pg.exec()
