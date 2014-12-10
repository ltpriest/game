import pygame, os, sys, tmx
from pygame.locals import *
import spritesheet
from sprite_strip_anim import SpriteStripAnim
h = 64 # x value
w = 64 # y value
# Old file char_file = 'images/character/ch003.png'
char_file = 'images/character/bahamut.png'
#
# Our enemies are quite dumb, just moving from side to side between "reverse"
# map triggers. It's game over if they hit the player.
#
class Enemy(pygame.sprite.Sprite):
    #image = pygame.image.load('enemy.png')
    def __init__(self, location, *groups):
        super(Enemy, self).__init__(*groups)
        FPS = 120
        frames = FPS / 24

        self.strips = [
            SpriteStripAnim(char_file, (0,h*0,h,w), 4, -1, True, frames),
            SpriteStripAnim(char_file, (0,h*1,h,w), 4, -1, True, frames),
            SpriteStripAnim(char_file, (0,h*2,h,w), 4, -1, True, frames), 
            SpriteStripAnim(char_file, (0,h*3,h,w), 4, -1, True, frames)
        ]
        self.strips[2].iter()
        self.image = self.strips[2].next()
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        # movement in the X direction; postive is right, negative is left
        self.direction = 1

    def update(self, dt, game):
        # move the enemy by 100 pixels per second in the movement direction
        self.rect.x += self.direction * 100 * dt
        # check all reverse triggers in the map to see whether this enemy has
        # touched one
        for cell in game.tilemap.layers['triggers'].collide(self.rect, 'reverse'):
            # reverse movement direction; make sure to move the enemy out of the
            # collision so it doesn't collide again immediately next update
            if self.direction > 0:
                self.rect.right = cell.left
                self.image = self.strips[1].next()
                
            else:
                self.rect.left = cell.right
                self.image = self.strips[2].next()
            self.direction *= -1
            break

        # check for collision with the player; on collision mark the flag on the
        # player to indicate game over (a health level could be decremented here
        # instead)
        if self.rect.colliderect(game.player.rect):
            game.player.is_dead = True

