#!/usr/bin/env python3
""" Fractals in Python """

import logging
from pygame import display, init
from src.settings import Settings
import src.pygame_functions as pf



def main():
    """ Fractals Main """

    # Initialize settings object
    settings = Settings()
    logging.basicConfig(level=logging.DEBUG)

    # Initialize Pygame and create a screen
    init()
    settings.SCREEN = display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    while True:
        fractal = settings.fractal_alg[settings.FRACTAL_ALGORITHM]
        colorize = settings.color_alg[settings.COLOR_ALGORITHM]

        if settings.COLOR:
            # Regenreate color settings.palette.
            logging.debug("Generating color palette...")
            settings.palette = colorize(settings)
            settings.COLOR = False

        if settings.DRAW:
            # Regenerate settings.point_list
            logging.debug("Generating point list palette...")
            settings.point_list = fractal(settings)
            settings.DRAW = False

        pf.display_fractal(settings)

        # Set display title
        display.set_caption(
            f"RE:({settings.RE_START}, {settings.RE_END}), "
            f"IM:({settings.IM_START}, {settings.IM_END})"
        )

        display.flip()

        pf.check_events(settings)


if __name__ == "__main__":
    main()
