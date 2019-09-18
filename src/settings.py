import src.fractal_equations as fe
import src.color_equations as ce


class Settings:
    """ Settings for fractals """

    def __init__(self):
        # Lists of available functions
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

        # Mandelbrot iterations
        self.MAX_ITER = 512

        # Screen settings
        self.SCREEN_WIDTH = 1024
        self.SCREEN_HEIGHT = 768

        self.WIDTH = self.SCREEN_WIDTH
        self.HEIGHT = self.SCREEN_WIDTH
        self.RATIO = self.SCREEN_HEIGHT / self.SCREEN_WIDTH
        self.SCREEN = None

        self.COLOR_ALGORITHM = "ce.colorize_color_black2"
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

        self.ROLL_R = 0
        self.ROLL_G = 0
        self.ROLL_B = 0

        # Plot window settings
        # self.RE_START = -1.4853696465081982
        # self.RE_END = -1.4853693374768457

        self.RE_START = -2
        self.RE_END = 1

        self.IM_START = -(((self.RE_END - self.RE_START) * self.RATIO) / 2)
        self.IM_END = ((self.RE_END - self.RE_START) * self.RATIO) / 2

        # Point history
        self.history = []

        # Mouse zoom
        self.MWHEEL_ZOOM = .2

        # Interesting Julia Values
        julia_values = ((0.4, 0.3), (0.3, 0.2), (0.35, 0.4))
        self.C_1 = julia_values[0][0]
        self.C_2 = julia_values[0][1]

        # Redraw
        self.DRAW = True
        self.COLOR = True
