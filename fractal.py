#!/usr/bin/env python3
""" Fractals in Python """
#pylint: disable=E0401

from pygame import display, init
from src.settings import Settings
import src.fractal_equations as fe
import src.color_equations as ce
import src.pygame_functions as pf


def main():
    """ Fractals Main """
    draw = True

    # Get an instance of Settings
    settings = Settings()

    # Set the fractal and color equations to use
    fractal = fe.mandelbrot
    colorize = ce.colorize_rgb

    # Initialize Pygame and create a screen
    init()
    settings.SCREEN = display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    while True:
        # Set display title
        display.set_caption(f"RE:({settings.RE_START}, {settings.RE_END}), "
                            f"IM:({settings.IM_START}, {settings.IM_END})")

        fractal = eval(settings.FRACTAL_ALGORITHM)
        colorize = eval(settings.COLOR_ALGORITHM)  

        if draw:
            # Regenerate point_list
            point_list = fractal(settings)
            palette = colorize(settings, point_list)

            # Render
            pf.display_fractal(settings, palette, point_list)

            display.flip()

        draw = pf.check_events(settings)


if __name__ == "__main__":
    main()
