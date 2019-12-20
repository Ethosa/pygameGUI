# -*- coding: utf-8 -*-
# author: Ethosa

from math import floor

from pygame import Surface
from .View import View


class AnimatedView(View):
    def __init__(self, width=100, height=100,
                 background_color=(255, 255, 255, 255), frames=[],
                 animation_speed=0.2):
        """View constructor

        Keyword Arguments:
            width {number} -- view width (default: {100})
            height {number} -- view height (default: {100})
            background_color {tuple} -- backgrond color (default: {(255, 255, 255, 255)})
            frames {list} -- frames for animation (default: {[]})
            animation_speed {number} -- frame rate
        """
        View.__init__(self, width, height, background_color)
        self.frames = frames
        self.animation_speed = animation_speed
        self.state = 0.0

    def add_frame(self, frame):
        """add new frame in animation frames

        Arguments:
            frame {tuple or pygame.Surface} -- color or surface
        """
        if isinstance(frame, tuple):
            color = frame[:]
            frame = Surface((self.width, self.height)).convert_alpha()
            frame.fill(color)
        self.frames.append(frame)

    def animate(self):
        """change frame
        """
        if len(self.frames) > 1:
            if self.state < len(self.frames)-self.animation_speed:
                self.state += self.animation_speed
            else:
                self.state = 0.0
            self.background = self.frames[int(floor(self.state))].copy()

    def draw(self):
        super().draw()
        self.animate()
