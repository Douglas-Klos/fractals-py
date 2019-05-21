import sys
import pygame
from math import floor
import src.functions as func


def check_events(screen, settings, palette):
    """ Check events """
    start_pos = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(event)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            settings._mouse_down = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            settings._mouse_up = pygame.mouse.get_pos()
            left_mouse_up_event(screen, settings, palette)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            settings._mouse_down = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            settings._mouse_up = pygame.mouse.get_pos()
            right_mouse_up_event(screen, settings, palette)


def right_mouse_up_event(screen, settings, palette):
    """ Shift screen based on mouse movement """
    # Calculate how many pixels the mouse moved while right clicked
    horizontal_movement = settings._mouse_up[0] - settings._mouse_down[0]
    verticle_movement = settings._mouse_up[1] - settings._mouse_down[1]

    # Calculate percentage of screen moved
    horizontal_percent = horizontal_movement / settings.SCREEN_WIDTH
    verticle_percent = verticle_movement / settings.SCREEN_HEIGHT

    # Calculate percentage of coordinate plane moved
    horizontal_shift = horizontal_percent * (settings.RE_START - settings.RE_END)
    verticle_shift = verticle_percent * (settings.IM_START - settings.IM_END)

    # Update settings to new coordinate plane
    settings.RE_START = settings.RE_START + horizontal_shift
    settings.RE_END = settings.RE_END + horizontal_shift
    settings.IM_START = settings.IM_START + verticle_shift
    settings.IM_END = settings.IM_END + verticle_shift

    # Regenerate point list
    point_list = func.fractal_list[settings.current_fractal](settings)

    # Render
    for point in point_list:
        screen.set_at((point[0], point[1]), palette[floor(point[2])])

    pygame.display.flip()


def left_mouse_up_event(screen, settings, palette):
    """ Zoom in on mouse selection area """
    if (settings._mouse_down[0] < settings._mouse_up[0]):
        # We want to maintain 1:1 ratio, so we move vert the same as horz
        #   regardless of user input.  Otherwise the image distorts.
        settings._mouse_up = (settings._mouse_up[0], settings._mouse_down[1] + (settings._mouse_up[0] - settings._mouse_down[0]))

        # Calculate the % of the current corrdinate plane the mouse moved.
        start_percent_re = (settings._mouse_down[0] / settings.SCREEN_WIDTH)
        end_percent_re = (settings._mouse_up[0] / settings.SCREEN_WIDTH)
        start_percent_im = (settings._mouse_down[1] / settings.SCREEN_HEIGHT)
        end_percent_im = (settings._mouse_up[1] / settings.SCREEN_HEIGHT)

        # Calculate the new coordinate plane to render.
        new_start_re = settings.RE_START + abs((start_percent_re * abs((settings.RE_START - settings.RE_END))))
        new_end_re = new_start_re + abs((end_percent_re - start_percent_re)) * abs((settings.RE_START - settings.RE_END))
        new_start_im = settings.IM_START + abs((start_percent_im * abs((settings.IM_START - settings.IM_END))))
        new_end_im = new_start_im + abs((end_percent_im - start_percent_im)) * abs((settings.IM_START - settings.IM_END))

        # # Output to stdout
        # print(f"start_percent_re:{start_percent_re}")
        # print(f"end_percent_re:{end_percent_re}")
        # print()
        # print(f"old_start_re:{settings.RE_START}")
        # print(f"new_start_re:{new_start_re}")
        # print(f"old_end_re:{settings.RE_END}")
        # print(f"new_end_re:{new_end_re}")
        # print()
        # print(f"old_start_im:{settings.IM_START}")
        # print(f"new_start_im:{new_start_im}")
        # print(f"old_end_im:{settings.IM_END}")
        # print(f"new_end_im:{new_end_im}")
        # print()

        # Update settings
        settings.RE_START = new_start_re
        settings.RE_END = new_end_re
        settings.IM_START = new_start_im
        settings.IM_END = new_end_im

        # Regenerate point_list
        point_list = func.fractal_list[settings.current_fractal](settings)

        # Render
        for point in point_list:
            screen.set_at((point[0], point[1]), palette[floor(point[2])])

        pygame.display.flip()


def check_keydown_event(event):
    """ Check event when keydown is detected """
    if event.key == pygame.K_q:
        sys.exit()
