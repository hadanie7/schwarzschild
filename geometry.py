# -*- coding: utf-8 -*-
"""
Created on Tue Dec 13 21:59:57 2016

@author: D
"""

import numpy as np

class point:
    def __init__(self, man, q):
        self.man = man
        self.q = np.array(q)
    
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
    
    def normalize(self):
        return 1./(np.sqrt(np.abs(self.sq()))) * self
    
class lin_map:
    def __init__(self, pt1, pt2, q):
        self.pt1 = pt1
        self.pt2 = pt2
        self.q = np.array(q)
        assert self.q.shape == (pt2.man.dim,pt1.man.dim)
    
    def __call__(self, v):
        assert isinstance(v, vector)
        assert v.pt is self.pt1
        return vector(self.pt2, np.dot(self.q, v.q))
    
    def __mul__(self, m2):
        assert isinstance(m2, lin_map)
        assert self.pt1 is m2.pt2
        return lin_map(m2.pt1, self.pt2, np.dot(self.q, m2.q))
    
def gram_schmidt(vs):
    us = []
    for v in vs:
        for u in us:
            v = v.ortho_part(u)
        v = v.normalize()
        us.append(v)
    return us

class manifold:
    def __init__(self, dim):
        self.dim = dim
    
    def get_point_by_coords(self, q):
        return point(self, q)
    
    def get_coords(self, obj):
        assert isinstance(obj, vector) or isinstance(obj, point)
        return obj.q
    
    def get_vec_by_coords(self, pt, q):
        return pt.get_vector(q)
    
    def christ(self, pt):
        NotImplemented #virtual
    
    def gram(self, pt):
        NotImplemented #virtual
    
    def dif_scale(self, v, d):
        NotImplemented #virtual

    """ parallel transport of the vector v by a short increment dt """
    def parallel_transport(self, v, dt):
        return self.get_parallel_transport(dt)(v)    

    """ parallel transport of the vector v by a short increment dt """
    """def parallel_transport2(self, v, dt):
        assert isinstance(v, vector); assert isinstance(dt, vector)
        assert v.pt is dt.pt
        D = np.zeros(self.dim)
        
        for k in range(self.dim):
            for i in range(self.dim):
                for j in range(self.dim):
                    D[k] -= self.christ2(v.pt, i, j, k) * dt.q[i] * v.q[j]
        npt = point(self, v.pt.q + dt.q)
        
        return vector(npt, v.q+D)"""
        
    """ parallel transport of the vector v by a short increment dt """
    """def parallel_transport3(self, v, dt):
        tmp = self.get_parallel_transport(dt)(v)
        print type(tmp), tmp
        return tmp
        assert isinstance(v, vector); assert isinstance(dt, vector)
        assert v.pt is dt.pt
        D = -np.tensordot(self.christ(v.pt), np.outer(v.q, dt.q))
        npt = point(self, v.pt.q + dt.q)
        
        return vector(npt, v.q+D)"""
    
    def get_parallel_transport(self, dt):
        assert isinstance(dt, vector)
        D = -np.tensordot(self.christ(dt.pt), dt.q, (1, 0))
        tq = np.eye(self.dim) + D
        npt = point(self, dt.pt.q + np.dot(tq, dt.q))

        return lin_map(dt.pt, npt, tq)
    
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
    
    def dif_scale(self, v, d=0.05):
        dist = v.pt.q[0]/self.rs
        d *= dist
        return v.scale(d/np.sqrt(np.inner(v.q, v.q)))
    
    def get_outward_dir(self, pt):
        g = self.gram(pt)
        return vector(pt, [1./np.sqrt(g[0,0]), 0, 0, 1./np.sqrt(-g[3,3])])
    
    def get_inward_dir(self, pt):
        g = self.gram(pt)
        return vector(pt, [-1./np.sqrt(g[0,0]), 0, 0, 1./np.sqrt(-g[3,3])])
        