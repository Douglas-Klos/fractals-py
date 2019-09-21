import src.fractal_equations as fe
import src.color_equations as ce


class Settings:
    """ Settings for fractals """

    def __init__(self):
        # Lists of available color and fractal algorithms.
        self.color_alg = {
            "ce.colorize_hue": ce.colorize_hue,
            "ce.colorize_hue_shifted": ce.colorize_hue_shifted,
            "ce.colorize_blue_green_sin": ce.colorize_blue_green_sin,
            "ce.colorize_blue_green_gold": ce.colorize_blue_green_gold,
            "ce.colorize_white_shift": ce.colorize_white_shift,
            "ce.colorize_black_gold": ce.colorize_black_gold,
            "ce.colorize_white_green_black": ce.colorize_white_green_black,
            "ce.colorize_rgb": ce.colorize_rgb,
            "ce.colorize_blue_gold": ce.colorize_blue_gold,
            "ce.colorize_color_black": ce.colorize_color_black,
            "ce.colorize_color_black2": ce.colorize_color_black2,
        }
        self.fractal_alg = {
            "fe.mandelbrot": fe.mandelbrot,
            "fe.julia": fe.julia,
        }

        # Default algorithms
        self.COLOR_ALGORITHM = "ce.colorize_color_black2"
        self.FRACTAL_ALGORITHM = "fe.mandelbrot"

        # Mandelbrot iterations
        self.MAX_ITER = 128

        # Screen settings
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 800
        self.SCREEN = None

        # Plot window settings
        self.RE_START = -2
        self.RE_END = 1
        self._im_mid = 0

        # self.RE_START = -1.4853696465081982
        # self.RE_END = -1.4853693374768457

        # self.RE_START = -1.355
        # self.RE_END = -1.1168

        self.IM_START = self._im_mid -(((self.RE_END - self.RE_START) * self.ratio()) / 2)
        self.IM_END = self._im_mid + ((self.RE_END - self.RE_START) * self.ratio()) / 2

        # print(self.IM_START)
        # print(self.IM_END)

        # self.IM_START = -(((self.RE_END - self.RE_START) * self.ratio()) / 2)
        # self.IM_END = ((self.RE_END - self.RE_START) * self.ratio()) / 2

        # Mouse zoom
        self.MWHEEL_ZOOM = .2

        # Color settings for colorize_hue and colorized_hue_shifted
        # 0. = Violet              .5 = Green
        # .1 = Pink                .6 = Green - Blue
        # .2 = Red                 .7 = Light Blue
        # .3 = Orange - Red        .8 = Blue
        # .4 = Yellow - Green      .9 = Blue - Purple
        self.HUE_SEED = 0

        # Setting for colorized_hue_shifted
        self.SHIFT = 10

        # Roll RGB values
        self.ROLL_R = 0
        self.ROLL_G = 0
        self.ROLL_B = 0

        # Point history
        self.history = []

        # Points
        self.point_list = []

        # Palette
        self.palette = []

        # Interesting Julia Values
        julia_values = ((0.4, 0.3), (0.3, 0.2), (0.35, 0.4))
        self.C_1 = julia_values[0][0]
        self.C_2 = julia_values[0][1]

        # Redraw
        self.DRAW = True
        self.COLOR = True

    def ratio(self):
        return self.SCREEN_HEIGHT / self.SCREEN_WIDTH
