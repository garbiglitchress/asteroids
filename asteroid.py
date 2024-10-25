from circleshape import *
from constants import *
import random

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.wraps=False
    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), self.position, self.radius, 2)
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
    def split(self):
        self.kill()
        if self.radius<ASTEROID_MIN_RADIUS:
            return
        else:
            angle=random.uniform(20, 50)
            new_vector_one=self.velocity.rotate(angle)
            new_vector_two=self.velocity.rotate(-angle)
            new_radius=self.radius-ASTEROID_MIN_RADIUS
            new_asteroid_one=Asteroid(self.position.x, self.position.y, new_radius)
            new_asteroid_two=Asteroid(self.position.x, self.position.y, new_radius)
            new_asteroid_one.velocity=new_vector_one*1.2
            new_asteroid_two.velocity=new_vector_two*1.2
            pass