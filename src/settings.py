class Settings():
    def __init__(self):

        self.MAX_ITER = 256
        self.COLOR_SCALE = 64

        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 1000
        self.WIDTH = self.SCREEN_WIDTH
        self.HEIGHT = self.SCREEN_WIDTH

        # Default, FUll plot window
        self.RE_START = -2
        self.RE_END = 1
        self.IM_START = -1.5
        self.IM_END = 1.5

        # Interesting Julia Values
        julia_values = ((.4, .3), (.3, .2), (.35, .4))
        self.C_1 = julia_values[2][0]
        self.C_2 = julia_values[2][1]

        # Internal program use, do not adjust.
        self._mouse_down = None
        self._mouse_up = None
