# -*- coding: utf-8 -*-
# author: Ethosa

import sys

from pygame import display, image
import pygame

from pygamegui.gui import View, Manager

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
        view = View(width=255, height=155, background_color=(33, 33, 77, 128))
        view.move(0, 0)
        view.set_background("icon.jpg", "inside right")
        view1 = View(width=255, height=155, background_color=(33, 77, 33, 128))
        view1.move(0, 155)
        view1.set_background("icon.jpg", "inside")
        view2 = View(width=255, height=155, background_color=(77, 33, 33, 128))
        view2.move(0, 155*2)
        view2.set_background("icon.jpg", "inside left")

        self.manager.add(view, view1, view2)
        view2.on_click(lambda pos: self.manager.take_screenshot("hello_world.png"))

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
