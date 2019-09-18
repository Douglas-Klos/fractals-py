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

    fractal = settings.fractal_alg[settings.FRACTAL_ALGORITHM]
    colorize = settings.color_alg[settings.COLOR_ALGORITHM]

    point_list = fractal(settings)
    palette = colorize(settings, point_list)

    while True:
        pf.display_fractal(settings, palette, point_list)

        # Set display title
        display.set_caption(
            f"RE:({settings.RE_START}, {settings.RE_END}), "
            f"IM:({settings.IM_START}, {settings.IM_END})"
        )

        display.flip()

        settings.COLOR = False
        settings.DRAW = False
        pf.check_events(settings)

        fractal = settings.fractal_alg[settings.FRACTAL_ALGORITHM]
        colorize = settings.color_alg[settings.COLOR_ALGORITHM]

        if settings.COLOR:
            # Regenreate color palette.
            palette = colorize(settings, point_list)

        if settings.DRAW:
            # Regenerate point_list
            point_list = fractal(settings)


if __name__ == "__main__":
    main()
