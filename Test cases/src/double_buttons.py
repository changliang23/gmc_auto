__author__ = 'lchang'

import random

def random_click(button_1, button_2):
    if random.choice([True, False]):
        return button_1
    else:
        return button_2