import pygame
from gridColors import *

class LED():
    def __init__(self, x, y, radius = 20, lit = False, color = EMPTY):
        self.x = x
        self.y = y
        self.lit = lit
        self.radius = radius
        self.screen = pygame.display.get_surface()
        self.color = color
        self.pos_x = int(self.x * (self.radius * 2 + 5)) + (self.radius)
        self.pos_y = int(self.y * (self.radius * 2 + 5)) + (self.radius) + 40
    
    # Draw LED
    def draw(self):
        (color, thickness) = (self.color, 0) if self.lit else (WHITE, 1)
        pygame.draw.circle(self.screen, color, (self.pos_x, self.pos_y), self.radius, thickness)
        pygame.draw.rect(self.screen, color,(self.pos_x-self.radius, self.pos_y-self.radius, (2*self.radius),(2*self.radius)),thickness)

    # Switch state of LED. LED ON = color, LED OFF = EMPTY/BLACK
    def clicked(self, _color = EMPTY):
        self.lit = not self.lit
        self.color = _color if self.lit else EMPTY
        return self.color