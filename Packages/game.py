import socket
from pygame import Surface
from typing import *
import pygame
import os

from Packages.network import *
from .mouse_handlers import *
from .config import *

from .Pawn import Pawn
from .Field import Field

window : Surface
game_field : Field
server_connection : socket.socket

t_cards = None
c_cards = None
l_cards = None
field = None
notes = None

clock = None
display_info = None

pawns : List[Pawn] = []

MOVING_PAWN : Pawn = None


def init():
    global clock
    global display_info
    
    pygame.init()
    clock = pygame.time.Clock()
    display_info = pygame.display.Info()


def load_images():
    global t_cards
    global c_cards 
    global l_cards
    global notes

    t_cards = []
    c_cards = []
    l_cards = []

    
    root = os.getcwd()

    for root, dirs, files in os.walk(PATH_TO_CARDS):
        for file in files:
            if file.startswith('t'):
                t_cards.append(pygame.image.load(os.path.join(PATH_TO_CARDS, file)).convert())
            elif file.startswith('c'):
                c_cards.append(pygame.image.load(os.path.join(PATH_TO_CARDS, file)).convert())
            else:
                l_cards.append(pygame.image.load(os.path.join(PATH_TO_CARDS, file)).convert())
    
    notes = pygame.image.load(os.path.join(PATH_TO_RES, 'notes.bmp'))


def draw_cards():
    pass

def draw_pawns():
    for pawn in game_field.pawns:
        pawn.draw(window)

def draw():
    window.fill(BLACK)
    game_field.draw(window)
    draw_cards()
    draw_pawns()
    pygame.display.update()


def send_msg(msg : Msg, connection : socket.socket):
    data = pickle.dumps(msg, protocol=5)
    connection.sendto(data, SERVER_ADDRESS)


def handle_mouse():
    global MOVING_PAWN, game_field, server_connection
    pawns = game_field.pawns
    
    l, m, r = pygame.mouse.get_pressed()
    rx, ry = pygame.mouse.get_rel()
    if MOVING_PAWN:
        if l:
            MOVING_PAWN.rect.move_ip(rx, ry)
        else:
            #MOVING_PAWN.rect.center = Field.cell_coord(Field.cell_index(MOVING_PAWN.rect.center))
            pawn_id = game_field.pawns.index(MOVING_PAWN)
            cell_x, cell_y = Field.cell_index(MOVING_PAWN.rect.center)
            content = (pawn_id, (cell_x, cell_y))
            msg = Msg(MSG_MOVE_PAWN, content)
            send_msg(msg, server_connection)
            MOVING_PAWN = None
    else:
        if l:
            MOVING_PAWN = is_mouse_over(pawns)


def update_interface(new_w : int, new_h : int):
    global WIDTH, HEIGHT, field
    dw = float(new_w) / WIDTH
    dh = float(new_h) / HEIGHT
    WIDTH = new_w
    HEIGHT = new_h
    old_fw, old_fh = field.get_rect().bottomright
    field = pygame.transform.smoothscale(field, (HEIGHT, HEIGHT))
    new_fw, new_fh = field.get_rect().bottomright
    d_fw = float(new_fw) / old_fw
    d_fh = float(new_fh) / old_fh
    for pawn in pawns:
        pawn.set_radius(pawn.get_radius() * d_fh)
        pawn.set_pos((pawn.rect.centerx * d_fw, pawn.rect.centery * d_fh))


def handle_msg(msg : Msg):
    if msg:
        if msg.type == MSG_MOVE_PAWN:
            pawn_id, (x, y) = msg.content
            game_field.set_pawn_cell(pawn_id, (x, y))
            


def run_game(_window : Surface, _server_connection : socket):
    global window, game_field, server_connection
    window = _window
    server_connection = _server_connection
    init()
    load_images()
    game_field = Field()
    
    quit = False
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
        
        handle_msg(receive_msg(server_connection))        
        handle_mouse() 
        draw()

        clock.tick(FPS)
