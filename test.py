# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 23:42:46 2016

@author: D
"""

from geometry import *
from dynamics import *

S = schwarzschild(1., 1.)
k = 3
v = 1/(2*k)**0.5
#v = (1-1/k)**0.5

r = k*S.rs

x0 = S.get_point_by_coords([r, np.pi/2, 0, 0])
dirc = S.get_vec_by_coords(x0, [0, 0, v/r, 1.])
dirc = dirc.normalize()

thing = body(dirc)

thing.set_frame([S.get_vec_by_coords(x0, [-1, 0, 0, 0]),
                               S.get_vec_by_coords(x0, [0, 0, 1, 0]),
                               S.get_vec_by_coords(x0, [0, 1, 0, 0])])

print thing.get_mass()

path = []
pad1 = []

dn = False

tot_time = 70.
tms = linspace(0, tot_time, 20)
step = tms[1]-tms[0]
for ct in tms:
    #path.append(dirc)
    #dirc = S.parallel_transport(dirc, S.dif_scale(dirc,0.01) )
    thing.advance(step, mode = 'coord')
    if (not dn) and ct > tot_time*0.8:
        dn = True
        print 'done'
        thing.shoot2(S.get_outward_dir(thing.get_pt()), 0.25, 0.5)
        print 'bam!!'
    path.append(thing.get_velocity())
    pad1.append(thing.get_space_vectors()[0])

import matplotlib.pyplot as plt

vpathx = []
vpathy = []
for d in path:
    q = d.pt.q
    vpathx.append(q[0]*np.cos(q[2]))
    vpathy.append(q[0]*np.sin(q[2]))

vpad1x = []
vpad1y = []
for d in pad1:
    r = d.q
    q = d.pt.q
    vpad1x.append(r[0]*np.cos(q[2])-r[2]*q[0]*np.sin(q[2]))
    vpad1y.append(r[0]*np.sin(q[2])+r[2]*q[0]*np.cos(q[2]))


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
eps = 4.
for x, y, dx, dy in zip(vpathx, vpathy, vpad1x, vpad1y):
    ax.plot([x, x+eps*dx], [y, y+eps*dy], color = 'green')
#plt.plot(p2x, p2y)
#plt.plot(vpathx, vpathy, 'o')