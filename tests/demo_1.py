# -*- coding: utf-8 -*-
# author: Ethosa

import sys

from pygame import display, image, QUIT, Surface, time, event, quit as q, init

from pygamegui.gui import Manager

init()


class Game:
    def __init__(self, width=1024, height=720, name="window",
                 icon="icon.jpg"):
        self.width = width
        self.height = height
        self.size = [self.width, self.height]

        display.set_caption(name)
        if icon:
            display.set_icon(image.load(icon))

        self.display = display.set_mode(self.size)
        self.screen = Surface((width, height))
        self.screen = self.screen.convert_alpha()
        self.clock = time.Clock()

        self.manager = Manager(self)

    def render(self):
        self.manager.draw()
        self.display.blit(self.screen, (0, 0))

    def start_loop(self):
        while 1:
            self.clock.tick(60)
            self.handle_events()
            self.render()
            display.update()

    def handle_events(self):
        for e in event.get():
            if e.type == QUIT:
                q()
                sys.exit()
        self.manager.event()


if __name__ == '__main__':
    game = Game(670, 512)
    game.start_loop()
