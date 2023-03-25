import pygame
import Event_Handler
from Map_Window import Map_Window
from Taskbar_Window import Taskbar_Window


def on_start():    
    print(f"Started.")

def handle_event(event):
    if event.type == pygame.QUIT:
        pygame.quit()
        quit()
    elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE: 
            global GAME_IS_RUNNING 
            GAME_IS_RUNNING = False
    else:
        MAP_WINDOW.handle_event(event)
        
def main_loop():
    while GAME_IS_RUNNING:
        for event in pygame.event.get(): 
            if event.type == pygame.VIDEORESIZE: GAME_WINDOW.on_resize()
            else: handle_event(event)
        MAP_WINDOW.draw()
        pygame.display.update()
        CLOCK.tick(GAME_FPS)
        TASKBAR_WINDOW.update()

if __name__ == "__main__":
    GAME_IS_RUNNING                 = True
    GAME_FPS                        = 5

    CLOCK                           = pygame.time.Clock()

    MAP_WINDOW                      = Map_Window(GAME_FPS=GAME_FPS)
    TASKBAR_WINDOW                  = Taskbar_Window(MAP_WINDOW)

    on_start()
    main_loop()
    pygame.quit()