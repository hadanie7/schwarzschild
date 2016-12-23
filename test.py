# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 23:42:46 2016

@author: D
"""

from geometry import *

S = schwarzschild(1., 1.)
k = 3
v = 1/(2*k)**0.5 /1.3
#v = (1-1/k)**0.5

r = k*S.rs

x0 = S.get_point_by_coords([r, np.pi/2, 0, 0])
dirc = x0.get_vector([0, 0, v/r, 1.])

path = []

for i in range(10000):
    path.append(dirc)
    dirc = S.parallel_transport(dirc, S.dif_scale(dirc,0.01) )

import matplotlib.pyplot as plt

vpathx = []
vpathy = []
for d in path:
    q = d.pt.q
    vpathx.append(q[0]*np.cos(q[2]))
    vpathy.append(q[0]*np.sin(q[2]))

p2x = []
p2y = []
for d in path:
    q = d.pt.q
    p2x.append(q[1])
    p2y.append(q[3])

xsw, ysw = S.rs*cos(linspace(0,np.pi*2)), S.rs*sin(linspace(0,np.pi*2))


fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_aspect('equal', 'datalim')
ax.plot(xsw, ysw, color='black')
ax.plot(vpathx, vpathy)
#plt.plot(p2x, p2y)
#plt.plot(vpathx, vpathy, 'o')