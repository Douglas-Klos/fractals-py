""" Color functions for fractals """
# pylint: disable=C0103

import pygame
from colorsys import hsv_to_rgb
from math import sin, cos, log, floor, ceil


def colorize_hue(settings, *_):
    """ Calculate hue color palette """
    palette = [0] * settings.MAX_ITER

    for i in range(settings.MAX_ITER):
        f = 1 - abs(
            (float(i) / settings.MAX_ITER - 1)
            ** (settings.MAX_ITER / 32)
        )

        hue = 0.66 + f / 3
        sat = 1 - f
        val = f if i < settings.MAX_ITER - 1 else 0

        # print(f"f:{f}, hue:{hue}, sat:{sat}, val:{val}")

        r, g, b = hsv_to_rgb(hue, sat, val)
        palette[i] = (int(r * 255), int(g * 255), int(b * 255))

    return palette


def colorize_hue_shifted(settings, point_list, *_):
    hues = []
    val_count = 0
    for point in point_list:
        hues.append(floor(point[2]))

    min_val = min(set(hues))

    palette = [0] * settings.MAX_ITER

    for i in range(settings.MAX_ITER):
        hue = 0.7 + (
            1
            - abs(
                ((float(i) - min_val) / settings.MAX_ITER - 1)
                ** (settings.MAX_ITER / 128)
            )
            / 4
        )
        sat = 1 - (
            1
            - abs(
                ((float(i) - min_val) / settings.MAX_ITER - 1)
                ** (settings.MAX_ITER / 128)
            )
        )
        val = (
            abs(1 - abs(((i - min_val - 20) / settings.MAX_ITER) - 1) ** 32)
            if i < settings.MAX_ITER - 1
            else 0
        )

        # print(f"hue:{hue}, sat:{sat}, val:{val}")

        r, g, b = hsv_to_rgb(hue, sat, val)
        palette[i] = (int(r * 255), int(g * 255), int(b * 255))
    
    return palette


def colorize_hue2(settings, *_):
    """ Calculate hue color palette """
    palette = [0] * settings.MAX_ITER

    for i in range(settings.MAX_ITER):
        hue = .46 + (1 - abs((i/(settings.MAX_ITER))-1)**(settings.MAX_ITER / 64) / 3)
        sat = abs(i / settings.MAX_ITER - 1) ** (settings.MAX_ITER / 64)
        val = (
            abs(1 - abs((i / settings.MAX_ITER) - 1.03) ** (256/12))
            if i < settings.MAX_ITER - 1
            else 0
        )

        # print(f"hue:{hue}, sat:{sat}, val:{val}")

        r, g, b = hsv_to_rgb(hue, sat, val)
        palette[i] = (int(r * 255), int(g * 255), int(b * 255))

    return palette


# While these next ones "work", they're certainly not very  aesthetic.

def colorize_log(settings, *_):
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


def colorize_linear(settings, *_):
    """ Calculate linear color palette """
    palette = [0] * settings.MAX_ITER

    for i in range(settings.MAX_ITER):
        r, g, b = hsv_to_rgb(
            i / settings.MAX_ITER, 1, 1 if i < settings.MAX_ITER - 1 else 0
        )
        palette[i] = (int(r * 255), int(g * 255), int(b * 255))

    return palette


def colorize_sin(settings, *_):
    """ Calculate sin color palette """
    palette = [0] * settings.MAX_ITER

    for i in range(settings.MAX_ITER):
        r, g, b = hsv_to_rgb(abs(sin(i)), 1, 1 if i < settings.MAX_ITER - 1 else 0)
        palette[i] = (int(r * 255), int(g * 255), int(b * 255))

    return palette


def colorize_cos(settings, *_):
    """ Calculate cos color palette """
    palette = [0] * settings.MAX_ITER

    for i in range(settings.MAX_ITER):
        r, g, b = hsv_to_rgb(abs(cos(i)), 1, 1 if i < settings.MAX_ITER - 1 else 0)
        palette[i] = (int(r * 255), int(g * 255), int(b * 255))

    return palette


# Work in progress - It's currently conceptual, a mess.
# def colorize_shifting(settings, point_list, screen):
#     hues = []
#     val_count = 0
#     for point in point_list:
#         hues.append(floor(point[2]))

#     min_val = min(set(hues))

#     palette = [0] * settings.MAX_ITER

#     for i in range(settings.MAX_ITER):
#         hue = 0.7 + (
#             1 - abs(((float(i) - min_val) / settings.MAX_ITER - 1) ** (settings.MAX_ITER / 128)) / 4
#         )
#         sat = 1 - (1 - abs(
#             ((float(i) - min_val) / settings.MAX_ITER - 1)
#             ** (settings.MAX_ITER / 128)
#         ))
#         val = (
#             abs(1 - abs(((i - min_val - 8) / settings.MAX_ITER) - 1) ** 32)
#             if i < settings.MAX_ITER - 1
#             else 0
#         )

#         # print(f"hue:{hue}, sat:{sat}, val:{val}")

#         r, g, b = hsv_to_rgb(hue, sat, val)
#         palette[i] = (int(r * 255), int(g * 255), int(b * 255))

#     for j in range(100):

#         val_count += 1
#         if val_count > 10:
#             val_count = 2

#         for point in point_list:
#             screen.set_at((point[0], point[1]), palette[floor(point[2])])

#         pygame.display.flip()

#         for i in range(settings.MAX_ITER):
#             val = (
#                 abs(1 - abs(((i - min_val - val_count) / settings.MAX_ITER) - 1) ** 32)
#                 if i < settings.MAX_ITER - 1
#                 else 0
#             )
#             r, g, b = hsv_to_rgb(hue, sat, val)
#             palette[i] = (int(r * 255), int(g * 255), int(b * 255))

#     return palette
