# -*- coding: utf-8 -*-
# author: Ethosa

from .gui import (LinearGradient, Manager, View, AnimatedView,
                  TextView, ImageView, LinearLayout, DialogView, Button, ScrollView)
from .utils import Timer, ThreadCreator

__version__ = "0.1.2"
__copyright__ = "2019"
__license__ = "LGPLv3"
__authors__ = ["Ethosa"]

if __name__ == '__main__':
    print(LinearGradient, View, Manager,
          AnimatedView, TextView, ImageView,
          LinearLayout, DialogView, Button,
          ScrollView)
    print(Timer, ThreadCreator)
