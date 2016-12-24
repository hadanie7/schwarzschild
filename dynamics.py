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
        print self.get_mass()
        return body(Ps)
    
    def shoot2(self, d, mass, energy):
        m = self.get_mass()
        ms = mass ; del mass
        E = energy ; del energy
        
        P = self.P
        v = self.get_velocity()
        """print v
        print P
        print d
        print d*P
        print (d*P/P.sq())
        print (d*P/P.sq())*P"""
        d = d.ortho_part(P) # just make sure d is a space vector in my frame
        d = d.normalize() # length 1
        
        # equations: [Eq(l*l-k*k, ms*ms), Eq(-k*k+(m-l)**2, (m-ms-E)**2)]
        # ks = k**2
        ks = E * (E + 2*ms) * (E/m - 2) * (E/m - 2 + 2*ms/m) * 0.25
        l = -E*E/(2*m) + E - E*ms/m + ms
        """print 'eqs:'
        print l*l-ks, ms*ms
        print -ks+(l+m)**2, (m-ms-E)**2"""
        # Ps = k*d + l*v = k*d + l/m * m*v
        Ps = np.sqrt(ks) * d  +  l*v
        #print locals()
        print '-----------'
        print d*d, v*v, d*v, v*d
        print E, ms, m
        print self.get_mass()
        print Ps.get_time()
        return self.shoot(Ps)
        
        
    
    def get_velocity(self):  
        return (1./ self.get_mass()) * self.P 
    
        
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
    
    def get_mass(self):
        return self.P.get_time()

class foref:
    def __init__(self, vel, space):
        assert isinstance(vel, vector)
        self.vel = vel
        self.man = vel.pt.man
        assert vel.is_timelike()
    
    
        
        