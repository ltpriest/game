import sys, os
import pygame, tmx, weapon
from pygame.locals import *
import spritesheet
from sprite_strip_anim import SpriteStripAnim
h = 64 # x value
w = 64 # y value
char_file = 'images/character/bahamut.png'
fg = 250, 240, 230
bg = 5, 5, 5

class Player(pygame.sprite.Sprite):
    def __init__(self, location, *groups):
        super(Player, self).__init__(*groups)
        #surface = pygame.display.set_mode((200,200))
        FPS = 120
        frames = FPS / 24
        self.strips = [
            SpriteStripAnim(char_file, (0,h*0,h,w), 4, -1, True, frames),
            SpriteStripAnim(char_file, (0,h*1,h,w), 4, -1, True, frames),
            SpriteStripAnim(char_file, (0,h*2,h,w), 4, -1, True, frames), 
            SpriteStripAnim(char_file, (0,h*3,h,w), 4, -1, True, frames)
        ]

        
        self.strips[0].iter()
        self.image = self.strips[0].next()
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        
        self.message = ' '
        # is the player dead?
        self.is_dead = False

        # movement in the X direction; postive is right, negative is left
        self.direction = 'w'
        # time since the player last shot
        self.gun_cooldown = 0

    def update(self, dt, game):
        # take a copy of the current position of the player before movement for
        # use in movement collision response
        last = self.rect.copy()

        # handle the player movement left/right keys
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()
        elif key[pygame.K_LEFT]:
            self.rect.x -= 100 * dt
            #self.image = self.left_image
            
            self.image = self.strips[1].next()
            self.direction = 'w'
        elif key[pygame.K_RIGHT]:
            self.rect.x += 100 * dt
            #self.image = self.right_image
            
            self.image = self.strips[2].next()
            self.direction = 'e'
        elif key[pygame.K_UP]:
            self.rect.y -= 100 * dt
            
            self.image = self.strips[3].next()
            self.direction = 'n'
        elif key[pygame.K_DOWN]:
            self.direction = 's'
            self.rect.y += 100 * dt
            
            self.image = self.strips[0].next()

        # handle the player shooting key
        elif key[pygame.K_LSHIFT] and not self.gun_cooldown:
            game.shoot.play()
 
            # create a bullet at an appropriate position (the side of the player
            # sprite) and travelling in the correct direction
            if self.direction == 'e':
                weapon.Bullet(self.rect.midright, 'e', game.sprites)
            elif self.direction == 'w':
                weapon.Bullet(self.rect.midleft, 'w', game.sprites)
            elif self.direction == 'n':
                weapon.Bullet(self.rect.midtop, 'n', game.sprites)
            else:
                weapon.Bullet(self.rect.midbottom, 's', game.sprites)
                
            # set the amount of time until the player can shoot again
            self.gun_cooldown = 1
        # decrement the time since the player last shot to a minimum of 0 (so
        # boolean checks work)
        self.gun_cooldown = max(0, self.gun_cooldown - dt)

        # collide the player with the map's blockers
        new = self.rect

        # look up the tilemap triggers layer for all cells marked "blockers"
        for cell in game.tilemap.layers['triggers'].collide(new, 'blockers'):
            # find the actual value of the blockers property
            blockers = cell['blockers']
            # now for each side set in the blocker check for collision; only
            # collide if we transition through the blocker side (to avoid
            # false-positives) and align the player with the side collided to
            # make things neater
            if 'l' in blockers and last.right <= cell.left and new.right > cell.left:
                new.right = cell.left
            if 'r' in blockers and last.left >= cell.right and new.left < cell.right:
                new.left = cell.right
            if 't' in blockers and last.bottom <= cell.top and new.bottom > cell.top:
                self.resting = True
                new.bottom = cell.top
            if 'b' in blockers and last.top >= cell.bottom and new.top < cell.bottom:
                new.top = cell.bottom

        self.message = ' '
        for sign in game.thing_sprite:
            #print sign.show
            if self.rect.colliderect(sign.rect):
                sign.show = True
                self.message = sign.message
            else:
                sign.show = False

        game.tilemap.set_focus(new.x, new.y)
 
