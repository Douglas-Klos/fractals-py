""" Color functions for fractals """
# pylint: disable=C0103

from colorsys import hsv_to_rgb
from math import sin, cos


def colorize_hue(settings):
    """ Calculate hue color palette """
    palette = [0] * settings.MAX_ITER

    for i in range(settings.MAX_ITER):
        f = 1 - abs(
            (float(i) / settings.MAX_ITER - 1)
            ** (settings.MAX_ITER / settings.COLOR_SCALE)
        )
        r, g, b = hsv_to_rgb(0.66 + f / 3, 1 - f, f if i < settings.MAX_ITER - 1 else 0)
        palette[i] = (int(r * 255), int(g * 255), int(b * 255))

    return palette


def colorize_linear(settings):
    """ Calculate linear color palette """
    palette = [0] * settings.MAX_ITER

    for i in range(settings.MAX_ITER):
        r, g, b = hsv_to_rgb(
            i / settings.MAX_ITER, 1, 1 if i < settings.MAX_ITER - 1 else 0
        )
        palette[i] = (int(r * 255), int(g * 255), int(b * 255))

    return palette


def colorize_sin(settings):
    """ Calculate sin color palette """
    palette = [0] * settings.MAX_ITER

    for i in range(settings.MAX_ITER):
        r, g, b = hsv_to_rgb(abs(sin(i)), 1, 1 if i < settings.MAX_ITER - 1 else 0)
        palette[i] = (int(r * 255), int(g * 255), int(b * 255))

    return palette


def colorize_cos(settings):
    """ Calculate cos color palette """
    palette = [0] * settings.MAX_ITER

    for i in range(settings.MAX_ITER):
        r, g, b = hsv_to_rgb(abs(cos(i)), 1, 1 if i < settings.MAX_ITER - 1 else 0)
        palette[i] = (int(r * 255), int(g * 255), int(b * 255))

    return palette
