from circleshape import *
from constants import *
import random

class Powerup(CircleShape):#makes your ship do double damage/give double pts for 10 seconds
    def __init__(self,x,y,radius):
        super().__init__(x,y,radius)
    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 255), self.position, self.radius, 2)
    def update(self, dt):
        self.position+=(self.velocity*dt)
        if self.position.x>SCREEN_WIDTH:
            self.position.x%=SCREEN_WIDTH
        if self.position.x<0:
            self.position.x+=SCREEN_WIDTH
        if self.position.y>SCREEN_HEIGHT:
            self.position.y%=SCREEN_HEIGHT
        if self.position.y<0:
            self.position.y+=SCREEN_HEIGHT
    
