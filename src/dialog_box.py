#!/usr/bin/python3
""" TKinter Dialog box to change settings """
#pylint: disable=W0614, W0401

from pygame import display
from tkinter import Frame, Label, Entry, Tk, StringVar, TOP, X, LEFT, RIGHT, YES, Button, OptionMenu

# This is for testing outside of execution
# from settings import Settings


def construct_dialog_box(settings):
    root = Tk()
    entries = makeform(root, settings)
    b1 = Button(root, text="Save", command=(lambda e=entries: update(settings, e)))
    b1.pack(side=LEFT, padx=5, pady=5)
    b2 = Button(root, text="Close", command=root.destroy)
    b2.pack(side=LEFT, padx=5, pady=5)
    root.mainloop()
    return 0


def makeform(root, settings):
    """ Construct the dialog box """
    fields = ["Iterations >= 64", "Hue Seed", "Color Shift", "Screen Width", "Screen Height", "Julia C_1", "Julis C_2", "Color Algorithm", "fractal algorithm"]
    color_alg = ["ce.colorize_hue", "ce.colorize_hue_shifted", "ce.colorize_hue2", "ce.colorize_blue_green_sin", "ce.colorize_blue_green_gold", "ce.colorize_blue_green_gold", "ce.colorize_white_shift", "ce.colorize_black_gold", "ce.colorize_white_green_black", "ce.colorize_rgb", "ce.colorize_blue_gold", "ce.colorize_color_black", "ce.colorize_color_black2"]
    fractal_alg = ["fe.mandelbrot", "fe.julia"]
    entries = []

    row = Frame(root)
    label = Label(row, width=18, text=fields[0], anchor="w")
    value = StringVar(row, value=settings.MAX_ITER)
    entry = Entry(row, textvariable=value)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    label.pack(side=LEFT)
    entry.pack(side=RIGHT, expand=YES, fill=X)
    entries.append((fields[0], entry))

    row = Frame(root)
    label = Label(row, width=18, text=fields[1], anchor="w")
    value = StringVar(row, value=settings.HUE_SEED)
    entry = Entry(row, textvariable=value)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    label.pack(side=LEFT)
    entry.pack(side=RIGHT, expand=YES, fill=X)
    entries.append((fields[1], entry))

    row = Frame(root)
    label = Label(row, width=18, text=fields[2], anchor="w")
    value = StringVar(row, value=settings.SHIFT)
    entry = Entry(row, textvariable=value)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    label.pack(side=LEFT)
    entry.pack(side=RIGHT, expand=YES, fill=X)
    entries.append((fields[2], entry))

    row = Frame(root)
    label = Label(row, width=18, text=fields[3], anchor="w")
    value = StringVar(row, value=settings.SCREEN_WIDTH)
    entry = Entry(row, textvariable=value)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    label.pack(side=LEFT)
    entry.pack(side=RIGHT, expand=YES, fill=X)
    entries.append((fields[3], entry))

    row = Frame(root)
    label = Label(row, width=18, text=fields[4], anchor="w")
    value = StringVar(row, value=settings.SCREEN_HEIGHT)
    entry = Entry(row, textvariable=value)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    label.pack(side=LEFT)
    entry.pack(side=RIGHT, expand=YES, fill=X)
    entries.append((fields[4], entry))

    row = Frame(root)
    label = Label(row, width=18, text=fields[5], anchor="w")
    value = StringVar(row, value=settings.C_1)
    entry = Entry(row, textvariable=value)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    label.pack(side=LEFT)
    entry.pack(side=RIGHT, expand=YES, fill=X)
    entries.append((fields[5], entry))

    row = Frame(root)
    label = Label(row, width=18, text=fields[6], anchor="w")
    value = StringVar(row, value=settings.C_2)
    entry = Entry(row, textvariable=value)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    label.pack(side=LEFT)
    entry.pack(side=RIGHT, expand=YES, fill=X)
    entries.append((fields[6], entry))



    row = Frame(root)
    label = Label(row, width=18, text=fields[7], anchor="w")
    variable = StringVar(root)
    variable.set(settings.COLOR_ALGORITHM)
    color_equation = OptionMenu(row, variable, *color_alg)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    label.pack(side=LEFT)
    color_equation.pack(side=RIGHT, expand=YES, fill=X)
    entries.append((fields[7], variable))

    row = Frame(root)
    label = Label(row, width=18, text=fields[8], anchor="w")
    variable = StringVar(root)
    variable.set(settings.FRACTAL_ALGORITHM)
    color_equation = OptionMenu(row, variable, *fractal_alg)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    label.pack(side=LEFT)
    color_equation.pack(side=RIGHT, expand=YES, fill=X)
    entries.append((fields[8], variable))

    return entries


def update(settings, entries):
    """ Update settings """
    old_ratio = settings.SCREEN_HEIGHT / settings.SCREEN_WIDTH

    settings.MAX_ITER = int(entries[0][1].get()) if int(entries[0][1].get()) >= 64 else 64
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
        delta = (new_ratio - old_ratio) / 2
        settings.IM_END = settings.IM_END + ((settings.IM_END - settings.IM_START) * delta)
        settings.IM_START = settings.IM_START - ((settings.IM_END - settings.IM_START) * delta)

    settings.SCREEN = display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    settings.C_1 = float(entries[5][1].get())
    settings.C_2 = float(entries[6][1].get())

    settings.COLOR_ALGORITHM = entries[7][1].get()
    settings.FRACTAL_ALGORITHM = entries[8][1].get()

def main():
    """ Main, just used for testing """
    #pylint: disable= E0602, W0612
    root = Tk()
    settings = Settings()
    entries = makeform(root, ["Iterations", "Hue Seed", "Color Shift"], settings)
    root.mainloop()


if __name__ == "__main__":
    main()
