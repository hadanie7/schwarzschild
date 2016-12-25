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
        assert Ps.pt is self.get_pt()
        newP = self.get_P() - Ps
        
        assert Ps.is_timelike()
        assert newP.is_timelike()
        # TODO: check validity of the new P's
        
        self.boost(newP)
        return body(Ps)
    
    def shoot2(self, d, mass, energy):
        m = self.get_mass()
        ms = mass ; del mass
        E = energy ; del energy
        
        v = self.get_velocity()
        d = d.ortho_part(v) # just make sure d is a space vector in my frame
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
        """print '-----------'
        print d*d, v*v, d*v, v*d
        print E, ms, m
        print self.get_mass()
        print Ps.get_time()"""
        return self.shoot(Ps)
        
    def set_frame(self, vectors):
        self.mass = self.P.get_time()
        v = (1./ self.mass) * self.P
        base = gram_schmidt([v]+vectors)
        self.frame = foref(base[0], base[1:])
        del self.P
    
    def get_P(self):
        if self.has_frame():
            return self.mass * self.frame.vel
        else:
            return self.P
    
    def get_pt(self):
        if self.has_frame():
            return self.frame.vel.pt
        else:
            return self.P.pt
    
    def has_frame(self):
        return hasattr(self, 'frame')
    
    def get_velocity(self):
        if self.has_frame():
            return self.frame.vel
        else:
            return (1./ self.get_mass()) * self.P 
    
    def get_space_vectors(self):
        return self.frame.space
    
        
    def advance(self, time, mode = 'self'):
        """ advance by the given amount of time.
        parameters:
            mode: determines how time is measured. accepted values: 'self', 'coord' """
        it_count = 0
        stop = False
        ttrans = None

        P = self.get_P()
        if self.has_frame():
            self.frame.diagnostics()
        while True:
            
            inc = self.man.dif_scale(P)
            if mode == 'self':
                t_inc = inc.get_time()
            elif mode == 'coord':
                t_inc = inc.q[3]
            else:
                raise Exception()
            
            if t_inc >= time:
                cur_inc = (time/t_inc)*inc
                stop = True
            else:
                cur_inc = inc
                time -= t_inc
            
            trans = self.man.get_parallel_transport(cur_inc)
            P = trans(P)
            if self.has_frame():
                if ttrans is None:
                    ttrans = trans
                else:
                    ttrans = trans*ttrans
            
            if stop: break
            
            it_count += 1
            if (it_count) > 5000: raise Exception('too many iterations.')
        
        if self.has_frame():
            self.transport(ttrans)
        else:
            self.P = P
    
    def transport(self, m):
        if self.has_frame():
            self.frame.transport(m)
        else:
            self.P = m(self.P)
    
    def boost(self, newP):
        if not self.has_frame():
            self.P = newP
            return
        self.mass = newP.get_time()
        newV = newP.normalize()
        del_v = newV - self.get_velocity()
        self.frame.lorentz(del_v)
        
    
    def get_mass(self):
        if self.has_frame():
            return self.mass
        else:
            return self.P.get_time()

class foref:
    def __init__(self, vel, space):
        assert isinstance(vel, vector)
        assert len(space) == 3
        for s in space:
            assert isinstance(s, vector)
           
        assert vel.is_timelike()
        self.vel = vel
        self.space = space
        
    
    def lorentz(self, del_v):
        v = self.vel
        self.diagnostics()
        # gam = v*(v+del_v)
        # v*del_v = 1-gam
        # gm1 = gam-1
        # eqs: 
        # x = alp*v + bet*del_v
        # x*x = 1, x*v = 0
        # solution: xs = x*sqrt(gam-1) = (gam-1)/sqrt(gam+1)*v + 1/sqrt(gam+1)*del_v
        # eqs:
        # x -> ax + by, x*x=1 x*v = 0
        # a = gam, b = sqrt(gam**2-1)
        # y = (x*y)x + y-(x*y)x
        # y -> y + (x*y)(ax+bv) - (x*y)x
        # y -> y + (x*y)((a-1)x+bv)
        # y -> y + (x*y) ((gam-1)x + sqrt(gam**2-1)*v)
        # y -> y + (xs*y) (xs + sqrt(gam+1)*v)
        n_vel = v + del_v        
               
        gm1 = (-1.)* v*del_v
        sp1 = np.sqrt(gm1+2)
        
        xs = (gm1 / sp1)*v + 1./sp1*del_v
        
        n_space = [y+(xs*y)*(xs+sp1*v) for y in self.space]
        
        self.vel = n_vel
        self.space = n_space
        self.diagnostics()
        
    def transport(self, m):
        assert isinstance(m, lin_map)
        self.vel = m(self.vel)
        self.space = [m(s) for s in self.space]
    
    def diagnostics(self):
        vcs = [self.vel] + list(self.space)
        print 'foref diagnostics:'
        print np.array([[v*u for v in vcs] for u in vcs])
        #print [[v*u for v in vcs] for u in vcs]
        print ''
        