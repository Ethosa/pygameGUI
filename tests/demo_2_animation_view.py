# -*- coding: utf-8 -*-
# author: Ethosa

import sys

from pygame import display, image
import pygame

from pygamegui.gui import AnimatedView, Manager

pygame.init()


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
        self.screen = pygame.Surface((width, height))
        self.screen = self.screen.convert_alpha()
        self.clock = pygame.time.Clock()

        self.manager = Manager(self)
        view = AnimatedView(width=255, height=155, background_color=(33, 33, 77, 128))
        view.move(0, 0)
        for i in range(255, 100, -1):
            view.add_frame((i, i, i, 255))
        for i in range(100, 255):
            view.add_frame((i, i, i, 255))

        view.set_ripple_color("#dd7777")

        self.manager.add(view)
        view.on_click(lambda pos: self.manager.take_screenshot("hello_world.png"))

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.manager.event()


if __name__ == '__main__':
    game = Game(670, 512)
    game.start_loop()
