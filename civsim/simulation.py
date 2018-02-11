from civsim.main import *
from copy import deepcopy

import matplotlib.pyplot as plt
import numpy as np

steps = 160000
interval = 2000

r = Region()

population = []
ww, wl, ll = [], [], []
xaxis = np.arange(steps)
for i in xaxis:
    r.step()


    if (i+1)%interval == 0:
        ww.append(Accum.winwin)
        wl.append(Accum.winlose)
        ll.append(Accum.loselose)
        Accum.clear()

        population.append(len(r.people))

    # # for a closer look
    # if options.VERBOSE == True:
    #     input()
    # if len(r.people) > 200:
    #     options.VERBOSE = True


fig, ax1 = plt.subplots()
ax1.set_xlabel('time')
# Make the y-axis label, ticks and tick labels match the line color.

g_axis = np.arange(0, steps, interval)
ax1.plot(g_axis, ww, label='ww', color='g')
ax1.plot(g_axis, wl, label='wl', color='y')
ax1.plot(g_axis, ll, label='ll', color='r')


ax1.plot(g_axis, np.sum((ww, wl, ll), axis=0), 'b--', label='ww')

ax1.set_ylabel('interactions', color='r')
ax1.tick_params('y', colors='r')


ax2 = ax1.twinx()


ax2.set_ylabel('population', color='b')
ax2.tick_params('y', colors='b')
ax2.plot(g_axis, population, label='pop')

fig.tight_layout()
plt.show()

input('hey')
options.VERBOSE = True
while True:
    r.step()
    c = input()
