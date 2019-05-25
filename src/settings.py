class Settings:
    """ Settings for fractals """

    def __init__(self):

        # Mandelbrot iterations
        self.MAX_ITER = 128

        # Screen settings
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 768
        self.WIDTH = self.SCREEN_WIDTH
        self.HEIGHT = self.SCREEN_WIDTH
        self.RATIO = self.SCREEN_HEIGHT / self.SCREEN_WIDTH
        self.SCREEN = None

        self.COLOR_ALGORITHM = "ce.colorize_rgb"
        self.FRACTAL_ALGORITHM = "fe.mandelbrot"

        # Color settings for colorize_hue and colorized_hue_shifted
        # 0. = Violet              .5 = Green
        # .1 = Pink                .6 = Green - Blue
        # .2 = Red                 .7 = Light Blue
        # .3 = Orange - Red        .8 = Blue
        # .4 = Yellow - Green      .9 = Blue - Purple
        self.HUE_SEED = 0

        # Setting for colorized_hue_shifted
        self.SHIFT = 10

        # Plot window settings
        self.RE_START = -2
        self.RE_END = 1
        self.IM_START = -(((self.RE_END - self.RE_START) * self.RATIO) / 2)
        self.IM_END = ((self.RE_END - self.RE_START) * self.RATIO) / 2

        # Point history
        self.history = []

        # Mouse zoom
        self.MWHEEL_ZOOM = .1

        # Interesting Julia Values
        julia_values = ((0.4, 0.3), (0.3, 0.2), (0.35, 0.4))
        self.C_1 = julia_values[0][0]
        self.C_2 = julia_values[0][1]
