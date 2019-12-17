# -*- coding: utf-8 -*-
# author: Ethosa

import sys

from pygame import display, image
import pygame

from pygamegui.gui import TextView, Manager

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
        view = TextView(width=255, height=155, background_color=(0, 0, 0, 55))
        view.move(0, 0)

        view.set_text("heh ..")
        view.set_text_size(30)
        view.set_font("Calibri")

        view.set_ripple_color("#dd7777")
        view.set_shadow((0, 0, 0, 128), scale=1.1)

        self.manager.add(view)

        def click(pos):
            self.manager.take_screenshot("hello_world.png")
            view.set_text("FPS: %s\nLOL :D\nclicked position:\n%s" % (self.clock.get_fps(), pos),
                          color="#7777dd50")

        view.on_click(click)

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
