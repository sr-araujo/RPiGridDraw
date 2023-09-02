import pygame
from colors import *

class Button():
    def __init__(self,
                 text,
                 pos,
                 action = None,
                 size = (100, 30),
                 color = tuple(DARKBLUE),
                 hilight = tuple(DARKCYAN),
                 fontColor = tuple(WHITE)
                 ):
        self.normal = color
        self.hilight = hilight
        self.rect = pygame.Rect(pos, size)
        self.mouseover = False
        self.text = text
        self.font = pygame.font.Font(None, 18)
        self.text_image = self.font.render(text, 1, fontColor)
        w, h = self.font.size(text)  # size of font image
        self.text_pos = (pos[0] + size[0] / 2 - w / 2, pos[1] + size[1] / 2 - h / 2)  # center text
        self.buttondown = False
        self.action = action
        
    # Draws the button
    def draw(self, surface):
        rectout = self.rect.inflate(2, 2)
        rectin = self.rect.inflate(1, 1)
        if self.buttondown:
            pygame.draw.rect(surface, EMPTY, rectout)
            pygame.draw.rect(surface, WHITE, rectin)
        else:
            pygame.draw.rect(surface, WHITE, rectout)
            pygame.draw.rect(surface, EMPTY, rectin)
        if self.mouseover:
            pygame.draw.rect(surface, self.hilight, self.rect)
        else:
            pygame.draw.rect(surface, self.normal, self.rect)
        surface.blit(self.text_image, self.text_pos)

    # Runs the appropriate action when button is clicked
    def click(self):
        if self.action:
            self.action()