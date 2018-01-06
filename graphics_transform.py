# -*- coding: utf-8 -*-
"""
Created on Sat Dec 24 15:03:26 2016

@author: Jonatan Hadas
"""

import math
import numpy as np

import pygame

def compose_transform(vec1, vec2):
    '''
    Creates transform from standard base to base vec1,vec2 as a composition of scaling and rotating
    scaling returned as (scale_x, scale_y)
    rotating returned as angle in radians
    '''
    fix = np.diag([1,-1])
    
    mat = np.array([vec1,vec2]).T
    
    
    r1,s,r2 = np.linalg.svd(mat)

    if np.linalg.det(r1)<0:
        r1 = np.dot(r1,fix)
        s[1] = -s[1]
    if np.linalg.det(r2)<0:
        r2 = np.dot(fix,r2)
        s[1] = -s[1]
        
    if np.all(s<0):
        s = -s
        r1 = -r1
    

    a1 = math.atan2(r1[1,0],r1[0,0])
    a2 = math.atan2(r2[1,0],r2[0,0])
    
        
    return a2,tuple(s),a1
    

def apply_transform(img, series):
    for t in series:
        if isinstance(t, (float,int,long)):
            img = pygame.transform.rotate(img,-math.degrees(t))
        elif isinstance(t, tuple):
            sx,sy = t
            w,h = img.get_size()
            w *= sx
            h *= sy
            w = abs(int(w))
            h = abs(int(h))
            if sx<0 or sy<0:
                img = pygame.transform.flip(img, sx<0, sy<0)
            img = pygame.transform.smoothscale(img, (w,h))
    return img