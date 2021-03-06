""" Pygame functions for Fractals """

from math import floor
from datetime import datetime
import pygame
import src.dialog_box as db


def check_events(settings):
    """ Check events """
    l_mouse_down = None
    r_mouse_down = None

    while True:

        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            exit()

        elif event.type == pygame.KEYDOWN:
            return check_keydown(settings, event)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            l_mouse_down = left_mouse_down()

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            return left_mouse_up(settings, l_mouse_down)

        elif event.type == pygame.MOUSEMOTION and l_mouse_down is not None:
            left_mouse_button_movement(settings, l_mouse_down)

        elif event.type == pygame.MOUSEMOTION and r_mouse_down is not None:
            right_mouse_button_movement(settings, r_mouse_down)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 2:
            return center_mouse_up(settings)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            r_mouse_down = right_mouse_down()

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            return right_mouse_up(settings, r_mouse_down)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
            return mouse_wheel_up(settings)

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
            return mouse_wheel_down(settings)


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
    """
        Loads the previous point from history into the current settings.

        If the current screen is wider than the coordinates stored in history,
            we use the imaginary (y) values that are saved, then adjust the real values
            (x) based on the difference in screen ratios.
        If the current screen is taller than the coordinates stored in history,
            we use the real (x) values that are saved, then adjust the imaginary values
            (y) based on the difference in screen rations.
        Else the ratios are the same even if the screen size isn't,
            we load all the saved values from history.
    """

    coordinates = settings.history.pop()

    if settings.ratio() < coordinates[4]:  # Screen is wider
        delta = (coordinates[4] - settings.ratio())
        re_start = coordinates[0]
        re_end = coordinates[1]
        settings.RE_START = re_start - ((re_end - re_start) * delta)
        settings.RE_END = re_end + ((re_end - re_start) * delta)
        settings.IM_START = coordinates[2]
        settings.IM_END = coordinates[3]

    elif settings.ratio() > coordinates[4]:  # Screen is taller
        delta = (settings.ratio() - coordinates[4]) / 2
        im_start = coordinates[2]
        im_end = coordinates[3]
        settings.RE_START = coordinates[0]
        settings.RE_END = coordinates[1]
        settings.IM_START = im_start - ((im_end - im_start) * delta)
        settings.IM_END = im_end + ((im_end - im_start) * delta)

    else:  # settings.ratio == coordinates[4]:
        settings.RE_START = coordinates[0]
        settings.RE_END = coordinates[1]
        settings.IM_START = coordinates[2]
        settings.IM_END = coordinates[3]

    settings.DRAW = True


def left_mouse_down():
    """ Left mouse button down event - capture mouse position """
    return pygame.mouse.get_pos()


def left_mouse_button_movement(settings, mouse_down):
    # We're going to draw over our current screen, but need to refresh it after every
    #   frame.  We blit the screen onto a backup surface.
    if mouse_down:
        backup_surface = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        backup_surface.blit(settings.SCREEN, (0, 0))

        mpos = pygame.mouse.get_pos()

        draw_selection_box(
            settings,
            min(mouse_down[0], mpos[0]),
            max(mouse_down[0], mpos[0]),
            min(mouse_down[1], mpos[1]),
            max(mouse_down[1], mpos[1]),
        )

        # Restore the original screen clearing the selection box we just drew.
        settings.SCREEN.blit(backup_surface, (0, 0))


def right_mouse_button_movement(settings, mouse_down):
    if mouse_down:
        backup_surface = pygame.Surface((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        backup_surface.blit(settings.SCREEN, (0, 0))

        mpos = pygame.mouse.get_pos()

        pygame.draw.line(
            settings.SCREEN,
            (255, 255, 255, 0),
            (mpos[0], -settings.SCREEN_HEIGHT * 2),
            (mpos[0], settings.SCREEN_HEIGHT * 2)
        )
        pygame.draw.line(
            settings.SCREEN,
            (255, 255, 255, 0),
            (-settings.SCREEN_WIDTH * 2, mpos[1]),
            (settings.SCREEN_WIDTH * 2, mpos[1]),
        )

        pygame.display.flip()
        settings.SCREEN.blit(backup_surface, (0, 0))


def left_mouse_up(settings, mouse_down):
    """ Left mouse button up event - zoom in on mouse selection area """
    mouse_up = pygame.mouse.get_pos()

    # Trapping some corner case that shouldn't exist, but occasionally does.
    if mouse_down is None or mouse_up is None:
        return

    # Click but no movement
    if mouse_down[0] == mouse_up[0] and mouse_down[1] == mouse_up[1]:
        return

    # Save current coordinates
    save_current_point(settings)

    left = min(mouse_down[0], mouse_up[0])
    right = max(mouse_down[0], mouse_up[0])
    top = min(mouse_down[1], mouse_up[1])
    bottom = max(mouse_down[1], mouse_up[1])

    # The user might draw a rectangle that isn't the same as our screen ratio.
    #   Here we calculate adjustments to their selection to maintain the screen ratio.
    delta = ((right - left) + (bottom - top)) / 2

    if (right - left) <= delta:
        h_adjust = (delta - (right - left)) / 2
    else:  # (right - left) > delta:
        h_adjust = -(((right - left) - delta) / 2)

    if (bottom - top) <= (delta * settings.ratio()):
        v_adjust = ((delta * settings.ratio()) - (bottom - top)) / 2
    else:  # (top - bottom) > (delta * settings.ratio()):
        v_adjust = -(((bottom - top) - (delta * settings.ratio())) / 2)

    # Center the zoom at the middle of the two click points
    left -= h_adjust
    right += h_adjust
    top -= v_adjust
    bottom += v_adjust

    # Show selection area on screen
    draw_selection_box(settings, left, right, top, bottom)

    # Calculate the % of the current corrdinate plane the mouse moved.
    start_percent_re = left / settings.SCREEN_WIDTH
    end_percent_re = right / settings.SCREEN_WIDTH
    start_percent_im = top / settings.SCREEN_HEIGHT
    end_percent_im = bottom / settings.SCREEN_HEIGHT

    # Calculate the new coordinate plane to render.
    new_start_re = settings.RE_START + (
        start_percent_re * (settings.RE_END - settings.RE_START)
    )
    new_end_re = new_start_re + (end_percent_re - start_percent_re) * (
        settings.RE_END - settings.RE_START
    )
    new_start_im = settings.IM_START + (
        start_percent_im * (settings.IM_END - settings.IM_START)
    )
    new_end_im = new_start_im + (end_percent_im - start_percent_im) * (
        settings.IM_END - settings.IM_START
    )

    # Update settings
    settings.RE_START = new_start_re
    settings.RE_END = new_end_re
    settings.IM_START = new_start_im
    settings.IM_END = new_end_im
    settings.DRAW = True


def center_mouse_up(settings):
    """ Center mouse button up event - Reset to default screen pos """
    save_current_point(settings)
    settings.RE_START = -2
    settings.RE_END = 1
    settings.IM_START = -(((settings.RE_END - settings.RE_START) * settings.ratio()) / 2)
    settings.IM_END = ((settings.RE_END - settings.RE_START) * settings.ratio()) / 2
    settings.DRAW = True


def right_mouse_down():
    """ Right mouse button down event - capture mouse position """
    return pygame.mouse.get_pos()


def right_mouse_up(settings, mouse_down):
    """ Right mouse button up event -  Shift screen based on mouse movement """
    mouse_up = pygame.mouse.get_pos()

    # Trapping some corner case that shouldn't exist, but occasionally does.
    if mouse_down is None or mouse_up is None:
        return

    # Click but no movement
    if mouse_down[0] == mouse_up[0] and mouse_down[1] == mouse_up[1]:
        return

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
    save_current_point(settings)

    # Update settings to new coordinate plane
    settings.RE_START = settings.RE_START + horizontal_shift
    settings.RE_END = settings.RE_END + horizontal_shift
    settings.IM_START = settings.IM_START + verticle_shift
    settings.IM_END = settings.IM_END + verticle_shift

    settings.DRAW = True


def mouse_wheel_down(settings):
    """ Mouse wheel down event, zoom out by settings.MWHEEL_ZOOM """

    re_adjust = (settings.RE_START - settings.RE_END) * settings.MWHEEL_ZOOM
    im_adjust = (settings.IM_START - settings.IM_END) * settings.MWHEEL_ZOOM

    # Save current coordinates
    save_current_point(settings)

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
    save_current_point(settings)

    settings.RE_START -= re_adjust
    settings.RE_END += re_adjust
    settings.IM_START -= im_adjust
    settings.IM_END += im_adjust

    settings.DRAW = True


def display_fractal(settings):
    """ Draw the fractal to the screen """
    for point in settings.point_list:
        settings.SCREEN.set_at((point[0], point[1]), settings.palette[floor(point[2])])


def draw_selection_box(settings, left, right, top, bottom):
    # Create a box from a surface and set transparency to 50%
    box_inside = pygame.Surface((right - left, bottom - top))
    box_inside.set_alpha(50)
    box_inside.fill((255, 255, 255))  # Fill the surface white

    # Create a rectable and blit it to the screen.
    box_outside = pygame.Rect(left, top, (right - left), (bottom - top))
    pygame.draw.rect(settings.SCREEN, pygame.Color(255, 255, 255), box_outside, 1)
    settings.SCREEN.blit(box_inside, (left, top))

    pygame.display.flip()


def save_current_point(settings):
    # Save current coordinates
    settings.history.append(
        (
            settings.RE_START,
            settings.RE_END,
            settings.IM_START,
            settings.IM_END,
            settings.ratio()
        )
    )
