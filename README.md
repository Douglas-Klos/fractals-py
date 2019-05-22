# Fractals in Python

## Interface

Left Mouse Button -  Zoom in on selected area.
   Note: Currently no box is _displayed_ while selecting an area.

Right Mouse Button - Pan the image around.

Center Mouse Button - Reset the image to the original coordinate plane.

Mouse Wheel Up - Zoom in 10%

Mouse Wheel Down - Zoom Out 10%

Q - Quit

### fractal.py

There's a couple lines here you can adjust

```Python
fractal = fe.mandelbrot
colorize = ce.colorize_hue_shifted
```

These are the fractal and coloring algorithms to be used for the run.  You can
try things like:

```Python
fractal = fe.julia
colorize = ce.colorize_hue
```


### settings.py

MAX_ITER = Number of iterations to perform.


## Why though?

This is one of the first programs I've written for personal enrichment.  It's
a work in progress that I'm using to improve my python skills while obtaining
a better understanding of fractals and their algorithms.