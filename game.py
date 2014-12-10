#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  game.py
#  
#  Copyright 2014 Larry T. Priest <larrytpriest at gmail dot com>
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
'''this is my new starting ground started on  14-12-09 04:31:15 PM 
I am going to try to get the basics into classes and use calls to some of the
other programs I have setup, copied or outright stole.
'''

#imports
import pygame
from pygame.locals import *
import sys, os
import mods.Player as Player
import mods.weapon as weapon
import mods.Enemy as Enemy
import mods.GetObjects as GetObjects
import mods.tmx as tmx

# global variables
mapfile = 'map_2.tmx'
tile_width, tile_height = 32, 32
FGCOLOUR = 250, 240, 230
#BGCOLOUR = 5, 5, 5
BRIGHTBLUE = (  0, 170, 255)
WHITE      = (255, 255, 255)
BGCOLOR = BRIGHTBLUE
TEXTCOLOR = WHITE
screen_w = 800
screen_h = 600
start = True


#initial message
def StartMessage(screen):
    ''' Display the startup message'''  
    font = pygame.font.SysFont('purisa', 20)
    pos = 40
    message=Game().__doc__
    line= message.split('\n')
    for l in line:
        ren = font.render(l,1,FGCOLOUR) 
        screen.blit(ren,((( screen_w ) - ( ( len(l)/2) * 20 ) )/2, pos))
        pos += 20
    pygame.display.flip()
#    print(StartMessage.__doc__)
    while (pygame.event.wait().type != KEYDOWN): pass
    
def startScreen():
    """Display the start screen (which has the title and instructions)
    until the player presses a key. Returns None."""

    # Position the title image.
    titleRect = IMAGESDICT['title'].get_rect()
    topCoord = 50 # topCoord tracks where to position the top of the text
    titleRect.top = topCoord
    titleRect.centerx = HALF_WINWIDTH
    topCoord += titleRect.height

    # Unfortunately, Pygame's font & text system only shows one line at
    # a time, so we can't use strings with \n newline characters in them.
    # So we will use a list with each line in it.
    instructionText = ['Push the stars over the marks.',
          'Arrow keys to move, WASD for camera control, P to change character.',
                       'Backspace to reset level, Esc to quit.',
                       'N for next level, B to go back a level.']

    # Start with drawing a blank color to the entire window:
    DISPLAYSURF.fill(BGCOLOUR)

    # Draw the title image to the window:
    DISPLAYSURF.blit(IMAGESDICT['title'], titleRect)
    # Position and draw the text.
    for i in range(len(instructionText)):
        instSurf = BASICFONT.render(instructionText[i], 1, TEXTCOLOR)
        instRect = instSurf.get_rect()
        topCoord += 10 # 10 pixels will go in between each line of text.
        instRect.top = topCoord
        instRect.centerx = HALF_WINWIDTH
        topCoord += instRect.height # Adjust for the height of the line.
        DISPLAYSURF.blit(instSurf, instRect)

    while True: # Main loop for the start screen.
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    terminate()
                return # user has pressed a key, so return.

        # Display the DISPLAYSURF contents to the actual screen.
        pygame.display.update()
        FPSCLOCK.tick()
        
class Game(object):
    """Welcome to My Game!
movement-> arrows
shoot-> left shift
Quit -> Esc
Goal so far wander around and shoot dragons
and other bad guys
more to come like backpack and weapon selection."""
    def main(self, screen):
        start=True
        # font = pygame.font.Font(None, 14)

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
            Enemy.Enemy((enemy.px, enemy.py), self.enemies)
        # GetObjects.py
        self.thing_sprite = tmx.SpriteLayer()
        self.tilemap.layers.append(self.thing_sprite)
        a = GetObjects.Get_obj_list(mapfile, self.thing_sprite)
        # load sounds
        self.shoot = pygame.mixer.Sound('Sounds/shoot.wav')
        self.explosion = pygame.mixer.Sound('Sounds/explosion.wav')
        clock = pygame.time.Clock()

# main game loop
        while 1:
            dt = clock.tick(20)
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or ((event.type == KEYDOWN)
                 and (event.key == K_ESCAPE)):
                    print('Wimped out did you?')
                    terminate()
            self.player.update(dt/1000., self)
            self.tilemap.update(dt/1000., self)
            self.tilemap.draw(screen)
            if start == True:
                StartMessage(screen)
                start = False
                pygame.display.flip()
                # restart the clock so sprites don't jump
                clock = pygame.time.Clock()
            # display signage
            font = pygame.font.SysFont('purisa', 20)
            ren = font.render(self.player.message,1,FGCOLOUR)
            screen.blit(ren,(((screen_w/2)-(len(self.player.message)*20)/2),420))
            # display enemy left on level
            font = pygame.font.SysFont('unpilgi', 20)
            text = 'There are ' + str(self.num_enemy) + ' left'
            ren = font.render(text,1,FGCOLOUR)
            screen.blit(ren,(20,20))
            # Print player score
            font = pygame.font.SysFont('unpilgi', 20)
            text = str(self.player.name) + ' Your score is -> ' + str(self.player.score)
            ren = font.render(text,1,FGCOLOUR)
            screen.blit(ren,(20,40))

            if self.player.is_dead:
  
                print( str(self.player.name) + ', you poor thing, You died ' )
                print('Your score is '+ str(self.player.score))
                terminate()
            # regen enemies if you run out
            if self.num_enemy == 0:
#            if True:
                for enemy in self.tilemap.layers['triggers'].find('enemy'):
                    self.num_enemy += 1
                    Enemy.Enemy((enemy.px, enemy.py), self.enemies)
            pygame.display.flip()

def terminate():
    pygame.quit()
    sys.exit()
    
if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((screen_w,screen_h),pygame.RESIZABLE)
    pygame.display.set_caption('The Road to Quarks - An epic journey.')
    Game().main(screen)

