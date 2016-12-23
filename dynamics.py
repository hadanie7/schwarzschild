# -*- coding: utf-8 -*-
"""
Created on Wed Dec 14 15:16:21 2016

@author: D
"""

from geometry import *

class body:
    def __init__(self,P):
        assert isinstance(P, vector)
        self.P = P
        self.man = P.pt.man
        assert P.is_timelike()
    
    def shoot(self, Ps):
        assert Ps.pt is self.P.pt
        self.P = self.P - Ps
        
        assert Ps.is_timelike()
        assert self.P.is_timelike()
        # TODO: check validity of the new P's
        return body(Ps)
    
    def get_velocity(self):  
        return self.P / self.get_inv_mass()
        
    def advance(self, time, mode = 'self'):
        """ advance by the given amount of time.
        parameters:
            mode: determines how time is measured. accepted values: 'self', 'coord' """
        inc = self.man.dif_scale(self.P)
        if mode == 'self':
            t_inc = inc.get_time()
        elif mode == 'coord':
            t_inc = inc.q[3]
        else:
            raise Exception()
        
        if t_inc >= time:
            self.P = self.man.parallel_transport(self.P, (time/t_inc)*inc )
        else:
            self.P = self.man.parallel_transport(self.P, inc)
            self.advance(time-t_inc, mode)
    
    def get_inv_mass(self):
        return -self.P.get_norm()

class foref:
    def __init__(self, vel, space):
        assert isinstance(vel, vector)
        self.vel = vel
        self.man = vel.pt.man
        assert vel.is_timelike()
    
    
        
        