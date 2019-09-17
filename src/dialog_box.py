#!/usr/bin/env python3
""" TKinter Dialog box to change settings """
# pylint: disable=W0614, W0401

from math import floor
from pygame import display
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

# This is for testing outside of execution
# from settings import Settings


def construct_dialog_box(settings):
    settings.DRAW = False
    settings.COLOR = False

    root = Tk()
    entries = makeform(root, settings)

    save_button = Button(root, text="Save", command=(lambda e=entries: update(settings, e)))
    save_button.pack(side=LEFT, padx=5, pady=5)

    close_botton = Button(root, text="Close", command=root.destroy)
    close_botton.pack(side=LEFT, padx=5, pady=5)

    root.mainloop()

    return


def makeform(root, settings):
    """ Construct the dialog box """
    fields = (
        ("Iterations >= 64", settings.MAX_ITER),
        ("Hue Seed", settings.HUE_SEED),
        ("Color Shift", settings.SHIFT),
        ("Screen Width", settings.SCREEN_WIDTH),
        ("Screen Height", settings.SCREEN_HEIGHT),
        ("Julia C_1", settings.C_1),
        ("Julis C_2", settings.C_2),
        ("Roll R", settings.ROLL_R),
        ("Rolls G", settings.ROLL_G),
        ("Roll B", settings.ROLL_B),
        ("Color Algorithm", settings.COLOR_ALGORITHM),
        ("Fractal Algorithm", settings.FRACTAL_ALGORITHM),
    )

    entries = []

    for counter, field in enumerate(fields):
        row = Frame(root)
        label = Label(row, width=18, text=field[0], anchor='w')
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
    settings.DRAW = False
    settings.COLOR = False

    if (
        settings.MAX_ITER != int(entries[0][1].get())
        or settings.C_1 != float(entries[5][1].get())
        or settings.C_2 != float(entries[6][1].get())
    ):
        settings.DRAW = True

    old_ratio = settings.SCREEN_HEIGHT / settings.SCREEN_WIDTH

    settings.MAX_ITER = (
        int(entries[0][1].get()) if int(entries[0][1].get()) >= 64 else 64
    )
    settings.HUE_SEED = float(entries[1][1].get())
    settings.SHIFT = int(entries[2][1].get())
    settings.SCREEN_WIDTH = int(entries[3][1].get())
    settings.SCREEN_HEIGHT = int(entries[4][1].get())
    settings.WIDTH = int(entries[3][1].get())
    settings.HEIGHT = int(entries[4][1].get())

    new_ratio = settings.SCREEN_HEIGHT / settings.SCREEN_WIDTH
    settings.RATIO = settings.SCREEN_HEIGHT / settings.SCREEN_WIDTH

    # print(f"old_ratio:{old_ratio}")
    # print(f"new_ratio:{new_ratio}")
    if old_ratio != new_ratio:
        settings.DRAW = True
        delta = (new_ratio - old_ratio) / 2
        settings.IM_END = settings.IM_END + (
            (settings.IM_END - settings.IM_START) * delta
        )
        settings.IM_START = settings.IM_START - (
            (settings.IM_END - settings.IM_START) * delta
        )

    settings.SCREEN = display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    settings.C_1 = float(entries[5][1].get())
    settings.C_2 = float(entries[6][1].get())

    settings.ROLL_R = floor(float(entries[7][1].get()))
    settings.ROLL_G = floor(float(entries[8][1].get()))
    settings.ROLL_B = floor(float(entries[9][1].get()))

    if (settings.COLOR_ALGORITHM != entries[10][1].get()):
        settings.COLOR_ALGORITHM = entries[10][1].get()
        settings.COLOR = True

    if (settings.FRACTAL_ALGORITHM != entries[11][1].get()):
        settings.FRACTAL_ALGORITHM = entries[11][1].get()
        settings.DRAW = True

    # print(settings.COLOR_ALGORITHM)
    # print(settings.FRACTAL_ALGORITHM)


def main():
    """ Main, just used for testing """

    import fractal_equations as fe
    import color_equations as ce

    root = Tk()

    # Initialize settings object
    settings = Settings()
    entries = makeform(root, settings)

    save_button = Button(root, text="Save", command=(lambda e=entries: update(settings, e)))
    save_button.pack(side=LEFT, padx=5, pady=5)

    close_botton = Button(root, text="Close", command=root.destroy)
    close_botton.pack(side=LEFT, padx=5, pady=5)

    root.mainloop()


if __name__ == "__main__":
    main()
