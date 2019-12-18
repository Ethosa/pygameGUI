# -*- coding: utf-8 -*-
# author: Ethosa

import pygame
from PIL import Image, ImageFilter
from .View import View


class ImageView(View):
    FILTERS = {
        "blur": ImageFilter.BLUR,
        "contour": ImageFilter.CONTOUR,
        "detail": ImageFilter.DETAIL,
        "edge_enchance": ImageFilter.EDGE_ENHANCE,
        "edge_enchance_more": ImageFilter.EDGE_ENHANCE_MORE,
        "emboss": ImageFilter.EMBOSS,
        "find_edges": ImageFilter.FIND_EDGES,
        "sharpen": ImageFilter.SHARPEN,
        "smooth": ImageFilter.SMOOTH,
        "smooth_more": ImageFilter.SMOOTH_MORE
    }

    def __init__(self, image_path="", width=0, height=0):
        """Creates an instance of ImageView

        Keyword Arguments:
            image_path {str} -- image path (default: {""})
            width {number} -- custom width (default: {0})
            height {number} -- custom height (default: {0})
        """
        self.image = Image.open(image_path)
        self.image.convert("RGBA")
        if width and height:
            self.image = self.image.resize((width, height), Image.ANTIALIAS)
        w, h = self.image.size
        super().__init__(width=w, height=h)

        background = pygame.image.fromstring(self.image.tobytes(), self.image.size, self.image.mode)
        self.set_background_image(background, "inside", False)

    def filter(self, filter_name=""):
        """Overlays the image filters. A function can be called an infinite number of times.

        Keyword Arguments:
            filter_name {str} -- filter name (default: {""})
        """
        if filter_name in ImageView.FILTERS:
            self.image = self.image.filter(ImageView.FILTERS[filter_name])
            background = pygame.image.fromstring(self.image.tobytes(), self.image.size, self.image.mode)
            self.set_background_image(background, "inside", False)
