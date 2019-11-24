import math

class Window():
    """ Smoth win mover.
        
        window -> self:
        
    """
    def __init__(self, window):
        self.wnd = window
        self.corn_status = 0
        self.popup_status = -1
        
    def popup_corner_show(self):
        """ Show corner. """
        if not self.popup_status:
            # print('popup_corner_show')
            pos_start = self.wnd.screen.width() - 10
            pos_end = self.wnd.screen.width() - 26
            self.win_move(pos_start, pos_end)
            self.corn_status = 1

    def popup_corner_hide(self):
        """ Hide corner. """
        if not self.popup_status:
            if self.corn_status:
                pos_start = pos_end = self.wnd.screen.width() - 26
                pos_end = self.wnd.screen.width() - 10
                self.win_move(pos_start, pos_end)
                self.corn_status = 0

    def popup_show_full(self):
        """ Show full window. """
        if self.popup_status == 2:
            height = self.wnd.screen.height() / 2 - self.wnd.height() / 2
            width = self.wnd.screen.width() - self.wnd.width() / 2
            self.wnd.move(width, height)
            self.popup_status = 1
        else:
            height = self.wnd.screen.height() / 2 - self.wnd.height() / 2
            width = self.wnd.screen.width() - self.wnd.width()
            self.wnd.move(width, height)
            self.popup_status = 2

    def popup_show(self):
        """ Show 1/2 window. """
        pos_start = pos_end = self.wnd.screen.width() - 26
        pos_end = self.wnd.screen.width() - self.wnd.width() / 2
        self.win_move(pos_start, pos_end, 1000)
        self.popup_status = 1

    def popup_hide(self):
        """ Hide window. """
        # половина окна
        if self.popup_status == 1:
            # print(' --1/2')
            pos_start = self.wnd.screen.width() - self.wnd.width() / 2
            pos_end = self.wnd.screen.width() - 10
        
        # все окно
        elif self.popup_status == 2:
            # print(' --1')
            pos_start = self.wnd.screen.width() - self.wnd.width()
            pos_end = self.wnd.screen.width() - 10

        # 
        else:
            return

        self.win_move(pos_start, pos_end, speed=1)
        self.popup_status = 0
        self.corn_status = 0

    def win_move(self, pos_start, pos_end, speed=1):
        """ Smoth win mover.
            
            Keyword arguments:
                pos_start - int(), pos_end - int(), speed - bool()
        """
        height = self.wnd.screen.height() / 2 - self.wnd.height() / 2
        pos_start, pos_end = math.ceil(pos_start), math.ceil(pos_end)

        if pos_start < pos_end:
            i = 2 if speed else 1
        else:
            i = -2 if speed else -1
        for coords in range(pos_start, pos_end, i):
            self.wnd.move(coords, height)