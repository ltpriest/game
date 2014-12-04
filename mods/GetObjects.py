#! /usr/bin/env python2
from pprint import pprint
from xml.etree import ElementTree as ET
import pygame, sys, os
from pygame.locals import *
fg = 250, 240, 230
bg = 5, 5, 5
''' This class will read the map file and create sprites for the
objects in the layer Hopefully the sprites are global and I can just add them I
will try the trick of calling self. calling from tmx or pygame_5'''
class Things(pygame.sprite.Sprite):
    """Things going wrong"""
    def __init__(self, x, y, props, *groups):
        super(Things, self).__init__(*groups)
        self.x = x
        self.y = y
        self.show = False
        self.image = pygame.image.load('images/Shroom.png')
        for n in props:
             if n[0][1] =='image':
                self.image = pygame.image.load(n[1][1])
             elif n[0][1] == 'message':
                self.message = n[1][1]
                self.show = True
        self.rect = pygame.rect.Rect((x, y), self.image.get_size())

    def update(self, dt, game):
        pass
        '''#check for thing collision
        if self.rect.colliderect(game.player.rect):
            font = pygame.font.Font(None,14)
            size =font.size(self.message)
            ren = font.render(self.message,1,fg)
            screen.blit(ren,(self.x,self.y))
            '''

def Get_obj_list(map_file, thing_sprite):
    tree = ET.parse(map_file)
    object_group = tree.find('objectgroup')
    for obj in object_group:
        if obj.tag == "object":
            x=[]
            if obj.keys():
                for name,value in obj.items():
                    if name == 'name':
                        for ind, val in obj.items():
                            if ind == 'name':
                                obj_name = val
                            elif ind == 'y':
                                obj_y = int(val)
                            elif ind == 'x':
                                obj_x = int(val)
                        Obj_props = obj.find('properties')
                        for prop in Obj_props:
                            x.append( prop.items())
                            
                        thingy = Things(obj_x, obj_y, x, thing_sprite)

if __name__ == '__main__':
    fg = 250, 240, 230
    bg = 5, 5, 5
    wc = 40, 40, 40
    map_file = 'test_map4.tmx'
    pygame.init()
    screen = pygame.display.set_mode((640,480))
    screen.fill(wc)
    thing_sprite = pygame.sprite.Group()
    a = Get_obj_list(map_file, thing_sprite)
    thing_sprite.draw(screen)
#    from examples/fonty.py
    font_80 = pygame.font.Font(None, 80)
    text = 'test message'
    font_20 = pygame.font.Font(None, 20)
    size = font_80.size(text)
    ## no AA , no trans,normal
    ren_nt = font_80.render(text,0, fg,bg)
    screen.blit(ren_nt, (10,10))
    # AA and trans
    ren_t = font_80.render(text,1, fg)
    screen.blit(ren_t, (10,55))
    
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                for sign in thing_sprite:
                    if sign.show:
                        screen.blit(ren_nt, (10,10))
                        screen.blit(ren_t, (10,55))
                        font = pygame.font.Font(None, 14)
                        ren = font.render(sign.message,1,fg)
                        screen.blit(ren,(sign.x,sign.y))
                        pygame.display.flip()
                        sign.show = False

                    else:
                        screen.fill(wc)
                        screen.blit(ren_nt, (10,10))
                        screen.blit(ren_t, (10,55))
                        font = pygame.font.Font(None, 14)
                        ren = font.render(sign.message,1,fg)
                        thing_sprite.draw(screen)
                        sign.show = True
        pygame.display.flip()
