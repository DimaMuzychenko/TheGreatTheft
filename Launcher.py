import pygame
import pygame_gui
import Packages.join_menu as join_menu
from Packages.config import *
from Packages.ui_config import *

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.Surface((WIDTH, HEIGHT))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((WIDTH, HEIGHT))

ui_container = pygame_gui.elements.UIPanel(relative_rect=window_surface.get_rect(),
                                               starting_layer_height=0,
                                               manager=manager,
                                               margins={'top' : 0, 'right' : 0, 'bottom' : 0, 'left' : 0})

button_rect = pygame.Rect(BUTTON_RECT)
button_rect.center = (WIDTH/2, HEIGHT/2)
button_rect.move_ip(0, -70)
join_room_button = pygame_gui.elements.UIButton(relative_rect=button_rect,
                                            text='Приєднатись до гри',
                                            manager=manager,
                                            container=ui_container)

button_rect.move_ip(0, 70)
create_room_button = pygame_gui.elements.UIButton(relative_rect=button_rect,
                                            text='Створити гру',
                                            manager=manager,
                                            container=ui_container)

button_rect.move_ip(0, 70)
quit_button = pygame_gui.elements.UIButton(relative_rect=button_rect,
                                            text='Вийти',
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
              if event.ui_element == join_room_button:
                  join_menu.run(window_surface)
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
              if event.ui_element == create_room_button:
                  pass
        
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
              if event.ui_element == quit_button:
                  is_running = False
        
        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
