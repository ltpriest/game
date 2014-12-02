import pygame
import os, sys
import spritesheet
from sprite_strip_anim import SpriteStripAnim

class Bullet(pygame.sprite.Sprite):
    image = pygame.image.load('images/bullet.png')
    def __init__(self, location, direction, *groups):
        super(Bullet, self).__init__(*groups)
        self.rect = pygame.rect.Rect(location, self.image.get_size())
        # movement in the X direction; postive is right, negative is left;
        # inherited from the player (shooter)
        self.direction = direction
        self.count_down = 0

        # time this bullet will live for in seconds
        self.lifespan = 2
        self.boom =  SpriteStripAnim('images/effects/Explode1.png', (0,0,24,24), 8, 1, True, 4)
        self.boom.iter()

    def update(self, dt, game):
        # decrement the lifespan of the bullet by the amount of time passed and
        # remove it from the game if its time runs out
        self.lifespan -= dt
        if self.lifespan < 0 or self.count_down == 8:
            self.kill()
            return
        if self.count_down  > 0:
            self.image = self.boom.next()
            self.count_down +=1

        # move the Bullet by 400 pixels per second in the movement direction
        if self.direction == 'w':
            self.rect.x += -1 * 400 * dt
        elif self.direction == 'e':
            self.rect.x += 1 * 400 * dt
        elif self.direction == 'n':
            self.rect.y += -1 * 400 * dt
        elif self.direction == 's':
            self.rect.y += 1 * 400 * dt

        # check for collision with any of the enemy sprites; we pass the "kill
        # if collided" flag as True so any collided enemies are removed from the
        # game
        if pygame.sprite.spritecollide(self, game.enemies, True):
            game.explosion.play()
            game.player.score += 10
            self.image = self.boom.next()
            game.num_enemy -=1
            # we also remove the bullet from the game or it will continue on
            # until its lifespan expires
            # self.kill()
            self.count_down += 1
            self.direction = 'd'
