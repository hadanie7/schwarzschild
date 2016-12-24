# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 15:03:26 2016

@author: Jonatan Hadas
"""

import math
import cmath

import pygame

def compose_transform(vec1, vec2):
    '''
    Creates transform from standard base to base vec1,vec2 as a composition of scaling and rotating
    scaling returned as (scale_x, scale_y)
    rotating returned as angle in radians
    '''
    rev_res = []
    x1,y1 = vec1
    x2,y2 = vec2
    if x1*x2*y1*y2 >= 0:
        a1 = math.atan2(y1,x1)
        a2 = math.atan2(y2,x2)
        a = -(a1+a2)/2
        rev_res.append(a)
        cp1,cp2 = x1+1j*y1, x2+1j*y2
        cp1 *= cmath.exp(1j*a)
        cp2 *= cmath.exp(1j*a)
        x1,y1 = cp1.real,cp1.imag
        x2,y2 = cp2.real,cp2.imag
    a = math.sqrt(-x1*x2/(y1*y2))
    rev_res.append((a,1))
    x1 /= a
    x2 /= a
    ang = math.atan2(y1,x1)
    rev_res.append(-ang)
    rev_res.append((x1**2+y1**2, x2**2+y2**2))
    
    return reversed(rev_res)

def apply_transform(img, series):
    for t in series:
        if isinstance(t, (float,int,long)):
            print -math.degrees(t)
            img = pygame.transform.rotate(img,-math.degrees(t))
        elif isinstance(t, tuple):
            sx,sy = t
            w,h = img.get_size()
            w *= sx
            h *= sy
            w = int(w)
            h = int(h)
            img = pygame.transform.smoothscale(img, (w,h))
    return img