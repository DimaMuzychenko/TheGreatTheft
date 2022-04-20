import pygame
from typing import *


class Pawn(pygame.sprite.Sprite):
    def __init__(self, radius : int, color : pygame.color.Color) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.color = color
        sur = pygame.Surface((radius*2, radius*2))
        pygame.draw.circle(sur, color, (radius, radius), radius)
        self.image = sur
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect(center=(radius, radius))
    
    
    def draw(self, surf : pygame.Surface):
        surf.blit(self.image, self.rect)

    
    def set_pos(self, pos : Tuple[int, int]):
        self.rect.center = pos

    
    def get_pos(self) -> Tuple[int, int]:
        return self.rect.center
    
    
    def set_radius(self, radius : int):
        sur = pygame.Surface((radius*2, radius*2))
        pygame.draw.circle(sur, self.color, (radius/2, radius/2), radius)
        self.image = sur
        self.image.set_colorkey((0, 0, 0))
        self.rect.w = radius
        self.rect.h = radius
    
    
    def get_radius(self) -> int:
        return self.rect.w


