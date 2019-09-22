""" Fractal Equations """

import logging
from pprint import pprint
from datetime import datetime
from math import log
from numba import jit
import time


from multiprocessing import Process, Queue


def mandelbrot_parallel(settings):
    start = datetime.now()
    point_list = []
        
    start = datetime.now()

    results_1 = Queue()
    results_2 = Queue()
    process_1 = Process(target=calculate_mandelbrot_1, args=(settings, results_1))
    process_2 = Process(target=calculate_mandelbrot_2, args=(settings, results_2))

    print(f"starting process 1")
    process_1.start()
    print(f"starting process 2")
    process_2.start()

    time.sleep(.2)

    while results_1.qsize() > 0 or results_2.qsize() > 0:
        while results_1.qsize() > 0:
            point_list.extend(results_1.get())
        while results_2.qsize() > 0:
            point_list.extend(results_2.get())
        # time.sleep(.01)


    print(f"joining process 1")
    process_1.join()
    print(f"joining process 2")
    process_2.join()
    print(f"total time: {datetime.now() - start}")
    # print(process_2)
    # print(f"queue: {results_2.get()}")
    # pprint(point_list_1)
    return point_list


def calculate_mandelbrot_1(settings, results_1):
    for x in range(0, settings.SCREEN_WIDTH, 2):
        point_list = []
        for y in range(0, settings.SCREEN_HEIGHT):
            c = complex(
                (settings.RE_START + (x / settings.SCREEN_WIDTH) * (settings.RE_END - settings.RE_START)),
                (settings.IM_START + (y / settings.SCREEN_HEIGHT) * (settings.IM_END - settings.IM_START)),
            )

            m = iterate_mandelbrot(settings.MAX_ITER, c)
            point_list.append([x, y, m])

        results_1.put(point_list)


def calculate_mandelbrot_2(settings, results_2):
    for x in range(1, settings.SCREEN_WIDTH, 2):
        point_list = []

        for y in range(0, settings.SCREEN_HEIGHT):
            c = complex(
                (settings.RE_START + (x / settings.SCREEN_WIDTH) * (settings.RE_END - settings.RE_START)),
                (settings.IM_START + (y / settings.SCREEN_HEIGHT) * (settings.IM_END - settings.IM_START)),
            )

            m = iterate_mandelbrot(settings.MAX_ITER, c)
            point_list.append([x, y, m])

        results_2.put(point_list)


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


# @jit(nopython=True)
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
