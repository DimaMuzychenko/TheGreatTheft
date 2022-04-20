import pygame
from pygame.sprite import Sprite
from typing import *



def is_mouse_over(sprite : Sprite) -> bool:
    return sprite.rect.collidepoint(pygame.mouse.get_pos())

def is_mouse_over(sprites : List[Sprite]) -> Sprite | None:
    x, y = pygame.mouse.get_pos()
    for sprite in sprites:
        if sprite.rect.collidepoint(x, y):
            return sprite
    return None