import pygame
from .Pawn import Pawn
from typing import *
from .config import *
from pygame import Surface


class Field(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load(os.path.join(PATH_TO_RES, "field2.bmp")).convert()
        self.image = pygame.transform.smoothscale(img, (HEIGHT, HEIGHT))
        self.rect = self.image.get_rect()
        self.pawns : List[Pawn] = Field.create_pawns()
        self.cells = Field._create_cells()

    
    def cell_index(coords : Tuple[int, int]) -> Tuple[int, int]:
        x = int(coords[0] / CELL_SIZE)
        y = int(coords[1] / CELL_SIZE)
        return (x, y)
    
    
    def cell_coord(indexes : Tuple[int, int]) -> Tuple[int, int]:
        x = int(indexes[0] * CELL_SIZE) + CELL_SIZE / 2
        y = int(indexes[1] * CELL_SIZE) + CELL_SIZE / 2
        return (x, y)
    
    
    def draw(self, surf : Surface):
        surf.blit(self.image, self.rect)
    
    
    def create_pawns() -> List[Pawn]:
        pawns = []
        pawns.append(Pawn(HEIGHT/60, BLACK))
        pawns.append(Pawn(HEIGHT/60, RED))
        pawns.append(Pawn(HEIGHT/60, GREEN))
        pawns.append(Pawn(HEIGHT/60, BLUE))
        pawns.append(Pawn(HEIGHT/60, DARK_BLUE))
        pawns.append(Pawn(HEIGHT/60, YELLOW))
        return pawns
    
    
    def Set_pawn_pos(self, pawn_id : int, coords : Tuple[int, int]) -> None:
        self.pawns[pawn_id].set_pos(coords)
        
        
    def Set_pawn_cell(self, pawn_id : int, indexes : Tuple[int, int]) -> None:
        self.pawns[pawn_id].set_pos(self.cell_coord(indexes))
        
    
    def Get_pawn_pos(self, pawn_id : int, coords : Tuple[int, int]) -> Tuple[int, int]:
        return self.pawns[pawn_id].get_pos()
        
        
    def Get_pawn_cell(self, pawn_id : int, indexes : Tuple[int, int]) -> Tuple[int, int]:
        return self.cell_index(self.pawns[pawn_id].get_pos())
    
    
    def _create_cells() -> List[List[int]]:
        cells = [
            [ 10, 1, 1, 1, 1, 1, 1, 10, 0, 2, 2, 2, 2, 2, 10, 0, 10, 3, 3, 3, 3, 3, 3 ],
            [ 10, 1, 1, 1, 1, 1, 1, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 3, 0, 3, 3, 3, 3 ],
            [ 10, 1, 1, 1, 1, 1, 1, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 3, 3, 3, 3, 3 ],
            [ 10, 1, 1, 1, 1, 1, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 3, 3, 3, 3, 3, 3 ],
            [ 10, 1, 1, 1, 1, 1, 1, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 3, 3, 3, 3, 3, 3 ],
            [ 10, 10, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 3, 3, 3, 3, 3, 3 ],
            [ 10, 9, 9, 9, 9, 9, 9, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10 ],
            [ 10, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0 ],
            [ 10, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 10 ],
            [ 10, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 4, 10 ],
            [ 0, 0, 0, 0, 0, 0, 0, 0, 0, 10, 10, 10, 10, 10, 10, 0, 0, 4, 4, 4, 4, 4, 10 ],
            [ 10, 8, 8, 8, 8, 8, 8, 0, 0, 10, 10, 10, 10, 10, 10, 0, 0, 0, 4, 4, 4, 4, 10 ],
            [ 10, 8, 8, 8, 8, 8, 8, 0, 0, 10, 10, 10, 10, 10, 10, 0, 0, 4, 4, 4, 4, 4, 10 ],
            [ 10, 8, 8, 8, 8, 8, 0, 0, 0, 10, 10, 10, 10, 10, 10, 0, 0, 4, 4, 4, 4, 4, 10 ],
            [ 10, 8, 8, 8, 8, 8, 8, 0, 0, 10, 10, 10, 10, 10, 10, 0, 0, 4, 4, 4, 4, 4, 10 ],
            [ 10, 8, 8, 8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 10 ],
            [ 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 0, 5, 10 ],
            [ 10, 7, 7, 7, 7, 7, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 0, 5, 5, 5, 5, 5, 10 ],
            [ 10, 7, 7, 7, 7, 7, 0, 0, 6, 6, 6, 6, 6, 6, 0, 6, 0, 5, 5, 5, 5, 5, 10 ],
            [ 10, 7, 7, 7, 7, 0, 0, 0, 0, 6, 0, 0, 6, 6, 6, 0, 0, 5, 5, 5, 5, 5, 10 ],
            [ 10, 7, 7, 7, 7, 7, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 0, 5, 5, 5, 5, 5, 10 ],
            [ 10, 7, 7, 7, 7, 7, 0, 0, 6, 6, 6, 6, 6, 6, 6, 6, 0, 0, 5, 5, 5, 5, 10 ],
            [ 10, 7, 7, 7, 7, 7, 10, 0, 6, 6, 6, 6, 6, 6, 6, 6, 0, 10, 5, 5, 5, 5, 10 ]
        ]
        return cells

        