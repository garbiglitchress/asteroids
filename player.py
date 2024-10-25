import pygame
from circleshape import *
from constants import *
from shot import *
import math
class Player(CircleShape):
    def __init__(self,x,y,control):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation=0
        self.cooldown=0
        self.control=control
        self.invincible = False
        self.wraps=True
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    def draw(self, screen):
        #pygame.draw.polygon(screen, (255,255,255), self.triangle(), 2)
        if not self.invincible:
            pygame.draw.polygon(screen, PLAYER_COLOR, self.triangle(), 2)
        else:
            pygame.draw.polygon(screen, PLAYER_COLOR_HIT, self.triangle(), 2)
    def rotate(self, dt):
        self.rotation+=(PLAYER_TURN_SPEED*dt)
    def update(self, dt):
        self.cooldown-=dt
        if self.control=='K':
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                self.rotate(-dt)
            if keys[pygame.K_d]:
                self.rotate(dt)
            if keys[pygame.K_s]:
                self.move(-dt)
            if keys[pygame.K_w]:
                self.move(dt)
            if keys[pygame.K_SPACE]:
                self.shoot()
        elif self.control=='M':#keyboard/mouse for now, ideally the ship would move toward the mouse when you're rightclicking, and would always be pointing toward the mouse, probably using a vector?
            keys = pygame.key.get_pressed()

            if keys[pygame.K_a]:
                self.rotate(-dt)
            if keys[pygame.K_d]:
                self.rotate(dt)
            if keys[pygame.K_s]:
                self.move(-dt)
            if keys[pygame.K_w]:
                self.move(dt)
            if keys[pygame.K_SPACE]:
                self.shoot()
            mouse_pressed=pygame.mouse.get_pressed()[0]
            mouse_move=pygame.mouse.get_pressed()[2]
            mouse_pos=pygame.mouse.get_pos()
            angle=math.atan2((self.position.y-mouse_pos[1]), (self.position.x-mouse_pos[0]))
            self.rotation=math.degrees(angle)+90
            if mouse_pressed==True:
                self.shoot()
            if mouse_move==True:
                self.move(dt)
    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position=(self.position+(forward*PLAYER_SPEED*dt))
        if self.position.x>SCREEN_WIDTH:
            self.position.x%=SCREEN_WIDTH
        if self.position.x<0:
            self.position.x+=SCREEN_WIDTH
        if self.position.y>SCREEN_HEIGHT:
            self.position.y%=SCREEN_HEIGHT
        if self.position.y<0:
            self.position.y+=SCREEN_HEIGHT
    def shoot(self):
        if self.cooldown<=0:
            s=Shot(self.position.x, self.position.y, SHOT_RADIUS)
            s.velocity=pygame.Vector2(0,1).rotate(self.rotation)
            s.velocity*=PLAYER_SHOOT_SPEED
            self.cooldown=PLAYER_SHOOT_COOLDOWN
        else:
            pass
        

        
