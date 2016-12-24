# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 21:59:57 2016

@author: D
"""

import numpy as np

class point:
    def __init__(self, man, q):
        self.man = man
        self.q = q
    
    def get_vector(self, q):
        return vector(self, q)
    
class vector:
    def __init__(self, pt, q):
        self.pt = pt
        self.q = np.array(q)
    
    def scale(self, lamb):
        return vector(self.pt, self.q.copy()*lamb)
    
    def sq(self):
        return self*self
    
    def get_time(self):
        sq = -self.sq()
        assert sq > 0
        return np.sqrt(sq)
    
    def get_length(self):
        sq = self.sq()
        assert sq > 0
        return np.sqrt(sq)

    def is_timelike(self):
        return self.sq() <= 0
        
    def __add__(self, v2):
        assert isinstance(v2, vector)
        assert self.pt is v2.pt
        return vector(self.pt, self.q+v2.q)
    
    def __sub__(self, v2):
        assert isinstance(v2, vector)
        assert self.pt is v2.pt
        return vector(self.pt, self.q-v2.q)
    
    def __mul__(self, val2): 
        return self.pt.man.inner_product(self, val2)
    
    def __rmul__(self, lamb):
        try:
            return self.scale(float(lamb))
        except:
            pass
        raise Exception("incompatible type for multiplication")
    
    def __repr__(self):
        return 'vec' + repr(self.q)
    
    def project_on(self, v2):
        return (self*v2 / v2.sq()) * v2
    
    def ortho_part(self, v2):
        return self - (self*v2 / v2.sq()) * v2
    
    
    
def gram_schmidt(vs):
    us = []
    for v in vs:
        for u in us:
            v = v - (v*u/u.sq())*u
        v = 1./(np.sqrt(np.abs(v.sq()))) * v
        us.append(v)
        

class manifold:
    def __init__(self, dim):
        self.dim = dim
    
    def get_point_by_coords(self, q):
        return point(self, np.array(q))
    
    def christ(self, pt, i, j, k):
        NotImplemented #virtual
    
    def gram(self, pt):
        NotImplemented #virtual
    
    def dif_scale(self, v, d):
        NotImplemented #virtual
    
    """ parallel transport of the vector v by a short increment dt """
    def parallel_transport2(self, v, dt):
        assert isinstance(v, vector); assert isinstance(dt, vector)
        assert v.pt is dt.pt
        D = np.zeros(self.dim)
        
        for k in range(self.dim):
            for i in range(self.dim):
                for j in range(self.dim):
                    D[k] -= self.christ2(v.pt, i, j, k) * dt.q[i] * v.q[j]
        npt = point(self, v.pt.q + dt.q)
        
        return vector(npt, v.q+D)        
        
        ####### debug
        if not hasattr(self, 'ftp'):
            self.ftp = 0
        if self.ftp < 5:
            print D
        self.ftp += 1

    """ parallel transport of the vector v by a short increment dt """
    def parallel_transport(self, v, dt):
        assert isinstance(v, vector); assert isinstance(dt, vector)
        assert v.pt is dt.pt
        D = -np.tensordot(self.christ(v.pt), np.outer(v.q, dt.q))
        npt = point(self, v.pt.q + dt.q)
        
        return vector(npt, v.q+D)
        
        ####### debug
        if not hasattr(self, 'ftp'):
            self.ftp = 0
        if self.ftp < 5:
            print D
        self.ftp += 1
    
    def inner_product(self, v1, v2):
        assert isinstance(v1, vector); assert isinstance(v2, vector)
        assert v1.pt is v2.pt
        return np.inner(v1.q, np.inner(self.gram(v1.pt) ,v2.q))

class schwarzschild(manifold):
    """ coordinates: r, theta, phi, t
        signature:   +  +      +    - """    
    
    def __init__(self, G, m):
        manifold.__init__(self, 4)
        self.G = G
        self.m = m
        self.rs = 2*G*m
        
    def christ2(self, pt, i, j, k):
        r, th, ph, t = pt.q
        B = -(1-self.rs/r)
        A = -1/B
        At = -self.rs/r**2 * A**2
        Bt = -self.rs/r**2
        i,j,k = i+1, j+1, k+1
        i, j = sorted([i,j]) # exploit symmetry
        if (k==1):
            if (i==j):
                if i==1:
                    return At/(2*A)
                elif i==2:
                    return -r/A
                elif i==3:
                    return -r*(np.sin(th)**2)/A
                else:
                    return -Bt/(2*A)
        elif (k==2):
            if (i==1 and j==2):
                return 1/r
            elif (i==3 and j==3):
                return -np.sin(th)*np.cos(th)
        elif k==3:
            if (j == 3):
                if (i==1):
                    return 1/r
                elif (i==2):
                    return 1/np.tan(th)
        else:
            if (i==1 and j==4):
                return Bt/(2*B)
        return 0
    
    def christ(self, pt):
        r, th, ph, t = pt.q
        B = -(1-self.rs/r)
        A = -1/B
        At = -self.rs/r**2 * A**2
        Bt = -self.rs/r**2
        crs = np.zeros([4,4,4])

        crs[0,0,0] = At/(2*A)
        crs[0,1,1] = -r/A
        crs[0,2,2] = -r*(np.sin(th)**2)/A
        crs[0,3,3] = -Bt/(2*A)

        crs[1,0,1], crs[1,1,0] = (1/r  ,)*2
        crs[1,2,2] = -np.sin(th)*np.cos(th)

        crs[2,0,2], crs[2,2,0] = (1/r  ,)*2
        crs[2,1,2], crs[2,2,1] = (1/np.tan(th)  ,)*2

        crs[3,0,3], crs[3,3,0] = (Bt/(2*B)  ,)*2
        
        return crs
    
    def gram(self, pt):
        r, th, ph, t = pt.q
        return np.diag([1./(1.-self.rs/r), r*r, r*r*np.sin(th)**2,
                        self.rs/r-1])
    
    def dif_scale(self, v, d=0.001):
        return v.scale(d/np.sqrt(np.inner(v.q, v.q)))
    
    def get_outward_dir(self, pt):
        g = self.gram(pt)
        return vector(pt, [1./np.sqrt(g[0,0]), 0, 0, 1./np.sqrt(-g[3,3])])
        