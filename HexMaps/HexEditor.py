import pygame
import Event_Handler
from Map_Window import Map_Window
from Taskbar_Window import Taskbar_Window
from Map_Handler import Map_Handler


def on_start():    
    print(f"Started.")

def handle_event(event):
    if event.type == pygame.QUIT:
        TASKBAR_WINDOW.destroy()
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
            if event.type == pygame.VIDEORESIZE: MAP_WINDOW.on_resize()
            else: handle_event(event)
        MAP_WINDOW.clear()
        MAP_WINDOW.draw()
        pygame.display.update()
        CLOCK.tick(MAP_FPS)
        TASKBAR_WINDOW.update()

if __name__ == "__main__":
    GAME_IS_RUNNING                 = True
    MAP_FPS                         = 10
    MAP_HANDLER                     = Map_Handler()
    CLOCK                           = pygame.time.Clock()

    MAP_WINDOW                      = Map_Window(MAP_HANDLER, MAP_FPS=MAP_FPS)
    TASKBAR_WINDOW                  = Taskbar_Window(MAP_HANDLER)

    on_start()
    main_loop()
    pygame.quit()
    quit()