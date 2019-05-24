#!/usr/bin/python3
""" TKinter Dialog box to change settings """
#pylint: disable=W0614, W0401

import asyncio
from tkinter import Frame, Label, Entry, Tk, StringVar, TOP, X, LEFT, RIGHT, YES, Button

# This is for testing outside of execution
# from settings import Settings


def construct_dialog_box(settings, root):
    entries = makeform(root, ["Iterations", "Hue Seed", "Color Shift"], settings)
    b1 = Button(root, text="Update", command=(lambda e=entries: update(settings, e)))
    b1.pack(side=LEFT, padx=5, pady=5)
    b2 = Button(root, text="Close", command=root.destroy)
    b2.pack(side=LEFT, padx=5, pady=5)
    root.mainloop()
    return 0
    # await


def makeform(root, fields, settings):
    """ Construct the dialog box """
    entries = []

    row = Frame(root)
    label = Label(row, width=15, text=fields[0], anchor="w")
    value = StringVar(row, value=settings.MAX_ITER)
    entry = Entry(row, textvariable=value)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    label.pack(side=LEFT)
    entry.pack(side=RIGHT, expand=YES, fill=X)
    entries.append((fields[0], entry))

    row = Frame(root)
    label = Label(row, width=15, text=fields[1], anchor="w")
    value = StringVar(row, value=settings.HUE_SEED)
    entry = Entry(row, textvariable=value)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    label.pack(side=LEFT)
    entry.pack(side=RIGHT, expand=YES, fill=X)
    entries.append((fields[1], entry))

    row = Frame(root)
    label = Label(row, width=15, text=fields[2], anchor="w")
    value = StringVar(row, value=settings.SHIFT)
    entry = Entry(row, textvariable=value)
    row.pack(side=TOP, fill=X, padx=5, pady=5)
    label.pack(side=LEFT)
    entry.pack(side=RIGHT, expand=YES, fill=X)
    entries.append((fields[2], entry))

    return entries


def update(settings, entries):
    """ Update settings """
    settings.MAX_ITER = int(entries[0][1].get())
    settings.HUE_SEED = float(entries[1][1].get())
    settings.SHIFT = float(entries[2][1].get())


def main():
    """ Main, just used for testing """
    #pylint: disable= E0602, W0612
    root = Tk()
    settings = Settings()
    entries = makeform(root, ["Iterations", "Hue Seed", "Color Shift"], settings)
    root.mainloop()


if __name__ == "__main__":
    main()
