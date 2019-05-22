#!/usr/bin/env python3
""" Fractals in Python """
#pylint: disable=E0611
from math import floor
from pygame import display, init
from src.settings import Settings
import src.fractal_equations as fe
import src.color_equations as ce
import src.pygame_functions as pf


def main():
    """ Fractals Main """
    redraw = True
    # Get an instance of Settings
    settings = Settings()

    # Set the fractal and color equations to use
    fractal = fe.mandelbrot
    # fractal = fe.julia
    colorize = ce.colorize_hue

    # Create the color palette
    palette = colorize(settings)

    # Initialize Pygame and create a screen
    init()
    screen = display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    while True:
        # Set display title
        display.set_caption(f"RE:({settings.RE_START}, {settings.RE_END}), "
                            f"IM:({settings.IM_START}, {settings.IM_END})")


        if redraw:
            # Regenerate point_list
            point_list = fractal(settings)

            # Render
            pf.display_fractal(palette, screen, point_list)

            display.flip()
        redraw = pf.check_events(settings)


if __name__ == "__main__":
    main()
