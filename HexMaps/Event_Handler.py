from Map_Handler import Map_Handler
import pygame

GAME_MOUSE_DOWN_FLAG = False

def handle_event(event, MAP_HANDLER, GAME_RECT):
    if event.type == pygame.KEYDOWN:
        # save map with return
        if event.key == pygame.K_RETURN:    MAP_HANDLER.save_map_to_file()
        # move map with arrow keys
        elif event.key == pygame.K_LEFT:    MAP_HANDLER.shift_offset(-1,0)
        elif event.key == pygame.K_DOWN:    MAP_HANDLER.shift_offset(-0.5,1)
        elif event.key == pygame.K_RIGHT:   MAP_HANDLER.shift_offset(1,0)
        elif event.key == pygame.K_UP:      MAP_HANDLER.shift_offset(0.5,-1)
        # zoom with + and - keys
        elif event.key == pygame.K_PLUS  or event.key == pygame.K_KP_PLUS:  
            MAP_HANDLER.change_scale(1, focus = pygame.mouse.get_pos())
        elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:  
            MAP_HANDLER.change_scale(-1, focus = pygame.mouse.get_pos())
        # place/delete hex with keys
        elif event.key == pygame.K_DELETE: 
            if MAP_HANDLER.get_select() != False:    MAP_HANDLER.set_tiles_on_map(list(MAP_HANDLER.get_select_tile()), 0)
        elif event.key == pygame.K_0 or event.key == pygame.K_KP0: 
            if MAP_HANDLER.get_select() != False:    MAP_HANDLER.set_tiles_on_map(list(MAP_HANDLER.get_select_tile()), 0)
        elif event.key == pygame.K_1 or event.key == pygame.K_KP1: 
            if MAP_HANDLER.get_select() != False:    MAP_HANDLER.set_tiles_on_map(list(MAP_HANDLER.get_select_tile()), 1)
        elif event.key == pygame.K_2 or event.key == pygame.K_KP2: 
            if MAP_HANDLER.get_select() != False:    MAP_HANDLER.set_tiles_on_map(list(MAP_HANDLER.get_select_tile()), 2)
        elif event.key == pygame.K_3 or event.key == pygame.K_KP3: 
            if MAP_HANDLER.get_select() != False:    MAP_HANDLER.set_tiles_on_map(list(MAP_HANDLER.get_select_tile()), 3)
        elif event.key == pygame.K_4 or event.key == pygame.K_KP4: 
            if MAP_HANDLER.get_select() != False:    MAP_HANDLER.set_tiles_on_map(list(MAP_HANDLER.get_select_tile()), 4)
        elif event.key == pygame.K_5 or event.key == pygame.K_KP5: 
            if MAP_HANDLER.get_select() != False:    MAP_HANDLER.set_tiles_on_map(list(MAP_HANDLER.get_select_tile()), 5)
        elif event.key == pygame.K_6 or event.key == pygame.K_KP6: 
            if MAP_HANDLER.get_select() != False:    MAP_HANDLER.set_tiles_on_map(list(MAP_HANDLER.get_select_tile()), 6)
        elif event.key == pygame.K_7 or event.key == pygame.K_KP7: 
            if MAP_HANDLER.get_select() != False:    MAP_HANDLER.set_tiles_on_map(list(MAP_HANDLER.get_select_tile()), 7)
        elif event.key == pygame.K_8 or event.key == pygame.K_KP8: 
            if MAP_HANDLER.get_select() != False:    MAP_HANDLER.set_tiles_on_map(list(MAP_HANDLER.get_select_tile()), 8)
        elif event.key == pygame.K_9 or event.key == pygame.K_KP9: 
            if MAP_HANDLER.get_select() != False:    MAP_HANDLER.set_tiles_on_map(list(MAP_HANDLER.get_select_tile()), 9)
        # move selected hex with weadyx keys
        elif event.key == pygame.K_s:   MAP_HANDLER.move_select("s")
        elif event.key == pygame.K_w:   MAP_HANDLER.move_select("w")
        elif event.key == pygame.K_e:   MAP_HANDLER.move_select("e")
        elif event.key == pygame.K_a:   MAP_HANDLER.move_select("a")
        elif event.key == pygame.K_d:   MAP_HANDLER.move_select("d")
        elif event.key == pygame.K_y:   MAP_HANDLER.move_select("y")
        elif event.key == pygame.K_z:   MAP_HANDLER.move_select("y")
        elif event.key == pygame.K_x:   MAP_HANDLER.move_select("x")
        # increase / decrease selection radius with r / q
        elif event.key == pygame.K_q:   MAP_HANDLER.increase_selection_radius(-1)
        elif event.key == pygame.K_r:   MAP_HANDLER.increase_selection_radius(1)

        # print distance between two selcted tiles
        elif event.key == pygame.K_g:   print(MAP_HANDLER.get_selected_distance())
    # mouse click to select hex, mouse drag to drag map, mousewheel to zoom
    global GAME_MOUSE_DOWN_FLAG
    if event.type == pygame.MOUSEBUTTONDOWN:
        if GAME_RECT.collidepoint(pygame.mouse.get_pos()):
            pygame.mouse.get_rel()
            GAME_MOUSE_DOWN_FLAG = True  # button down inside window
    if event.type == pygame.MOUSEBUTTONUP: 
        if GAME_MOUSE_DOWN_FLAG:         # count click if started in window
            if event.button == 1: 
                rel = pygame.mouse.get_rel()
                if (abs(rel[0] < 10) and abs(rel[1]) < 10): 
                    MAP_HANDLER.select(*pygame.mouse.get_pos())
                else: MAP_HANDLER.move_with_mouse(rel)
            elif event.button == 3: 
                rel = pygame.mouse.get_rel()
                if (abs(rel[0] < 10) and abs(rel[1]) < 10): 
                    MAP_HANDLER.select(*pygame.mouse.get_pos(), secondary=1)
            elif event.button == 4: 
                pos = pygame.mouse.get_pos()
                MAP_HANDLER.change_scale(3, focus = pygame.mouse.get_pos())
            elif event.button == 5: 
                pos = pygame.mouse.get_pos()
                MAP_HANDLER.change_scale(-3, focus = pygame.mouse.get_pos())
            GAME_MOUSE_DOWN_FLAG = False
