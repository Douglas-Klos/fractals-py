""" Color functions for fractals """
#pylint: disable=E0401, E0402, C0103, W0611, R0914

from colorsys import hsv_to_rgb
from math import sin, cos, floor, sqrt
import pygame
from numba import jit
from .color import Color


def colorize_hue(settings, point_list, *_):
    """ Calculate hue color palette """
    palette = [0] * settings.MAX_ITER
    hues = []

    for point in point_list:
        hues.append(floor(point[2]))

    min_val = min(set(hues))

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
    """ Calculate hue color palette shifted """
    palette = [0] * settings.MAX_ITER
    hues = []

    for point in point_list:
        hues.append(floor(point[2]))

    min_val = min(set(hues))

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


def colorize_blue_green_sin(settings, *_):
    """ Calculate sin color palette """
    palette = [0] * settings.MAX_ITER

    for i in range(settings.MAX_ITER):
        hue = 0.5 + 0.1 * (cos(i / (settings.MAX_ITER / 8)))
        sat = 0.5 + sin((settings.MAX_ITER / (settings.MAX_ITER ** 2)) * i)
        val = 0.5 + 0.5 * (sin(i / 64)) if i < settings.MAX_ITER - 1 else 0

        # print(f"hue:{hue}, sat:{sat}, val:{val}")
        r, g, b = hsv_to_rgb(hue, sat, val)
        palette[i] = [int(r * 255), int(g * 255), int(b * 255)]

    palette[settings.MAX_ITER - 1] = hsv_to_rgb(0, 0, 0)
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


def colorize_blue_green_gold(settings, *_):
    """ Predefined blue - green - gold color palette """
    gold = Color("gold")
    blue = Color("blue")
    black = Color("black")
    white = Color("white")

    palette = []
    return_palette = []

    palette += list(black.range_to(blue, 10 * floor(settings.MAX_ITER / 1024)))
    palette += list(blue.range_to(white, 20 * floor(settings.MAX_ITER / 1024)))
    palette += list(white.range_to(gold, 40 * floor(settings.MAX_ITER / 1024)))
    palette += list(gold.range_to(black, 40 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(blue, 80 * floor(settings.MAX_ITER / 1024)))
    palette += list(blue.range_to(white, 80 * floor(settings.MAX_ITER / 1024)))
    palette += list(white.range_to(gold, 80 * floor(settings.MAX_ITER / 1024)))
    palette += list(gold.range_to(black, 100 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(blue, 100 * floor(settings.MAX_ITER / 1024)))
    palette += list(blue.range_to(white, 100 * floor(settings.MAX_ITER / 1024)))
    palette += list(white.range_to(gold, 100 * floor(settings.MAX_ITER / 1024)))
    palette += list(gold.range_to(black, 100 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(white, 200 * floor(settings.MAX_ITER / 1024)))

    for item in enumerate(palette):
        r = item[1].rgb[0]
        g = item[1].rgb[1]
        b = item[1].rgb[2]
        return_palette.append([int(r * 255), int(g * 255), int(b * 255)])

    return_palette[settings.MAX_ITER - 1] = (0, 0, 0)
    return return_palette


def colorize_black_shift(settings, *_):
    """ Predefined black - color rainbow palette """
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

    palette += list(black.range_to(violet, 10 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(red, 20 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(yellow, 4 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(green, 40 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(cyan, 80 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(blue, 80 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(violet, 80 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(red, 100 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(yellow, 100 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(green, 100 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(cyan, 100 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(blue, 100 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(white, 250 * floor(settings.MAX_ITER / 1024)))

    for item in enumerate(palette):
        r = item[1].rgb[0]
        g = item[1].rgb[1]
        b = item[1].rgb[2]
        return_palette.append([int(r * 255), int(g * 255), int(b * 255)])

    return_palette[settings.MAX_ITER - 1] = (0, 0, 0)
    return return_palette


def colorize_white_shift(settings, *_):
    """ Predefined white - color rainbow palette """
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

    palette += list(white.range_to(violet, 10 * floor(settings.MAX_ITER / 1024)))
    palette += list(white.range_to(red, 20 * floor(settings.MAX_ITER / 1024)))
    palette += list(white.range_to(yellow, 4 * floor(settings.MAX_ITER / 1024)))
    palette += list(white.range_to(green, 40 * floor(settings.MAX_ITER / 1024)))
    palette += list(white.range_to(cyan, 80 * floor(settings.MAX_ITER / 1024)))
    palette += list(white.range_to(blue, 80 * floor(settings.MAX_ITER / 1024)))
    palette += list(white.range_to(violet, 80 * floor(settings.MAX_ITER / 1024)))
    palette += list(white.range_to(red, 100 * floor(settings.MAX_ITER / 1024)))
    palette += list(white.range_to(yellow, 100 * floor(settings.MAX_ITER / 1024)))
    palette += list(white.range_to(green, 100 * floor(settings.MAX_ITER / 1024)))
    palette += list(white.range_to(cyan, 100 * floor(settings.MAX_ITER / 1024)))
    palette += list(white.range_to(blue, 100 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(white, 250 * floor(settings.MAX_ITER / 1024)))

    for item in enumerate(palette):
        r = item[1].rgb[0]
        g = item[1].rgb[1]
        b = item[1].rgb[2]
        return_palette.append([int(r * 255), int(g * 255), int(b * 255)])

    return_palette[settings.MAX_ITER - 1] = (0, 0, 0)
    return return_palette


def colorize_black_gold(settings, *_):
    """ Predefined black and gold color palette """
    gold = Color("gold")
    black = Color("black")
    palette = []
    return_palette = []
    palette += list(gold.range_to(black, 10 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(gold, 20 * floor(settings.MAX_ITER / 1024)))
    palette += list(gold.range_to(black, 60 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(gold, 60 * floor(settings.MAX_ITER / 1024)))
    palette += list(gold.range_to(black, 60 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(gold, 60 * floor(settings.MAX_ITER / 1024)))
    palette += list(gold.range_to(black, 60 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(gold, 60 * floor(settings.MAX_ITER / 1024)))
    palette += list(gold.range_to(black, 60 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(gold, 444 * floor(settings.MAX_ITER / 1024)))
    palette += list(gold.range_to(black, 1000 * floor(settings.MAX_ITER / 1024)))

    for item in enumerate(palette):
        r = item[1].rgb[0]
        g = item[1].rgb[1]
        b = item[1].rgb[2]
        return_palette.append([int(r * 255), int(g * 255), int(b * 255)])

    return_palette[settings.MAX_ITER - 1] = (0, 0, 0)
    return return_palette


def colorize_white_green_black(settings, *_):
    """ Predefined white - green - black color palette """
    black = Color("black")
    white = Color("white")
    green = Color("green")
    palette = []
    return_palette = []
    palette += list(white.range_to(green, 10 * floor(settings.MAX_ITER / 1024)))
    palette += list(green.range_to(black, 20 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(green, 60 * floor(settings.MAX_ITER / 1024)))
    palette += list(green.range_to(white, 60 * floor(settings.MAX_ITER / 1024)))
    palette += list(white.range_to(green, 60 * floor(settings.MAX_ITER / 1024)))
    palette += list(green.range_to(white, 60 * floor(settings.MAX_ITER / 1024)))
    palette += list(white.range_to(green, 60 * floor(settings.MAX_ITER / 1024)))
    palette += list(green.range_to(black, 60 * floor(settings.MAX_ITER / 1024)))
    palette += list(black.range_to(green, 60 * floor(settings.MAX_ITER / 1024)))
    palette += list(green.range_to(white, 444 * floor(settings.MAX_ITER / 1024)))
    palette += list(white.range_to(black, 130 * floor(settings.MAX_ITER / 1024)))

    for item in enumerate(palette):
        r = item[1].rgb[0]
        g = item[1].rgb[1]
        b = item[1].rgb[2]
        return_palette.append([int(r * 255), int(g * 255), int(b * 255)])

    return_palette[settings.MAX_ITER - 1] = (0, 0, 0)
    return return_palette


def colorize_rgb(settings, *_):
    """ Predefined RGB / rainbow color palette """
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

    palette += list(black.range_to(red, 10 * floor(settings.MAX_ITER / 1024)))
    palette += list(red.range_to(yellow, 20 * floor(settings.MAX_ITER / 1024)))
    palette += list(yellow.range_to(green, 40 * floor(settings.MAX_ITER / 1024)))
    palette += list(green.range_to(cyan, 40 * floor(settings.MAX_ITER / 1024)))
    palette += list(cyan.range_to(blue, 80 * floor(settings.MAX_ITER / 1024)))
    palette += list(blue.range_to(violet, 80 * floor(settings.MAX_ITER / 1024)))
    palette += list(violet.range_to(red, 80 * floor(settings.MAX_ITER / 1024)))
    palette += list(red.range_to(yellow, 100 * floor(settings.MAX_ITER / 1024)))
    palette += list(yellow.range_to(green, 100 * floor(settings.MAX_ITER / 1024)))
    palette += list(green.range_to(cyan, 100 * floor(settings.MAX_ITER / 1024)))
    palette += list(cyan.range_to(blue, 100 * floor(settings.MAX_ITER / 1024)))
    palette += list(blue.range_to(violet, 100 * floor(settings.MAX_ITER / 1024)))
    palette += list(violet.range_to(white, 1000 * floor(settings.MAX_ITER / 1024)))

    for item in enumerate(palette):
        r = item[1].rgb[0]
        g = item[1].rgb[1]
        b = item[1].rgb[2]
        return_palette.append([int(r * 255), int(g * 255), int(b * 255)])

    return_palette[settings.MAX_ITER - 1] = (0, 0, 0)
    return return_palette


def colorize_blue_gold(settings, *_):
    """ Predefined blue and gold color palette """
    gold = Color("gold")
    black = Color("black")
    white = Color("white")
    palette = []
    return_palette = []

    palette += black_to_blue(10 * floor(settings.MAX_ITER / 1024))
    palette += blue_to_black(30 * floor(settings.MAX_ITER / 1024))
    palette += list(black.range_to(gold, 60 * floor(settings.MAX_ITER / 1024)))
    palette += list(gold.range_to(black, 100 * floor(settings.MAX_ITER / 1024)))
    palette += black_to_blue(100 * floor(settings.MAX_ITER / 1024))
    palette += blue_to_black(100 * floor(settings.MAX_ITER / 1024))
    palette += list(black.range_to(gold, 100 * floor(settings.MAX_ITER / 1024)))
    palette += list(gold.range_to(black, 100 * floor(settings.MAX_ITER / 1024)))
    palette += black_to_blue(100 * floor(settings.MAX_ITER / 1024))
    palette += blue_to_black(100 * floor(settings.MAX_ITER / 1024))
    palette += list(black.range_to(white, 400 * floor(settings.MAX_ITER / 1024)))

    for item in enumerate(palette):
        try:
            r = item[1].rgb[0]
            g = item[1].rgb[1]
            b = item[1].rgb[2]
        except AttributeError:
            # print(f"item:{item}")
            r = item[1][0]/255
            g = item[1][1]/255
            b = item[1][2]/255
        finally:
            return_palette.append([int(r * 255), int(g * 255), int(b * 255)])

    return_palette[settings.MAX_ITER - 1] = (0, 0, 0)
    # print(f"palette:{return_palette}")
    return return_palette


# The black to blue and blue to black color shifts in the Color package
#   do not operate as expected, it would always pass through green.
#   Decided to code my own blue to black shift functions.
def blue_to_black(span):
    """ Colour package blue.range_to(black) gives incorrect result """
    return [[0, 0, floor(x * (256/span))] for x in reversed(range(span))]

def black_to_blue(span):
    """ Colour package black.range_to(blue) gives incorrect result """
    return [[0, 0, floor(x * (256/span))] for x in range(span)]
