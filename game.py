# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 15:59:29 2016

@author: J
"""

import dynamics
import numpy as np
import pygame

class Game:
    def __init__(me):
        me.S = dynamics.schwarzschild(1., 1.)
        k = 3
        v = 1/(2*k)**0.5

        r = k*me.S.rs

        x0 = me.S.get_point_by_coords([r, np.pi/2, 0, 0])
        dirc = x0.get_vector([0, 0, v/r, 1.])
        
        me.spaceship = dynamics.body(dirc)
        
    def advance(me, time):
        me.spaceship.advance(time,'coord')
    def ss_coords(me):
        phi = me.spaceship.P.pt.q[2]
        r = me.spaceship.P.pt.q[0]
        print me.spaceship.P.pt.q
        return r*np.array([np.cos(phi),np.sin(phi)])

class GameDrawer:
    s_rad = 20
    def __init__(me, upper, game):
        me.game = game
        me.upper = upper
        
    def convert(me,game_p):
        cent = np.array([me.upper.sw/2,me.upper.sh/2])
        return tuple(int(i) for i in cent + me.s_rad / me.game.S.rs * game_p)
    def main(me):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                me.upper.end()
                return
                                
        me.game.advance(1.0/me.upper.fps_lim)
        
        me.upper.scr.fill((150,150,150))
        pygame.draw.circle(me.upper.scr, (0,0,0), me.convert(np.zeros(2)), me.s_rad)
        
        p = me.game.ss_coords()
                
        pygame.draw.circle(me.upper.scr, (255,255,255), me.convert(p), 0)
        
        

class Main:
    fps_lim = 60
    sw,sh = 640,480
    def __init__(me):
        pygame.init()
        me.scr = pygame.display.set_mode((me.sw,me.sh))
        me.state = None
        
        me.init_game()
        
        me.clock = pygame.time.Clock()
        
        me.cont = True
        
        while me.cont:
            me.clock.tick(me.fps_lim)
            me.state.main()
            pygame.display.flip()
        pygame.quit()
            
    def end(me):
        me.cont = False
        
    def init_game(me):
        me.state = GameDrawer(me, Game())
        
if __name__ == "__main__":
    Main()