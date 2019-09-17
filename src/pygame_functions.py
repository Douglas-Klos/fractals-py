""" Pygame functions for Fractals """
# pylint: disable=C0301, E1101, W0212

from datetime import datetime
import pygame
import src.dialog_box as db


def check_events(settings):
    """ Check events """
    mouse_down = None

    while True:

        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown(settings, event)
            break

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_down = left_mouse_down()

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            left_mouse_up(settings, mouse_down)
            break

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 2:
            center_mouse_up(settings)
            break

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouse_down = right_mouse_down()

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            right_mouse_up(settings, mouse_down)
            break

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            mouse_wheel_up(settings)
            break

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            mouse_wheel_down(settings)
            break


def check_keydown(settings, event):
    """ Check event when keydown is detected """
    if event.key == pygame.K_q:
        exit()

    elif event.key == pygame.K_SPACE:
        filename = f"{datetime.now():%Y-%m-%d %H-%M-%S}.png"
        print(f"Saving {filename}")
        pygame.image.save(settings.SCREEN, f"fractal {filename}")

    elif event.key == pygame.K_RETURN:
        db.construct_dialog_box(settings)

    elif event.key == pygame.K_BACKSPACE:
        if settings.history:
            load_from_history(settings)
            settings.DRAW = True


def load_from_history(settings):
    coordinates = settings.history.pop()

    settings.RE_START = coordinates[0]
    settings.RE_END = coordinates[1]

    im_start = coordinates[2]
    im_end = coordinates[3]
    ratio = coordinates[4]

    if ratio != settings.RATIO:
        delta = (settings.RATIO - ratio) / 2
        settings.IM_START = im_start - ((im_end - im_start) * delta)
        settings.IM_END = im_end + ((im_end - im_start) * delta)
    else:
        settings.IM_START = im_start
        settings.IM_END = im_end

    settings.DRAW = True


def left_mouse_down():
    """ Left mouse button down event - capture mouse position """
    return pygame.mouse.get_pos()


def left_mouse_up(settings, mouse_down):
    """ Left mouse button up event - zoom in on mouse selection area """
    mouse_up = pygame.mouse.get_pos()

    # Trapping some corner case that shouldn't exist, but occasionally does.
    if mouse_down == None or mouse_up == None:
        # False, do not redraw the screen
        return False

    # Rejecting clicks that didn't move
    if mouse_down[0] == mouse_up[0] and mouse_down[1] == mouse_up[1]:
        # False, do not redraw the screen
        return False

    # Setting left, right, bottom, top values for click points
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


    # Maintain our screen ratio
    delta = ((right - left) + (top - bottom)) / 2

    # print(f"left:{left}, right:{right}, bottom:{bottom}, top:{top}")
    # print(f"l-r:{left - right}, t-b:{top-bottom}")
    # print(f"delta:{delta}")

    # Calculate the amount to adjust screen position based on click points
    if (right - left) <= delta:
        h_adjust = (delta - (right - left)) / 2
    else:  # (right - left) > delta:
        h_adjust = -(((right - left) - delta) / 2)

    if (top - bottom) <= (delta * settings.RATIO):
        v_adjust = ((delta * settings.RATIO) - (top - bottom)) / 2
    else:  # (top - bottom) > (delta * settings.RATIO):
        v_adjust = -(((top - bottom) - (delta * settings.RATIO)) / 2)

    # Center the zoom at the middle of the two click points
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

    # Save current coordinates
    settings.history.append((settings.RE_START, settings.RE_END, settings.IM_START, settings.IM_END, settings.RATIO))

    # Update settings
    settings.RE_START = new_start_re
    settings.RE_END = new_end_re
    settings.IM_START = new_start_im
    settings.IM_END = new_end_im

    settings.DRAW = True


def center_mouse_up(settings):
    """ Center mouse button up event - Reset to default screen pos """
    # Save current coordinates
    settings.history.append((settings.RE_START, settings.RE_END, settings.IM_START, settings.IM_END, settings.RATIO))

    settings.RE_START = -2
    settings.RE_END = 1
    ratio = settings.SCREEN_HEIGHT / settings.SCREEN_WIDTH
    settings.IM_START = -(((settings.RE_END - settings.RE_START) * ratio) / 2)
    settings.IM_END = ((settings.RE_END - settings.RE_START) * ratio) / 2

    settings.DRAW = True


def right_mouse_down():
    """ Right mouse button down event - capture mouse position """
    return pygame.mouse.get_pos()


def right_mouse_up(settings, mouse_down):
    """ Right mouse button up event -  Shift screen based on mouse movement """
    mouse_up = pygame.mouse.get_pos()

    # Trapping some corner case that shouldn't exist, but occasionally does.
    if mouse_down == None or mouse_up == None:
        # False, do not redraw the screen
        return False

    if mouse_down[0] == mouse_up[0] and mouse_down[1] == mouse_up[1]:
        # False, do not redraw the screen
        return False

    # Calculate how many pixels the mouse moved while right clicked
    horizontal_movement = mouse_up[0] - mouse_down[0]
    verticle_movement = mouse_up[1] - mouse_down[1]

    # Calculate percentage of screen moved
    horizontal_percent = horizontal_movement / settings.SCREEN_WIDTH
    verticle_percent = verticle_movement / settings.SCREEN_HEIGHT

    # Calculate percentage of coordinate plane moved
    horizontal_shift = horizontal_percent * (settings.RE_START - settings.RE_END)
    verticle_shift = verticle_percent * (settings.IM_START - settings.IM_END)

    # Save current coordinates
    settings.history.append((settings.RE_START, settings.RE_END, settings.IM_START, settings.IM_END, settings.RATIO))

    # Update settings to new coordinate plane
    settings.RE_START = settings.RE_START + horizontal_shift
    settings.RE_END = settings.RE_END + horizontal_shift
    settings.IM_START = settings.IM_START + verticle_shift
    settings.IM_END = settings.IM_END + verticle_shift

    settings.DRAW = True


def mouse_wheel_down(settings):
    """ Mouse wheel down event, zoom out 10% """

    re_adjust = (settings.RE_START - settings.RE_END) * settings.MWHEEL_ZOOM
    im_adjust = (settings.IM_START - settings.IM_END) * settings.MWHEEL_ZOOM

    # Save current coordinates
    settings.history.append((settings.RE_START, settings.RE_END, settings.IM_START, settings.IM_END, settings.RATIO))

    settings.RE_START += re_adjust
    settings.RE_END -= re_adjust
    settings.IM_START += im_adjust
    settings.IM_END -= im_adjust

    settings.DRAW = True


def mouse_wheel_up(settings):
    """ Mouse wheel up event, zoom in 10% """
    re_adjust = (settings.RE_START - settings.RE_END) * settings.MWHEEL_ZOOM
    im_adjust = (settings.IM_START - settings.IM_END) * settings.MWHEEL_ZOOM

    # Save current coordinates
    settings.history.append((settings.RE_START, settings.RE_END, settings.IM_START, settings.IM_END, settings.RATIO))

    settings.RE_START -= re_adjust
    settings.RE_END += re_adjust
    settings.IM_START -= im_adjust
    settings.IM_END += im_adjust

    settings.DRAW = True


