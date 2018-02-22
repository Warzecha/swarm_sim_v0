import pygame

class Circle:

    def __init__(self, _x, _y, _radius):

        self.pos = pygame.math.Vector2(_x, _y)
        self.radius = _radius
        self.x = _x
        self.y = _y


    def show(self, display):

        pygame.draw.circle(display, (255,0,0), (self.x, self.y), self.radius, 4)





