""" Fractal Equations """
# pylint: disable=C0111, C0103, C0301

from datetime import datetime
from math import log
from numba import jit


@jit(nopython=True)
def iterate_mandelbrot(MAX_ITER, c, z=0):
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z * z + c
        n += 1

    if n == MAX_ITER:
        return MAX_ITER - 1

    return n + 1 - log(log(abs(z) / log(2)))


def mandelbrot(settings):
    """ Mandelbrot sequence """
    SCALE = 1
    CENTER = (0, 0)
    start = datetime.now()
    point_list = []

    for x in range(0, settings.SCREEN_WIDTH):
        for y in range(0, settings.SCREEN_HEIGHT):
            c = complex(
                (
                    settings.RE_START
                    + (x / settings.WIDTH) * (settings.RE_END - settings.RE_START)
                )
                * SCALE
                + CENTER[0],
                (
                    settings.IM_START
                    + (y / settings.HEIGHT) * (settings.IM_END - settings.IM_START)
                )
                * SCALE
                + CENTER[1],
            )

            m = iterate_mandelbrot(settings.MAX_ITER, c)
            point_list.append((x, y, m))
        print(
            f"Calculating Fractal: {((x / settings.SCREEN_WIDTH) * 100):0.2f} % complete  ",
            end="\r",
        )
    print(f"time:{datetime.now()-start}")
    return point_list


def julia(settings):
    """ Julia sequence """
    SCALE = 1.4
    CENTER = (0, 0)

    point_list = []

    for x in range(0, settings.SCREEN_WIDTH):
        for y in range(0, settings.SCREEN_HEIGHT):
            c = complex(
                (
                    settings.RE_START
                    + (x / settings.WIDTH) * (settings.RE_END - settings.RE_START)
                )
                * SCALE
                + CENTER[0],
                (
                    settings.IM_START
                    + (y / settings.HEIGHT) * (settings.IM_END - settings.IM_START)
                )
                * SCALE
                + CENTER[1],
            )
            m = iterate_mandelbrot(
                settings.MAX_ITER, complex(settings.C_1, settings.C_2), c
            )
            point_list.append((x, y, m))
        print(
            f"Calculating Fractal: {((x / settings.SCREEN_WIDTH) * 100):0.2f} % complete  ",
            end="\r",
        )
    return point_list
