# -*- coding: utf-8 -*-
# author: Ethosa

import re
import math
from copy import copy

import pygame
from .LinearGradient import LinearGradient
from ..utils.RoundRect import RoundRect


class View:
    def __init__(self, width=100, height=100,
                 background_color=(255, 255, 255, 255)):
        """View constructor

        Keyword Arguments:
            parent {Game} -- (default: {None})
            width {number} -- view width (default: {100})
            height {number} -- view height (default: {100})
            background_color {tuple} -- backgrond color (default: {(255, 255, 255, 255)})
        """
        self.background = pygame.Surface((width, height)).convert_alpha()
        self.foreground = self.background.copy()
        self.foreground.fill((0, 0, 0, 0))
        self.background.fill(background_color)
        self.background_color = background_color
        self.parent = None
        self.parent_layout = None

        self.shadow = self.foreground.copy()
        self.ripple_effect = self.foreground.copy()

        self.border = {
            "width": 0,
            "color": (0, 0, 0, 0)
        }
        self.mask = None

        self.view_id = 0
        self.x, self.y = 0, 0
        self.shadow_x_offset, self.shadow_y_offset = (0, 0)
        self.width = width
        self.height = height
        self.ripple_position = [0, 0]
        self.ripple_radius = 0
        self.ripple_color = (0, 0, 0, 0)
        self.ripple_time = 0
        self.out_time = 0
        self.tool_tip_time = 35
        self.tool_tip_pos = (0, 0)
        self.tool_tip_text = ""
        self.tool_tip_color = (0, 0, 0, 255)
        self.tool_tip_back = (255, 255, 255, 255)
        self.tool_tip_size = 15

        self.clicked = lambda position: None
        self.released = lambda: None
        self.pressed = lambda: None
        self.focused = lambda: None
        self.unfocused = lambda: None
        self.hovered = lambda: None
        self.outed = lambda: None

        self.is_clicked = 0
        self.is_focused = 0
        self.is_pressed = 0
        self.is_hovered = 0
        self.is_ripple_effect = 0
        self.is_ripple_back = 0
        self.is_visible = 1

    def bring_to_front(self):
        """moves this view to the foreground
        """
        self.parent.views.remove(self)
        self.parent.views.append(self)

    def copy(self):
        view = copy(self)
        view.background = self.background.copy()
        view.ripple_effect = self.ripple_effect.copy()
        view.foreground = self.foreground.copy()
        view.shadow = self.shadow.copy()
        return view

    def draw(self):
        """render shadow, background, foreground, and wave effect
        """
        if self.is_visible:
            self.parent.screen.blits(((self.shadow, (self.x+self.shadow_x_offset, self.y+self.shadow_y_offset)),
                                      (self.background, (self.x, self.y)),
                                      (self.foreground, (self.x, self.y)),
                                      (self.ripple_effect, (self.x, self.y))), 0)

            # draw borders
            if self.border["width"] and self.parent:
                w = self.border["width"]
                pygame.draw.rect(self.parent.screen, self.border["color"],
                                 pygame.Rect(self.x-w,
                                             self.y-w,
                                             self.width + w,
                                             self.height + w),
                                 w)

            # draw ripple effect
            if self.is_ripple_effect and self.ripple_color[3]:
                self.ripple_radius += self.width//8 if self.width > self.height else self.height//8
                clr = self.ripple_color
                if self.ripple_time < 8:
                    pygame.draw.circle(self.ripple_effect,
                                       (clr[0], clr[1], clr[2], 128 - self.ripple_time*16),
                                       (self.ripple_position[0] - self.x,
                                        self.ripple_position[1] - self.y),
                                       self.ripple_radius)
                    self.ripple_time += 1
                else:
                    self.ripple_time = 0
                    self.ripple_radius = 0
                    self.is_ripple_effect = 0
                    if not self.is_ripple_back:
                        self.ripple_effect.fill((clr[0], clr[1], clr[2], 128-16*6))
                        self.is_ripple_back = 1
            else:
                if self.is_ripple_back and not self.is_pressed:
                    self.ripple_radius += self.width//8 if self.width > self.height else self.height//8
                    if self.out_time < 8:
                        pygame.draw.circle(self.ripple_effect,
                                           (0, 0, 0, 0),
                                           (self.ripple_position[0] - self.x,
                                            self.ripple_position[1] - self.y),
                                           self.ripple_radius)
                        self.out_time += 1
                    else:
                        self.out_time = 0
                        self.is_ripple_back = 0
                        self.ripple_radius = 0
                        self.ripple_position = (0, 0)
                        self.ripple_effect.fill((0, 0, 0, 0))

            # mask draw
            if self.mask:
                for y in range(self.height):
                    for x in range(self.width):
                        if not self.mask.get_at((x, y)):
                            self.ripple_effect.set_at((x, y), (0, 0, 0, 0))

    def draw_tool_tip(self):
        if self.tool_tip_text and self.tool_tip_time == 0:
            pos = pygame.mouse.get_pos()
            rendered = pygame.font.SysFont("Roboto",
                                           self.tool_tip_size).render(self.tool_tip_text,
                                                                      True, self.tool_tip_color,
                                                                      self.tool_tip_back)
            self.parent.screen.blit(rendered, (pos[0], pos[1]+30))

    def get_rect(self):
        """getting pygame.Rect from this view

        Returns:
            pygame.Rect
        """
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def handle_event(self):
        position = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed()
        self_index = self.parent.views.index(self)

        # True if the view is on top of all.
        is_self = True
        for index, view in enumerate(self.parent.views):
            if index > self_index:
                if view.get_rect().collidepoint(position):
                    is_self = False

        collision = self.is_collide_rounded(position)
        if collision and is_self:
            if not self.is_hovered:
                self.is_hovered = 1
                self.hovered()
            if buttons[0]:
                if not self.is_clicked:
                    self.is_clicked = 1
                    self.is_pressed = 1
                    self.clicked(position)
                    self.ripple_position = position
                    self.is_ripple_effect = 1
                    if not self.is_focused:
                        self.is_focused = 1
                        self.focused()
                self.pressed()
                self.tool_tip_time = 35
            else:
                if self.is_clicked:
                    self.is_clicked = 0
                    self.is_pressed = 0
                    self.released()
            if self.tool_tip_pos != position:
                self.tool_tip_pos = position
                self.tool_tip_time = 35

            if self.tool_tip_time > 0:
                    self.tool_tip_time -= 1
        else:
            if self.is_clicked:
                self.is_clicked = 0
                self.is_pressed = 0
                self.released()
            if self.is_hovered:
                self.is_hovered = 0
                self.tool_tip_time = 35
                self.outed()
            if self.is_focused:
                if buttons[0]:
                    self.is_focused = 0
                    self.unfocused()

    def is_collide(self, obj):
        """check collision with point or rect

        Arguments:
            obj {tuple} -- point (x, y) or rect (x, y, width, height)

        Returns:
            bool
        """
        if isinstance(obj, tuple):
            if len(obj) == 2:
                return self.get_rect().collidepoint(obj)
            elif len(obj) == 4:
                return self.get_rect().colliderect(pygame.Rect(obj))

    def is_collide_rounded(self, position):
        collision = self.get_rect().collidepoint(position)
        if collision and self.mask and position[0] >= self.x and position[1] >= self.y:
            collision = self.mask.get_at(
                (position[0] - self.x - self.width
                    if position[0] > self.width + self.x else position[0] - self.x,
                 position[1] - self.y - self.height
                    if position[1] > self.height + self.y else position[1] - self.y)
                )
        return collision

    def move(self, x, y):
        """moving this view to certain coordinates on the x and y axes

        Arguments:
            x {number}
            y {number}
        """
        self.x, self.y = x, y

    def on_click(self, f):
        self.clicked = f

    def on_focused(self, f):
        self.focused = f

    def on_hover(self, f):
        self.hovered = f

    def on_pressed(self, f):
        self.pressed = f

    def on_release(self, f):
        self.released = f

    def on_out(self, f):
        self.outed = f

    def on_unfocused(self, f):
        self.unfocused = f

    def resize(self, w, h):
        """resizes the view using the arguments passed

        Arguments:
            w {int} -- new width
            h {int} -- new height

        P.S.
            Also, w and h can be strings, however, the view must have parent_layout.
        """
        if self.parent_layout and isinstance(w, str):
            if w == "fill_parent":
                w = self.parent_layout.width
        if self.parent_layout and isinstance(h, str):
            if h == "fill_parent":
                h = self.parent_layout.width
        self.width = w
        self.height = h
        self.shadow = pygame.transform.smoothscale(self.shadow, (w, h))
        self.background = pygame.transform.smoothscale(self.background, (w, h))
        self.foreground = pygame.transform.smoothscale(self.foreground, (w, h))
        self.ripple_effect = pygame.transform.smoothscale(self.ripple_effect, (w, h))

    def set_background(self, path_or_color, mode="resize"):
        """Fills the background with color if the string is HEX

        Arguments:
            path_or_color {str} -- file path or hex (or rgba) color

        Keyword Arguments:
            mode {str} -- mode for image, can be "resize", "crop", "inside"
                "inside right", "inside right_top", "inside right_bottom",
                "inside left", "inside left_top", "inside left_bottom",
                "inside top", "inside bottom" (default: {"resize"})
        """
        if isinstance(path_or_color, str):
            if re.match(r"\A#[0-9a-fA-F]{6,8}\Z", path_or_color):
                self.set_background_color(path_or_color)
            else:
                self.set_background_image(path_or_color, mode)
        elif isinstance(path_or_color, tuple):
            self.set_background_color(path_or_color)
        elif isinstance(path_or_color, pygame.Surface):
            self.set_background_image(path_or_color, mode)

    def set_background_color(self, color):
        """Fills the background with color

        Arguments:
            color {tuple}
        """
        self.background_color = pygame.Color(color)
        self.background.fill(self.background_color)

    def set_background_image(self, path, mode="resize", is_path=True):
        """loads image as background

        Arguments:
            path {str} -- file path

        Keyword Arguments:
            mode {str} -- mode for image, can be "resize", "crop", "inside"
                "inside right", "inside right_top", "inside right_bottom",
                "inside left", "inside left_top", "inside left_bottom",
                "inside top", "inside bottom" (default: {"resize"})
            is_path {bool} -- is path?
        """
        if path:
            if is_path:
                self.background_image = pygame.image.load(path)
            else:
                self.background_image = path
            if mode == "resize":
                self.background.blit(
                    pygame.transform.smoothscale(self.background_image,
                                                 (self.width, self.height)),
                    (0, 0))
            elif mode == "crop":
                w, h = self.background_image.get_size()
                while w < self.width:
                    w *= 2
                while h < self.height:
                    h *= 2
                if self.background_image.get_size() != (w, h):
                    pygame.transform.smoothscale(self.background_image, (w, h))
                rect = pygame.Rect(w//2 - self.width//2, h//2 - self.height//2,
                                   self.width, self.height)
                self.background.blit(self.background_image.subsurface(rect), (0, 0))
            elif mode.startswith("inside"):
                w, h = self.background_image.get_size()
                while w > self.width or h > self.height:
                    w //= 2
                    h //= 2
                x, y = w/h, h/w
                while w < self.width and h < self.height:
                    w += x
                    h += y

                # image x, y calculate
                x, y = 0, 0
                w, h = int(w), int(h)
                if mode.endswith("left"):
                    if h < self.height:
                        y = self.height//2 - h//2
                elif mode.endswith("top"):
                    if w < self.width:
                        x = self.width//2 - w//2
                elif mode.endswith("right"):
                    x = self.width - w
                    if h < self.height:
                        y = self.height//2 - h//2
                elif mode.endswith("right_top"):
                    x = self.width - w
                elif mode.endswith("right_bottom"):
                    x = self.width - w
                    y = self.height - h
                elif mode.endswith("bottom"):
                    if w < self.width:
                        x = self.width//2 - w//2
                    y = self.height - h
                elif mode.endswith("left_bottom"):
                    y = self.height - h
                elif mode == "inside":
                    if w < self.width:
                        x = self.width//2 - w//2
                    elif h < self.height:
                        y = self.height//2 - h//2

                background = pygame.transform.smoothscale(self.background_image, (w, h))
                self.background.blit(background, (x, y))

    def set_border(self, width, color):
        """set view borders

        Arguments:
            width {int} -- border width
            color {tuple or str} -- border color (supported alpha channel)
        """
        self.border = {
            "width": width,
            "color": pygame.Color(color)
        }

    def set_border_color(self, color=(255, 255, 255, 255)):
        """set view border color

        Keyword Arguments:
            color {tuple} -- border color (default: {(255, 255, 255, 255)})
        """
        self.border["color"] = pygame.Color(color)

    def set_border_width(self, width):
        """set view borders width

        Arguments:
            width {int} -- width in pixels
        """
        self.border["width"] = width

    def set_foreground_color(self, color):
        """fill view foreground

        Arguments:
            color {tuple} -- fill color
        """
        self.foreground_color = pygame.Color(color)
        self.foreground.fill(self.foreground_color)

    def set_gradient(self, pos1, pos2, clr1, clr2):
        """Draws a linear gradient from point pos1 to point pos2

        Arguments:
            pos1 {tuple} -- first position
            pos2 {tuple} -- second position
            clr1 {tuple} -- first color
            clr2 {tuple} -- second color
        """
        lg = LinearGradient((self.width, self.height), pos1[::-1], pos2[::-1],
                            pygame.Color(clr1), pygame.Color(clr2))
        lg.fill_gradient()
        self.background_image = lg.surface.copy()
        self.background = self.background_image

    def set_parent(self, parent):
        if parent:
            self.parent = parent
            self.screen = pygame.Surface(parent.screen.get_size()).convert_alpha()
            self.screen.fill((0, 0, 0, 0))

    def set_ripple_color(self, color):
        self.ripple_color = pygame.Color(color)

    def set_round(self, borders=(0, 0, 0, 0)):
        """rounds the edges of the view, also affects the collision

        Keyword Arguments:
            borders {tuple} -- borders corners
                (lefttop, righttop, rightbottom, leftbottom) (default: {(0, 0, 0, 0)})
        """
        self.border["width"] = 0
        surface = pygame.Surface((self.width, self.height)).convert_alpha()
        RoundRect(surface, borders, (255, 255, 255, 255))
        self.mask = pygame.mask.from_surface(surface)
        for y in range(self.height):
            for x in range(self.width):
                if not self.mask.get_at((x, y)):
                    self.background.set_at((x, y), (0, 0, 0, 0))
                    self.foreground.set_at((x, y), (0, 0, 0, 0))
                    self.ripple_effect.set_at((x, y), (0, 0, 0, 0))

    def set_shadow(self, end_color, offset=(0, 0), scale=1.0, start_color=(0, 0, 0, 0)):
        """draws a diamond-shaped gradient making a shadow

        Arguments:
            end_color {tuple} -- color in center

        Keyword Arguments:
            offset {tuple} -- shadow offset (default: {(0, 0)})
            scale {number} -- shadow scale (default: {1.0})
            start_color {tuple} -- color in borders (default: {(0, 0, 0, 0)})
        """
        imgsize = (self.width, self.height)
        self.shadow_x_offset, self.shadow_y_offset = offset
        self.shadow = pygame.Surface((self.width, self.height)).convert_alpha()
        self.shadow.fill((0, 0, 0, 0))
        sqrt = math.sqrt(2)
        ds = sqrt * imgsize[0]/2
        for y in range(imgsize[1]):
            for x in range(imgsize[0]):
                # Find the distance to the center
                distance = min(abs(x - imgsize[0]), x, abs(y - imgsize[1]), y)

                # Make it on a scale from 0 to 1innerColor
                distance = distance / ds

                # Calculate r, g, b and q values
                r = end_color[0] * distance + start_color[0] * (1 - distance)
                g = end_color[1] * distance + start_color[1] * (1 - distance)
                b = end_color[2] * distance + start_color[2] * (1 - distance)
                a = end_color[3] * distance + start_color[3] * (1 - distance)

                # print r, g, b, a
                if y < self.height and x < self.width:
                    self.shadow.set_at((x, y), (int(r), int(g), int(b), int(a)))
        w, h = int(self.width*scale), int(self.height*scale)
        self.shadow = pygame.transform.smoothscale(self.shadow, (w, h))
        self.shadow_x_offset -= (w - self.width)//2
        self.shadow_y_offset -= (h - self.height)//2

    def set_tool_tip(self, text, text_size=15, text_color=(0, 0, 0, 255), back_color=(255, 255, 255, 255)):
        self.tool_tip_text = text
        self.tool_tip_color = pygame.Color(text_color)
        self.tool_tip_back = pygame.Color(back_color)
        self.tool_tip_size = text_size

    def set_visible(self, v):
        self.is_visible = v

    def set_x(self, x):
        """move view at x axe

        Arguments:
            x {number}
        """
        self.x = x

    def set_y(self, y):
        """move view at y axe

        Arguments:
            y {number}
        """
        self.y = y

    def set_z(self, z):
        """move view at z axe

        Arguments:
            z {number}
        """
        self.parent.views.remove(self)
        self.parent.views.insert(z, self)
