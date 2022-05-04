import pygame, pygame_gui
import socket
import pickle
from .network import *
from pygame import Surface
from .config import *
from .ui_config import *
from .game import run_game



def try_connect(address : str, name : str, socket : socket.socket) -> str:
    try:
        host, port = tuple(address.split(':'))
        port = int(port)
    except ValueError:
        return 'Невірна адреса!'
    msg = Msg(MSG_NEW_PLAYER, name)
    log('Msg', msg, 'to', (host, port))
    socket.sendto(pickle.dumps(msg, 5), (host, port))
    respond = None
    while not respond:
        respond = receive_msg(socket)
    log('Got respond', respond)
    if respond.type == MSG_NEW_PLAYER:
        if respond.content == 'OK':
            return 'OK'
        else:
            return "Ім'я зайняте!"
    return 'Невідома помилка, спробуйте ще раз!'

  

def run(window : Surface):
    width, height = window.get_rect().bottomright
    manager = pygame_gui.UIManager((width, height))



    ui_container = pygame_gui.elements.UIPanel(relative_rect=window.get_rect(),
                                                starting_layer_height=0,
                                                manager=manager,
                                                margins={'top' : 0, 'right' : 0, 'bottom' : 0, 'left' : 0})
    
    error_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect(0, height/4, width, BUTTON_HEIGHT),
                                              text='',
                                              manager=manager,
                                              container=ui_container)

    button_rect = pygame.Rect(BUTTON_RECT)
    button_rect.center = (width/2, height/2)
    button_rect.move_ip(0, -210)
    
    label_rect = pygame.Rect(button_rect.left, button_rect.centery + button_rect.height, button_rect.width, button_rect.height/2)
    address_label = pygame_gui.elements.UILabel(relative_rect=label_rect,
                                                text='Адреса сервера:',
                                                manager=manager,
                                                container=ui_container)
    
    button_rect.move_ip(0, 100)
    address_entry_line = pygame_gui.elements.UITextEntryLine(relative_rect=button_rect,
                                                manager=manager,
                                                container=ui_container)
    
    label_rect.move_ip(0, 70)
    name_label = pygame_gui.elements.UILabel(relative_rect=label_rect,
                                                text="Ваше ім'я:",
                                                manager=manager,
                                                container=ui_container)
    
    button_rect.move_ip(0, 70)
    name_entry_line = pygame_gui.elements.UITextEntryLine(relative_rect=button_rect,
                                                manager=manager,
                                                container=ui_container)

    button_rect.move_ip(0, 70)
    connect_button = pygame_gui.elements.UIButton(relative_rect=button_rect,
                                                text='Підключитись',
                                                manager=manager,
                                                container=ui_container)

    button_rect.move_ip(0, 70)
    back_button = pygame_gui.elements.UIButton(relative_rect=button_rect,
                                                text='Назад',
                                                manager=manager,
                                                container=ui_container)

    clock = pygame.time.Clock()
    is_running = True

    while is_running:
        time_delta = clock.tick(FPS)/1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == connect_button:
                    sock = create_client_socket()
                    result = try_connect(address_entry_line.get_text(), name_entry_line.get_text(), sock)
                    if result == 'OK':
                        run_game(window, sock)
                    else:
                        error_label.set_text(error_label)
            
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == back_button:
                    is_running = False
            
            manager.process_events(event)

        manager.update(time_delta)

        manager.draw_ui(window)

        pygame.display.update()
