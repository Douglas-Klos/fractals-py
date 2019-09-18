""" Fractal Equations """
# pylint: disable=C0330, C0103, R0913

from datetime import datetime
from math import log
from numba import jit


@jit(nopython=True)
def iterate_mandelbrot(MAX_ITER, c, z=0):
    """ Iterate the mandelbrot function """
    n = 0
    while abs(z) <= 2 and n < MAX_ITER:
        z = z * z + c
        n += 1

    if n == MAX_ITER:
        return MAX_ITER - 1

    return n + 1 - log(log(abs(z) / log(2)))


def mandelbrot(settings):
    """ Mandelbrot sequence """
    start = datetime.now()
    point_list = []

    # We're wrapping calculate_mandelbrot so we can jit it.
    for point in calculate_mandelbrot(
        settings.SCREEN_WIDTH,
        settings.SCREEN_HEIGHT,
        settings.RE_START,
        settings.RE_END,
        settings.IM_START,
        settings.IM_END,
        settings.MAX_ITER,
    ):
        if point[1] % 1000 == 0:
            print(
                f"Calculating Fractal: {((point[0] / settings.SCREEN_WIDTH) * 100):0.2f} % complete  ",
                end="\r",
            )
        point_list.append(point)

    print(f"Calculating Fractal: 100.00% complete - Time:{datetime.now()-start}")
    return point_list


@jit(nopython=True)
def calculate_mandelbrot(width, height, re_start, re_end, im_start, im_end, max_iter):
    """ Calculate mandelbrot for our screen size """
    for x in range(0, width):
        for y in range(0, height):
            c = complex(
                (re_start + (x / width) * (re_end - re_start)),
                (im_start + (y / height) * (im_end - im_start)),
            )

            m = iterate_mandelbrot(max_iter, c)
            yield x, y, m


def julia(settings):
    """ Mandelbrot sequence """
    start = datetime.now()
    point_list = []

    # We're wrapping calculate_mandelbrot so we can jit it.
    for point in calculate_julia(
        settings.SCREEN_WIDTH,
        settings.SCREEN_HEIGHT,
        settings.RE_START,
        settings.RE_END,
        settings.IM_START,
        settings.IM_END,
        settings.MAX_ITER,
        settings.C_1,
        settings.C_2,
    ):
        if point[1] % 1000 == 0:
            print(
                f"Calculating Fractal: {((point[0] / settings.SCREEN_WIDTH) * 100):0.2f} % complete  ",
                end="\r",
            )
        point_list.append(point)

    print(f"Calculating Fractal: 100.00% complete - Time:{datetime.now()-start}")
    return point_list


@jit(nopython=True)
def calculate_julia(
    width, height, re_start, re_end, im_start, im_end, max_iter, C_1, C_2
):
    """ Julia sequence for our screen size """
    for x in range(0, width):
        for y in range(0, height):
            c = complex(
                (re_start + (x / width) * (re_end - re_start)),
                (im_start + (y / height) * (im_end - im_start)),
            )

            m = iterate_mandelbrot(max_iter, complex(C_1, C_2), c)
            yield x, y, m
