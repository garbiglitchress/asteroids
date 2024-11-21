from circleshape import *
class Shot(CircleShape):
    def __init__(self, x, y, radius, distance):
        super().__init__(x, y, radius)
        self.distance=distance
    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), self.position, self.radius, 2)#green
    def update(self, dt):
        self.position+=(self.velocity*dt)
        self.distance+=dt