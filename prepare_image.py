#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""辅助工具：准备高清图片配置"""

import pygame as pg
import sys
import json
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

if len(sys.argv) < 3:
    print("用法: python prepare_image.py <对象名> <图片路径>")
    print("示例: python prepare_image.py Chomper resources/graphics/Plants/Chomper/Chomper/ChomperDigest_0.png")
    sys.exit(1)

name = sys.argv[1]
image_path = sys.argv[2]

try:
    pg.init()
    img = pg.image.load(image_path)
    width = img.get_width()
    height = img.get_height()
    ratio = width / height
    pg.quit()

    print("=" * 70)
    print(f"图片信息：{name}")
    print("=" * 70)
    print(f"\n实际尺寸: {width} x {height}")
    print(f"宽高比: {ratio:.3f} (宽:高 = {width}:{height})")

    print(f"\n【步骤 1】添加到 plant.json 或 zombie.json:")
    print(f'    "{name}": {{"x": 0, "y": 0, "width": {width}, "height": {height}}}')

    # 计算合适的显示尺寸（保持比例）
    # 尝试几种不同的目标高度
    for target_height in [120, 100, 80]:
        target_width = int(width * target_height / height)
        print(f"\n【步骤 2】添加到 display_config.json (高度 {target_height}):")
        print(f'    "{name}": {{"width": {target_width}, "height": {target_height}, "scale_mode": "keep_ratio"}}')

    print("\n" + "=" * 70)
    print("提示：")
    print("1. 复制上面的配置到对应的 JSON 文件")
    print("2. 如果是动画对象，准备所有帧（Chomper 需要 13 帧）")
    print("3. 运行游戏测试，根据实际效果调整 display_config.json 中的尺寸")
    print("=" * 70)

except Exception as e:
    print(f"错误: {e}")
    sys.exit(1)
