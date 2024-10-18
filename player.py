import pygame
from circleshape import *
from constants import *
from shot import *

class Player(CircleShape):
    def __init__(self,x,y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation=0
        self.cooldown=0
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    def draw(self, screen):
        pygame.draw.polygon(screen, (255,255,255), self.triangle(), 2)
    def rotate(self, dt):
        self.rotation+=(PLAYER_TURN_SPEED*dt)
    def update(self, dt):
        self.cooldown-=dt
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
        

        