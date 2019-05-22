""" Color functions for fractals """
# pylint: disable=C0103

from colorsys import hsv_to_rgb
from math import sin, cos, log, floor, ceil


def colorize_hue(settings):
    """ Calculate hue color palette """
    palette = [0] * settings.MAX_ITER

    for i in range(settings.MAX_ITER):
        f = 1 - abs(
            (float(i) / settings.MAX_ITER - 1)
            ** (settings.MAX_ITER / settings.COLOR_SCALE)
        )

        hue = 0.66 + f / 3
        sat = 1 - f
        val = f if i < settings.MAX_ITER - 1 else 0

        # print(f"f:{f}, hue:{hue}, sat:{sat}, val:{val}")

        r, g, b = hsv_to_rgb(hue, sat, val)
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


def colorize_log(settings):
    """ Calculate a log color palette """
    palette = [0] * settings.MAX_ITER

    for i in range(settings.MAX_ITER):

        f = log(1 + (i / settings.MAX_ITER), 7)

        hue = 1 / ((f / 2) + 0.6)
        sat = 1 - f
        val = 0.3 + f if i < settings.MAX_ITER - 1 else 0

        print(f"f:{f}, hue:{hue}, sat:{sat}, val:{val}")

        r, g, b = hsv_to_rgb(hue, sat, val)
        palette[i] = (int(r * 255), int(g * 255), int(b * 255))

    return palette


def colorize_hue2(settings):
    """ Calculate hue color palette """
    palette = [0] * settings.MAX_ITER

    for i in range(settings.MAX_ITER):

        hue = 0.66 + (
            1 - abs((float(i) / settings.MAX_ITER - 1) ** (settings.MAX_ITER / 32)) / 3
        )
        sat = 1 - abs(((i / settings.MAX_ITER) - 1) ** 1024 / 32)
        val = (
            abs(1 - abs(((i - 4) / settings.MAX_ITER) - 1) ** 32)
            if i < settings.MAX_ITER - 1
            else 0
        )

        # print(f"hue:{hue}, sat:{sat}, val:{val}")

        r, g, b = hsv_to_rgb(hue, sat, val)
        palette[i] = (int(r * 255), int(g * 255), int(b * 255))

    return palette


def colorize_hue_shifting(settings, point_list):
    hues = []
    for point in point_list:
        hues.append(floor(point[2]))

    min_val = min(set(hues))

    palette = [0] * settings.MAX_ITER

    for i in range(settings.MAX_ITER):
        hue = 0.7 + (
            1 - abs((float(i) / settings.MAX_ITER - 1) ** (settings.MAX_ITER / 128)) / 4
        )
        sat = 1 - abs(((i / settings.MAX_ITER) - 1) ** 1024 / 32)
        val = (
            abs(1 - abs(((i - min_val - 10) / settings.MAX_ITER) - 1) ** 32)
            if i < settings.MAX_ITER - 1
            else 0
        )

        # print(f"hue:{hue}, sat:{sat}, val:{val}")

        r, g, b = hsv_to_rgb(hue, sat, val)
        palette[i] = (int(r * 255), int(g * 255), int(b * 255))

    return palette
