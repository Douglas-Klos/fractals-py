""" Pygame functions for Fractals """
# pylint: disable=C0301, E1101, W0212

from math import floor
import pygame


def check_events(settings):
    """ Check events """
    mouse_down = None

    while True:

        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown(event)
            return False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_down = left_mouse_down()

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            return left_mouse_up(settings, mouse_down)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 2:
            return center_mouse_up(settings)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouse_down = right_mouse_down()

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            return right_mouse_up(settings, mouse_down)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            return mouse_wheel_up(settings)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            return mouse_wheel_down(settings)


def left_mouse_down():
    """ Left mouse button down event - capture mouse position """
    return pygame.mouse.get_pos()


def left_mouse_up(settings, mouse_down):
    """ Left mouse button up event - zoom in on mouse selection area """
    mouse_up = pygame.mouse.get_pos()

    if (mouse_down[0] == mouse_up[0] and mouse_down[1] == mouse_up[1]):
        return False

    if mouse_down[0] < mouse_up[0]:
        left = mouse_down[0]
        right = mouse_up[0]
    else:
        left = mouse_up[0]
        right = mouse_down[0]

    if mouse_down[1] < mouse_up[1]:
        bottom = mouse_down[1]
        top = mouse_up[1]
    else:
        bottom = mouse_up[1]
        top = mouse_down[1]

    # We want to maintain our ratio to prevent distorting.
    #   This needs work, it maintains a square ration, change so it maintains
    #   whatever the initial ratio might have been, to support different
    #   screen sizes.
    delta = ((right - left) + (top - bottom)) / 2

    if (right - left) < delta:
        h_adjust = (delta - (right - left)) / 2
    elif (right - left) > delta:
        h_adjust = -(((right - left) - delta) / 2)
    else:
        h_adjust = delta
    if (top - bottom) < delta:
        v_adjust = (delta - (top - bottom)) / 2
    elif (top - bottom) > delta:
        v_adjust = -(((top - bottom) - delta) / 2)
    else:
        v_adjust = delta

    # We also want to center the zoom center of the two points
    left -= h_adjust
    right += h_adjust
    bottom -= v_adjust
    top += v_adjust

    # Calculate the % of the current corrdinate plane the mouse moved.
    start_percent_re = left / settings.SCREEN_WIDTH
    end_percent_re = right / settings.SCREEN_WIDTH
    start_percent_im = bottom / settings.SCREEN_HEIGHT
    end_percent_im = top / settings.SCREEN_HEIGHT

    # Calculate the new coordinate plane to render.
    new_start_re = settings.RE_START + abs(
        (start_percent_re * abs((settings.RE_START - settings.RE_END)))
    )
    new_end_re = new_start_re + abs((end_percent_re - start_percent_re)) * abs(
        (settings.RE_START - settings.RE_END)
    )
    new_start_im = settings.IM_START + abs(
        (start_percent_im * abs((settings.IM_START - settings.IM_END)))
    )
    new_end_im = new_start_im + abs((end_percent_im - start_percent_im)) * abs(
        (settings.IM_START - settings.IM_END)
    )

    # Update settings
    settings.RE_START = new_start_re
    settings.RE_END = new_end_re
    settings.IM_START = new_start_im
    settings.IM_END = new_end_im

    return True


def center_mouse_up(settings):
    """ Center mouse button up event - Reset to default screen pos """
    settings.RE_START = -2
    settings.RE_END = 1
    settings.IM_START = -1.5
    settings.IM_END = 1.5

    return True


def right_mouse_down():
    """ Right mouse button down event - capture mouse position """
    return pygame.mouse.get_pos()


def right_mouse_up(settings, mouse_down):
    """ Right mouse button up event -  Shift screen based on mouse movement """
    mouse_up = pygame.mouse.get_pos()

    if (
        mouse_down[0] == mouse_up[0]
        and mouse_down[1] == mouse_up[1]
    ):
        return False

    # Calculate how many pixels the mouse moved while right clicked
    horizontal_movement = mouse_up[0] - mouse_down[0]
    verticle_movement = mouse_up[1] - mouse_down[1]

    # Calculate percentage of screen moved
    horizontal_percent = horizontal_movement / settings.SCREEN_WIDTH
    verticle_percent = verticle_movement / settings.SCREEN_HEIGHT

    # Calculate percentage of coordinate plane moved
    horizontal_shift = horizontal_percent * (
        settings.RE_START - settings.RE_END
    )
    verticle_shift = verticle_percent * (settings.IM_START - settings.IM_END)

    # Update settings to new coordinate plane
    settings.RE_START = settings.RE_START + horizontal_shift
    settings.RE_END = settings.RE_END + horizontal_shift
    settings.IM_START = settings.IM_START + verticle_shift
    settings.IM_END = settings.IM_END + verticle_shift

    return True


def mouse_wheel_down(settings):
    """ Mouse wheel down event, zoom out 10% """

    re_adjust = (settings.RE_START - settings.RE_END) * .1
    im_adjust = (settings.IM_START - settings.IM_END) * .1

    settings.RE_START += re_adjust
    settings.RE_END -= re_adjust
    settings.IM_START += im_adjust
    settings.IM_END -= im_adjust

    return True


def mouse_wheel_up(settings):
    """ Mouse wheel up event, zoom in 10% """
    re_adjust = (settings.RE_START - settings.RE_END) * .1
    im_adjust = (settings.IM_START - settings.IM_END) * .1

    settings.RE_START -= re_adjust
    settings.RE_END += re_adjust
    settings.IM_START -= im_adjust
    settings.IM_END += im_adjust

    return True


def check_keydown(event):
    """ Check event when keydown is detected """
    if event.key == pygame.K_q:
        exit()


def display_fractal(palette, screen, point_list):
    """ Draw the fractal to the screen """
    for point in point_list:
        screen.set_at((point[0], point[1]), palette[floor(point[2])])
