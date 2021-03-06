#!/usr/bin/env python3
""" TKinter Dialog box to change settings """

from math import floor
from tkinter import (
    Frame,
    Label,
    Entry,
    Tk,
    StringVar,
    TOP,
    X,
    LEFT,
    RIGHT,
    YES,
    Button,
    OptionMenu,
)
from pygame import display


def construct_dialog_box(settings):
    root = Tk()
    entries = makeform(root, settings)

    save_button = Button(
        root, text="Save", command=(lambda e=entries: update(settings, e))
    )
    save_button.pack(side=LEFT, padx=5, pady=5)

    close_botton = Button(root, text="Close", command=root.destroy)
    close_botton.pack(side=LEFT, padx=5, pady=5)

    root.mainloop()


def makeform(root, settings):
    """ Adds fields the dialog box """
    fields = (
        ("Iterations >= 64", settings.MAX_ITER),  # 0
        ("Hue Seed", settings.HUE_SEED),  # 1
        ("Color Shift", settings.SHIFT),  # 2
        ("Screen Width", settings.SCREEN_WIDTH),  # 3
        ("Screen Height", settings.SCREEN_HEIGHT),  # 4
        ("Julia C_1", settings.C_1),  # 5
        ("Julis C_2", settings.C_2),  # 6
        ("Roll R", settings.ROLL_R),  # 7
        ("Roll G", settings.ROLL_G),  # 8
        ("Roll B", settings.ROLL_B),  # 9
        ("Color Algorithm", settings.COLOR_ALGORITHM),  # 10
        ("Fractal Algorithm", settings.FRACTAL_ALGORITHM),  # 11
    )

    entries = []

    for counter, field in enumerate(fields):
        row = Frame(root)
        label = Label(row, width=18, text=field[0], anchor="w")
        if counter < 10:
            value = StringVar(row, value=field[1])
            entry = Entry(row, textvariable=value)
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            label.pack(side=LEFT)
            entry.pack(side=RIGHT, expand=YES, fill=X)
            entries.append((field, entry))

        else:
            variable = StringVar(root)
            variable.set(field[1])

            if counter == 10:  # Color Algorithms
                equation = OptionMenu(row, variable, *settings.color_alg.keys())
            elif counter == 11:  # Fractal Algorithms
                equation = OptionMenu(row, variable, *settings.fractal_alg.keys())
            row.pack(side=TOP, fill=X, padx=5, pady=5)
            label.pack(side=LEFT)
            equation.pack(side=RIGHT, expand=YES, fill=X)
            entries.append((fields[10], variable))

    return entries


def update(settings, entries):
    """ Update settings """
    if (
            settings.MAX_ITER != int(entries[0][1].get()) or
            settings.SCREEN_WIDTH != int(entries[3][1].get()) or
            settings.SCREEN_HEIGHT != int(entries[4][1].get()) or
            settings.C_1 != float(entries[5][1].get()) or
            settings.C_2 != float(entries[6][1].get()) or
            settings.FRACTAL_ALGORITHM != entries[11][1].get()
    ):
        settings.DRAW = True

    if (
            settings.MAX_ITER != int(entries[0][1].get()) or
            settings.HUE_SEED != float(entries[1][1].get()) or
            settings.SHIFT != int(entries[2][1].get()) or
            settings.ROLL_R != int(entries[7][1].get()) or
            settings.ROLL_G != int(entries[8][1].get()) or
            settings.ROLL_B != int(entries[9][1].get()) or
            settings.COLOR_ALGORITHM != entries[10][1].get()
    ):
        settings.COLOR = True

    settings.MAX_ITER = (
        int(entries[0][1].get()) if int(entries[0][1].get()) >= 64 else 64
    )
    settings.HUE_SEED = float(entries[1][1].get())
    settings.SHIFT = int(entries[2][1].get())

    adjust_edges(settings, entries)

    settings.SCREEN = display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
    settings.C_1 = float(entries[5][1].get())
    settings.C_2 = float(entries[6][1].get())
    settings.ROLL_R = floor(float(entries[7][1].get()))
    settings.ROLL_G = floor(float(entries[8][1].get()))
    settings.ROLL_B = floor(float(entries[9][1].get()))
    settings.COLOR_ALGORITHM = entries[10][1].get()
    settings.FRACTAL_ALGORITHM = entries[11][1].get()


def adjust_edges(settings, entries):
    """
        Adjusts the RE and IM values to correct for the new screen resolution.

        If the screen height has changed:
            Real values are left unchaged.
            Imaginary values are adjusted based on the new screen height.

        If the screen width has changed:
            Imaginary values are left unchanged.
            Real values are adjusted based on the new screen width.

        If both are changed, first the imaginary then real are updated.
            This has the effect of increasing the area to be rendered instead
                of scaling the current RM and IM values.
    """
    if settings.SCREEN_HEIGHT != int(entries[4][1].get()):
        im_middle = mid_point(0, 0, settings.IM_START, settings.IM_END)
        adjustment = (
            (settings.RE_END - settings.RE_START) *
            int(entries[4][1].get()) /
            settings.SCREEN_WIDTH /
            2
        )
        settings.IM_START = im_middle[1] - adjustment
        settings.IM_END = im_middle[1] + adjustment
        settings.SCREEN_HEIGHT = int(entries[4][1].get())

    if settings.SCREEN_WIDTH != int(entries[3][1].get()):
        re_middle = mid_point(settings.RE_START, settings.RE_END, 0, 0)
        adjustment = (
            (settings.IM_END - settings.IM_START) *
            int(entries[3][1].get()) /
            settings.SCREEN_HEIGHT /
            2
        )
        settings.RE_START = re_middle[0] - adjustment
        settings.RE_END = re_middle[0] + adjustment
        settings.SCREEN_WIDTH = int(entries[3][1].get())


def mid_point(x1, x2, y1, y2):
    return ((x1 + x2) / 2, (y1 + y2) / 2)


def main():
    """ Main, just used for testing """
    from settings import Settings

    root = Tk()
    settings = Settings()
    entries = makeform(root, settings)
    save_button = Button(
        root, text="Save", command=(lambda e=entries: update(settings, e))
    )
    save_button.pack(side=LEFT, padx=5, pady=5)
    close_botton = Button(root, text="Close", command=root.destroy)
    close_botton.pack(side=LEFT, padx=5, pady=5)
    root.mainloop()


if __name__ == "__main__":
    main()
