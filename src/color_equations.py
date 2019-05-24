""" Color functions for fractals """
# pylint: disable=C0103

from .color import *
import pygame
import numpy as np
from colorsys import hsv_to_rgb
from math import sin, cos, tan, log, floor, ceil, sqrt
from numba import jit


def colorize_hue(settings, point_list, *_):
    hues = []
    palette = []
    val_count = 0
    for point in point_list:
        hues.append(floor(point[2]))

    min_val = min(set(hues))

    """ Calculate hue color palette """
    palette = [0] * settings.MAX_ITER

    for i in range(settings.MAX_ITER):
        f = 1 - abs(
            ((float(i) - min_val) / settings.MAX_ITER - 1) ** (settings.MAX_ITER / 32)
        )

        hue = 0.66 + f / 3
        sat = 1 - f
        val = f if i < settings.MAX_ITER - 1 else 0

        # print(f"f:{f}, hue:{hue}, sat:{sat}, val:{val}")

        r, g, b = hsv_to_rgb(hue, sat, val)
        palette[i] = [int(r * 255), int(g * 255), int(b * 255)]

    # geld(palette)
    return palette


def colorize_hue_shifted(settings, point_list, *_):
    hues = []
    palette = []
    val_count = 0
    for point in point_list:
        hues.append(floor(point[2]))

    min_val = min(set(hues))

    # print(settings.MAX_ITER)
    palette = [0] * settings.MAX_ITER

    for i in range(settings.MAX_ITER):
        hue = settings.HUE_SEED + (
            1
            - abs(
                ((float(i) - min_val) / settings.MAX_ITER - 1)
                ** (sqrt(settings.MAX_ITER))
            )
            / 4
        )
        sat = 1 - (
            1
            - abs(
                ((float(i) - min_val) / settings.MAX_ITER - 1)
                ** (sqrt(settings.MAX_ITER))
            )
        )
        val = (
            abs(
                1
                - abs(
                    (
                        (i - min_val - settings.SHIFT - (settings.MAX_ITER / 128))
                        / settings.MAX_ITER
                    )
                    - 1
                )
                ** 32
            )
            if i < settings.MAX_ITER - 1
            else 0
        )

        # print(f"hue:{hue}, sat:{sat}, val:{val}")

        r, g, b = hsv_to_rgb(hue, sat, val)

        palette[i] = [int(r * 255), int(g * 255), int(b * 255)]

    return geld(palette)


def geld(palette):
    """ When iterations get low, the palette numbers exceed limits

    We remove values that exceed limits and replace them with limit values
    """
    for color in palette:
        # print(color)
        if color[0] > 255:
            color[0] = 255
        if color[1] > 255:
            color[1] = 255
        if color[2] > 255:
            color[2] = 255
        if color[0] < 0:
            color[0] = 1
        if color[1] < 0:
            color[1] = 1
        if color[2] < 0:
            color[2] = 1

    return palette


def colorize_hue2(settings, *_):
    """ Calculate hue color palette """
    palette = [0] * settings.MAX_ITER

    for i in range(settings.MAX_ITER):
        hue = 0.46 + (
            1 - abs((i / (settings.MAX_ITER)) - 1) ** (settings.MAX_ITER / 64) / 3
        )
        sat = abs(i / settings.MAX_ITER - 1) ** (settings.MAX_ITER / 64)
        val = (
            abs(1 - abs((i / settings.MAX_ITER) - 1.03) ** (settings.MAX_ITER / 12))
            if i < settings.MAX_ITER - 1
            else 0
        )

        # print(f"hue:{hue}, sat:{sat}, val:{val}")

        r, g, b = hsv_to_rgb(hue, sat, val)
        palette[i] = (int(r * 255), int(g * 255), int(b * 255))

    return palette


def colorize_blue_green_sin(settings, point_list, *_):
    """ Calculate sin color palette """

    hues = []
    palette = []
    for point in point_list:
        hues.append(floor(point[2]))

    min_val = min(set(hues))

    palette = [0] * settings.MAX_ITER

    for i in range(settings.MAX_ITER):
        hue = 0.5 + 0.1 * (cos(i / (settings.MAX_ITER / 8)))
        sat = 0.5 + sin((settings.MAX_ITER / (settings.MAX_ITER ** 2)) * i)
        val = 0.5 + 0.5 * (sin(i / 64)) if i < settings.MAX_ITER - 1 else 0
        # print(f"hue:{hue}, sat:{sat}, val:{val}")
        r, g, b = hsv_to_rgb(hue, sat, val)
        palette[i] = [int(r * 255), int(g * 255), int(b * 255)]

    palette[settings.MAX_ITER - 1] = hsv_to_rgb(0, 0, 0)
    geld(palette)
    return palette


def colorize_blue_green_gold(settings, *_):
    gold = Color("gold")
    blue = Color("blue")
    black = Color("black")
    white = Color("white")
    palette = []
    return_palette = []

    palette1 = list(black.range_to(blue, 10 * floor(settings.MAX_ITER / 1024)))
    palette2 = list(blue.range_to(white, 20 * floor(settings.MAX_ITER / 1024)))
    palette3 = list(white.range_to(gold, 40 * floor(settings.MAX_ITER / 1024)))
    palette4 = list(gold.range_to(black, 40 * floor(settings.MAX_ITER / 1024)))
    palette5 = list(black.range_to(blue, 80 * floor(settings.MAX_ITER / 1024)))
    palette6 = list(blue.range_to(white, 80 * floor(settings.MAX_ITER / 1024)))
    palette7 = list(white.range_to(gold, 80 * floor(settings.MAX_ITER / 1024)))
    palette8 = list(gold.range_to(black, 100 * floor(settings.MAX_ITER / 1024)))
    palette9 = list(black.range_to(blue, 100 * floor(settings.MAX_ITER / 1024)))
    palette10 = list(blue.range_to(white, 100 * floor(settings.MAX_ITER / 1024)))
    palette11 = list(white.range_to(gold, 100 * floor(settings.MAX_ITER / 1024)))
    palette12 = list(gold.range_to(black, 100 * floor(settings.MAX_ITER / 1024)))
    palette13 = list(black.range_to(white, 200 * floor(settings.MAX_ITER / 1024)))

    palette = (
        palette1
        + palette2
        + palette3
        + palette4
        + palette5
        + palette6
        + palette7
        + palette8
        + palette9
        + palette10
        + palette11
        + palette12
        + palette13
    )

    for item in enumerate(palette):
        r = item[1].rgb[0]
        g = item[1].rgb[1]
        b = item[1].rgb[2]
        return_palette.append([int(r * 255), int(g * 255), int(b * 255)])

    return_palette[settings.MAX_ITER - 1] = (0, 0, 0)
    return return_palette


def colorize_black_shift(settings, *_):
    gold = Color("gold")
    red = Color("red")
    yellow = Color("yellow")
    green = Color("green")
    cyan = Color("cyan")
    blue = Color("blue")
    violet = Color("violet")
    black = Color("black")
    white = Color("white")

    palette = []
    return_palette = []

    palette1 = list(black.range_to(violet, 10 * floor(settings.MAX_ITER / 1024)))
    palette2 = list(black.range_to(red, 20 * floor(settings.MAX_ITER / 1024)))
    palette3 = list(black.range_to(yellow, 4 * floor(settings.MAX_ITER / 1024)))
    palette4 = list(black.range_to(green, 40 * floor(settings.MAX_ITER / 1024)))
    palette5 = list(black.range_to(cyan, 80 * floor(settings.MAX_ITER / 1024)))
    palette6 = list(black.range_to(blue, 80 * floor(settings.MAX_ITER / 1024)))
    palette7 = list(black.range_to(violet, 80 * floor(settings.MAX_ITER / 1024)))
    palette8 = list(black.range_to(red, 100 * floor(settings.MAX_ITER / 1024)))
    palette9 = list(black.range_to(yellow, 100 * floor(settings.MAX_ITER / 1024)))
    palette10 = list(black.range_to(green, 100 * floor(settings.MAX_ITER / 1024)))
    palette11 = list(black.range_to(cyan, 100 * floor(settings.MAX_ITER / 1024)))
    palette12 = list(black.range_to(blue, 100 * floor(settings.MAX_ITER / 1024)))
    palette13 = list(black.range_to(white, 250 * floor(settings.MAX_ITER / 1024)))

    palette = (
        palette1
        + palette2
        + palette3
        + palette4
        + palette5
        + palette6
        + palette7
        + palette8
        + palette9
        + palette10
        + palette11
        + palette12
        + palette13
    )

    for item in enumerate(palette):
        r = item[1].rgb[0]
        g = item[1].rgb[1]
        b = item[1].rgb[2]
        return_palette.append([int(r * 255), int(g * 255), int(b * 255)])

    return_palette[settings.MAX_ITER - 1] = (0, 0, 0)
    return return_palette


def colorize_black_gold(settings, *_):
    gold = Color("gold")
    black = Color("black")
    white = Color("white")
    palette = []
    return_palette = []
    palette1 = list(gold.range_to(black, 10 * floor(settings.MAX_ITER / 1024)))
    palette2 = list(black.range_to(gold, 20 * floor(settings.MAX_ITER / 1024)))
    palette3 = list(gold.range_to(black, 60 * floor(settings.MAX_ITER / 1024)))
    palette4 = list(black.range_to(gold, 60 * floor(settings.MAX_ITER / 1024)))
    palette5 = list(gold.range_to(black, 60 * floor(settings.MAX_ITER / 1024)))
    palette6 = list(black.range_to(gold, 60 * floor(settings.MAX_ITER / 1024)))
    palette7 = list(gold.range_to(black, 60 * floor(settings.MAX_ITER / 1024)))
    palette8 = list(black.range_to(gold, 60 * floor(settings.MAX_ITER / 1024)))
    palette9 = list(gold.range_to(black, 60 * floor(settings.MAX_ITER / 1024)))
    palette10 = list(black.range_to(gold, 444 * floor(settings.MAX_ITER / 1024)))
    palette11 = list(gold.range_to(black, 1000 * floor(settings.MAX_ITER / 1024)))

    palette = (
        palette1
        + palette2
        + palette3
        + palette4
        + palette5
        + palette6
        + palette7
        + palette8
        + palette9
        + palette10
        + palette11
    )

    for item in enumerate(palette):
        r = item[1].rgb[0]
        g = item[1].rgb[1]
        b = item[1].rgb[2]
        return_palette.append([int(r * 255), int(g * 255), int(b * 255)])

    return_palette[settings.MAX_ITER - 1] = (0, 0, 0)
    return return_palette


def colorize_white_green_black(settings, point_list, *_):
    black = Color("black")
    white = Color("white")
    green = Color("green")
    palette = []
    return_palette = []
    palette1 = list(white.range_to(green, 10 * floor(settings.MAX_ITER / 1024)))
    palette2 = list(green.range_to(black, 20 * floor(settings.MAX_ITER / 1024)))
    palette3 = list(black.range_to(green, 60 * floor(settings.MAX_ITER / 1024)))
    palette4 = list(green.range_to(white, 60 * floor(settings.MAX_ITER / 1024)))
    palette5 = list(white.range_to(green, 60 * floor(settings.MAX_ITER / 1024)))
    palette6 = list(green.range_to(white, 60 * floor(settings.MAX_ITER / 1024)))
    palette7 = list(white.range_to(green, 60 * floor(settings.MAX_ITER / 1024)))
    palette8 = list(green.range_to(black, 60 * floor(settings.MAX_ITER / 1024)))
    palette9 = list(black.range_to(green, 60 * floor(settings.MAX_ITER / 1024)))
    palette10 = list(green.range_to(white, 444 * floor(settings.MAX_ITER / 1024)))
    palette11 = list(white.range_to(black, 130 * floor(settings.MAX_ITER / 1024)))

    palette = (
        palette1
        + palette2
        + palette3
        + palette4
        + palette5
        + palette6
        + palette7
        + palette8
        + palette9
        + palette10
        + palette11
    )

    for item in enumerate(palette):
        r = item[1].rgb[0]
        g = item[1].rgb[1]
        b = item[1].rgb[2]
        return_palette.append([int(r * 255), int(g * 255), int(b * 255)])

    return_palette[settings.MAX_ITER - 1] = (0, 0, 0)
    return return_palette


def colorize_rgb(settings, point_list, *_):
    red = Color("red")
    yellow = Color("yellow")
    green = Color("green")
    cyan = Color("cyan")
    blue = Color("blue")
    violet = Color("violet")
    black = Color("black")
    white = Color("white")

    palette = []
    return_palette = []

    palette1 = list(black.range_to(red, 10 * floor(settings.MAX_ITER / 1024)))
    palette2 = list(red.range_to(yellow, 20 * floor(settings.MAX_ITER / 1024)))
    palette3 = list(yellow.range_to(green, 40 * floor(settings.MAX_ITER / 1024)))
    palette4 = list(green.range_to(cyan, 40 * floor(settings.MAX_ITER / 1024)))
    palette5 = list(cyan.range_to(blue, 80 * floor(settings.MAX_ITER / 1024)))
    palette6 = list(blue.range_to(violet, 80 * floor(settings.MAX_ITER / 1024)))
    palette7 = list(violet.range_to(red, 80 * floor(settings.MAX_ITER / 1024)))
    palette8 = list(red.range_to(yellow, 100 * floor(settings.MAX_ITER / 1024)))
    palette9 = list(yellow.range_to(green, 100 * floor(settings.MAX_ITER / 1024)))
    palette10 = list(green.range_to(cyan, 100 * floor(settings.MAX_ITER / 1024)))
    palette11 = list(cyan.range_to(blue, 100 * floor(settings.MAX_ITER / 1024)))
    palette12 = list(blue.range_to(violet, 100 * floor(settings.MAX_ITER / 1024)))
    palette13 = list(violet.range_to(white, 1000 * floor(settings.MAX_ITER / 1024)))

    palette = (
        palette1
        + palette2
        + palette3
        + palette4
        + palette5
        + palette6
        + palette7
        + palette8
        + palette9
        + palette10
        + palette11
        + palette12
        + palette13
    )

    for item in enumerate(palette):
        r = item[1].rgb[0]
        g = item[1].rgb[1]
        b = item[1].rgb[2]
        return_palette.append([int(r * 255), int(g * 255), int(b * 255)])

    return_palette[settings.MAX_ITER - 1] = (0, 0, 0)
    return return_palette
