#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from os import path, makedirs
import json 

t = np.linspace(-15, 5, 100)
y = 100 * (abs(1 - 0.01 * t ** 2)) ** .5 + 0.01 * abs(t + 10) 

if not path.exists("results"):
    makedirs("results")

with open('results/function.json', 'w') as json_file:
    dictionary = {"x": list(t), "y": list(y)}
    json.dump(dictionary, json_file, separators=(',',' = '), indent=4)
json_file.close()

plt.grid()
plt.plot(t, y)
plt.show()

