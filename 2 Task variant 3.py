#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import xml.etree.ElementTree as ET
import numpy as np
from scipy.special import spherical_jn, spherical_yn
import matplotlib.pyplot as plt

#url = "https://jenyay.net/uploads/Student/Modelling/task_02.xml"

#response = requests.get(url)

#with open("data.xml", "wb") as f:
#    f.write(response.content)

tree = ET.parse('data.xml')
root = tree.getroot()

c = 3e8
eps = 1e-12


for i, child in enumerate(root):
    if i == 2:
        D = float(child.attrib["D"])
        fmin = float(child.attrib["fmin"])
        fmax = float(child.attrib["fmax"])


h = lambda n, z: spherical_jn(n, z) + 1j * spherical_yn(n, z)

f = np.arange(fmin, fmax + 1, 1e6)
_lambda = c / f
r = D / 2
RCS_array = np.zeros(f.size)
for j, __lambda in enumerate(_lambda):
    k = 2 * np.pi / __lambda
    RCS = 0
    RCS_old = -1
    n = 1
    while abs(RCS - RCS_old) >= eps:            
        a = spherical_jn(n, k * r) / h(n, k * r)
        b = (k * r * spherical_jn(n - 1, k * r) - n * spherical_jn(n, k * r)) / (k * r * h(n - 1, k * r) - n * h(n, k * r))
        RCS_old = RCS
        RCS += (-1) ** n * (n + 0.5) * (b - a)
        n += 1
    RCS_array[j] = __lambda ** 2 / np.pi * abs(RCS) ** 2

plt.plot(f / 1e9, RCS_array)
plt.grid()
plt.xlabel("Частота, ГГц")
plt.ylabel("ЭПР, м²")
data = ET.Element('data')
data_frequency = ET.SubElement(data, 'frequencydata')
data_lambda = ET.SubElement(data, 'lambdadata')
data_rcs = ET.SubElement(data, 'rcsdata')

for i in range(f.size):
    _f = ET.SubElement(data_frequency, 'f')
    _f.text = str(f[i])
    __lambda = ET.SubElement(data_lambda, 'lambda')
    __lambda.text = str(_lambda[i])
    RCS = ET.SubElement(data_rcs, 'rcs')
    RCS.text = str(RCS_array[i])
xml_data = ET.ElementTree(data)

with open("RCS.xml", "wb") as out:
    xml_data.write(out, encoding='utf-8')
out.close()

plt.show()
