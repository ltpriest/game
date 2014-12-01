#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  game.py
#  
#  Copyright 2014 Larry T. Priest <larrytpriest@gmail.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
'''this is my new starting ground started on 13-02-15 03:57:38 PM 
I am going to try to get the basics into classes and use calls to some of the
other programs I have setup, copied or outright stole.
'''

#startup stuff like imports
import pygame
from pygame.locals import *

import sys, os
#import Player, weapon, Enemy, GetObjects, tmx

import mods.Player as Player
import mods.weapon as weapon
import mods.Enemy as Enemy
import mods.GetObjects as GetObjects
import mods.tmx as tmx


mapfile = 'map_2.tmx'
tile_width, tile_height = 32, 32
fg = 250, 240, 230
bg = 5, 5, 5

class Game(object):
    def main(self, screen):
        font = pygame.font.Font(None, 14)
        clock = pygame.time.Clock()
       #self.screen=screen
# load the map
        self.tilemap = tmx.load(mapfile, screen.get_size())
# set up sprite layer for ???        
        self.sprites = tmx.SpriteLayer()
        self.tilemap.layers.append(self.sprites)
        
# locate the player and start the game there        
        start_cell = self.tilemap.layers['triggers'].find('player')[0]
        self.player = Player.Player((start_cell.px,start_cell.py), self.sprites)

# create enemies
        self.enemies = tmx.SpriteLayer()
        self.tilemap.layers.append(self.enemies)
        self.num_enemy = 0
        for enemy in self.tilemap.layers['triggers'].find('enemy'):
            self.num_enemy += 1
            print 'so far enemies = ', self.num_enemy
            Enemy.Enemy((enemy.px, enemy.py), self.enemies)

# GetObjects.py
        self.thing_sprite = tmx.SpriteLayer()
        self.tilemap.layers.append(self.thing_sprite)
        a = GetObjects.Get_obj_list(mapfile, self.thing_sprite)

# load sounds
        self.shoot = pygame.mixer.Sound('Sounds/shoot.wav')
        self.explosion = pygame.mixer.Sound('Sounds/explosion.wav')

# main game loop            
        while 1:
            dt = clock.tick(20)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.player.update(dt/1000., self)
            self.tilemap.update(dt/1000., self)
            self.tilemap.draw(screen)
            
            # display signage
            font = pygame.font.SysFont('purisa', 30)
            ren = font.render(self.player.message,1,fg)
            screen.blit(ren,(40,40))
            
            font = pygame.font.SysFont('unpilgi', 20)
            text = 'There are ' + str(self.num_enemy) + ' left'
            ren = font.render(text,1,fg)
            # player score display
            text2 = "Your score:> " + str(Player.Player.score)
            ren2 = font.render(text2,1,fg)
            screen.blit(ren2, (50,20))
            screen.blit(ren,(20,20))
            
            pygame.display.flip()
            
            # add player dead test
            if self.player.is_dead:
                pygame.quit()
                print 'You died'
                sys.exit()

            if self.num_enemy == 0:
                for enemy in self.tilemap.layers['triggers'].find('enemy'):
                    self.num_enemy += 1
                    print 'so far enemies = ', self.num_enemy
                    Enemy.Enemy((enemy.px, enemy.py), self.enemies)

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    Game().main(screen)

