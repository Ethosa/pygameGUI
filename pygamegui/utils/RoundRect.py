# -*- coding: utf-8 -*-
# author: Ethosa

from pygame import draw, Color


class RoundRect:
    def __init__(self, surface, radius=(0, 0, 0, 0), color=(255, 255, 255, 255)):
        surface.fill((0, 0, 0, 0))
        w, h = surface.get_size()
        color = Color(color)

        # draw circle shapes
        draw.circle(surface, color,
                    (radius[0], radius[0]),
                    radius[0])
        draw.circle(surface, color,
                    (w - radius[1], radius[1]),
                    radius[1])
        draw.circle(surface, color,
                    (w - radius[2], h - radius[2]),
                    radius[2])
        draw.circle(surface, color,
                    (radius[3], h - radius[3]),
                    radius[3])

        # draw lines
        surface.fill(color,
                     (0,
                      radius[0],
                      radius[0],
                      h - radius[3] - radius[0]))
        surface.fill(color,
                     (radius[0],
                      0,
                      w - radius[1] - radius[0],
                      radius[1] if radius[1] > radius[0] else radius[0]))
        surface.fill(color,
                     (w - radius[1] if radius[1] > radius[2] else w - radius[2],
                      radius[1],
                      w - radius[1] if radius[1] > radius[2] else w - radius[2],
                      h - radius[1] - radius[2]))
        surface.fill(color,
                     (radius[3],
                      h - radius[3] if radius[3] > radius[2] else h - radius[2],
                      w - radius[3] - radius[2],
                      h - radius[3] if radius[3] > radius[2] else h - radius[2]))

        # fill rect
        surface.fill(color,
                     (radius[0],
                      radius[0],
                      w - radius[2] - radius[0] - (radius[3] - radius[1] if radius[3] < radius[1] else 0),
                      h - radius[2] - radius[0] - (radius[3] - radius[2] if radius[3] > radius[2] else 0)))
