# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 15:59:29 2016

@author: Jonatan Hadas
"""

import dynamics
import numpy as np
import pygame

class Game:
    fuel_mass = 0.001
    fuel_energy = 0.001
    fuel_limit = 300
    
    fuel_timeout = 0
    
    turn_speed = np.pi * 0.04
    def __init__(me):
        me.S = dynamics.schwarzschild(1., 1.)
        k = 3
        v = 1/(2*k)**0.5

        r = k*me.S.rs

        x0 = me.S.get_point_by_coords([r, np.pi/2, 0, 0])
        dirc = x0.get_vector([0, 0, v/r, 1.])
        
        me.spaceship = dynamics.body(dirc)
        
        me.fuel_left = me.fuel_limit
        
        me.fuel_parts = {}
    
    def engine(me):
        if me.fuel_left > 0:
            print me.fuel_left
            me.fuel_left -= 1
            me.fuel_parts[me.spaceship.shoot2(me.S.get_outward_dir(me.spaceship.P.pt),
                                             me.fuel_mass,
                                             me.fuel_energy)] = me.fuel_timeout
    def turn(me, side):
        pass
    def advance(me, time):
        me.spaceship.advance(time,'self')
        fr = set()
        for p in me.fuel_parts:
            if me.fuel_parts[p] == 0:
                fr.add(p)
            else:
                me.fuel_parts[p] -= 1
                p.advance(me.spaceship.P.pt.q[3] - p.P.pt.q[3]
                          ,'coord')
        for p in fr:
            me.fuel_parts.pop(p)
    def ss_coords(me):
        phi = me.spaceship.P.pt.q[2]
        r = me.spaceship.P.pt.q[0]
        return r*np.array([np.cos(phi),np.sin(phi)])
    def f_part_coords(me):
        phis = np.array([p.P.pt.q[2] for p in me.fuel_parts])
        rs = np.array([p.P.pt.q[0] for p in me.fuel_parts])
        return list((rs*np.array([np.cos(phis), np.sin(phis)])).T)

class GameDrawer:
    s_rad = 20
    time_mult = 3
    step_num = 1
    def __init__(me, upper, game):
        me.game = game
        me.upper = upper
        
        me.up_p, me.rt_p, me.lt_p = (False,)*3
        
    def convert(me,game_p):
        cent = np.array([me.upper.sw/2,me.upper.sh/2])
        return tuple(int(i) for i in cent + me.s_rad / me.game.S.rs * game_p)
    def main(me):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                me.upper.end()
                return
            elif e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    me.up_p = True
                elif e.key == pygame.K_RIGHT:
                    me.rt_p = True
                elif e.key == pygame.K_LEFT:
                    me.lt_p = True
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_UP:
                    me.up_p = False
                elif e.key == pygame.K_RIGHT:
                    me.rt_p = False
                elif e.key == pygame.K_LEFT:
                    me.lt_p = False
        if not pygame.display.get_active():
            me.up_p, me.rt_p, me.lt_p = (False,)*3
            return
            
                                
        if me.up_p:
            me.game.engine()
        for i in xrange(me.step_num):
            me.game.advance(1.0/me.upper.fps_lim*me.time_mult/me.step_num)
            if me.rt_p:
                me.game.turn(1.0/me.step_num)
            if me.lt_p:
                me.game.turn(-1.0/me.step_num)
        
        me.upper.scr.fill((150,150,150))
        pygame.draw.circle(me.upper.scr, (0,0,0), me.convert(np.zeros(2)), me.s_rad)
        
        p = me.game.ss_coords()
                
        pygame.draw.circle(me.upper.scr, (255,255,255), me.convert(p), 2)
        
        for p in me.game.f_part_coords():
            pygame.draw.circle(me.upper.scr, (255,0,0), me.convert(p), 0)
            
        
        

class Main:
    fps_lim = 60
    sw,sh = 640,480
    def __init__(me):
        pygame.init()
        me.scr = pygame.display.set_mode((me.sw,me.sh)) #fullscreen : (max(pygame.display.list_modes()), pygame.FULLSCREEN)
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
    try:
        Main()
    except:
        pygame.quit()
        raise
