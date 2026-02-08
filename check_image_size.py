#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查图片尺寸"""

import pygame as pg
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

pg.init()

files = [
    r"resources\graphics\Screen\PanelBackground.png",
    r"resources\graphics\Screen\ChooserBackground.png"
]

for file in files:
    try:
        img = pg.image.load(file)
        rect = img.get_rect()
        print(f"{file}: {rect.w} x {rect.h}")
    except Exception as e:
        print(f"{file}: 读取失败 - {e}")

pg.quit()
