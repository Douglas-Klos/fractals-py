#!/usr/bin/env python3
""" Fractals in Python """

from pygame import display, init
from src.settings import Settings
import src.pygame_functions as pf


def main():
    """ Fractals Main """

    # Initialize settings object
    settings = Settings()

    # Initialize Pygame and create a screen
    init()
    settings.SCREEN = display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    while True:
        fractal = settings.fractal_alg[settings.FRACTAL_ALGORITHM]
        colorize = settings.color_alg[settings.COLOR_ALGORITHM]

        if settings.COLOR:
            # Regenreate color settings.palette.
            settings.palette = colorize(settings)

        if settings.DRAW:
            # Regenerate settings.point_list
            settings.point_list = fractal(settings)

        pf.display_fractal(settings)

        # Set display title
        display.set_caption(
            f"RE:({settings.RE_START}, {settings.RE_END}), "
            f"IM:({settings.IM_START}, {settings.IM_END})"
        )

        display.flip()

        settings.COLOR = False
        settings.DRAW = False

        pf.check_events(settings)


if __name__ == "__main__":
    main()
