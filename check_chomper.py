#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame as pg
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

pg.init()

print("检查 Chomper 图片")
print("=" * 60)

# 检查原始图片
print("\n原始图片 (origin_graphics):")
try:
    img = pg.image.load(r'resources\origin_graphics\Plants\Chomper\Chomper\Chomper_0.png')
    print(f"  ChomperAttack_0.png: {img.get_width()} x {img.get_height()}")
except Exception as e:
    print(f"  读取失败: {e}")

# 检查新图片
print("\n新图片 (graphics):")
try:
    img = pg.image.load(r'resources\graphics\Plants\Chomper\Chomper\Chomper_0.png')
    print(f"  ChomperAttack_0.png: {img.get_width()} x {img.get_height()}")

    # 检查是否有其他帧
    import os
    chomper_dir = r'resources\graphics\Plants\Chomper\Chomper'
    if os.path.exists(chomper_dir):
        files = [f for f in os.listdir(chomper_dir) if f.endswith('.png')]
        print(f"  找到 {len(files)} 个文件: {files}")
except Exception as e:
    print(f"  读取失败: {e}")

# 检查配置
print("\n配置信息:")
print(f"  plant.json 裁剪配置: x=0, y=0, width=100, height=114")
print(f"  display_config.json: width=100, height=114")

print("\n" + "=" * 60)
pg.quit()
