#!/usr/bin/env python3
""" Fractals in Python """
#pylint: disable=E0611
from pygame import display, init
from src.settings import Settings
import src.fractal_equations as fe
import src.color_equations as ce
import src.pygame_functions as pf


def main():
    """ Fractals Main """
    # Get an instance of Settings
    settings = Settings()

    fractal = fe.mandelbrot
    colorize = ce.colorize_hue

    # Generate our fractal points
    point_list = fractal(settings)

    # Create the color palette
    palette = colorize(settings)

    # Initialize Pygame and create a screen
    init()
    screen = display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    display.set_caption(f"Fractals")

    pf.display_fractal(palette, screen, point_list)
    display.flip()

    while True:
        pf.check_events(screen, settings, palette, fractal)


if __name__ == "__main__":
    main()
