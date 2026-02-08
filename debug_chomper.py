#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""详细检查 Chomper 加载过程"""

import sys
import io
import os
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, 'source')

import pygame as pg
from source import tool
from source import constants as c

pg.init()

print("=" * 70)
print("Chomper 加载过程详细检查")
print("=" * 70)

# 1. 加载图片
img = pg.image.load(r'resources\graphics\Plants\Chomper\Chomper\Chomper_0.png')
print(f"\n1. 原始图片尺寸: {img.get_width()} x {img.get_height()}")

# 2. 获取 plant.json 配置
plant_config = tool.PLANT_RECT.get('Chomper', {})
print(f"\n2. plant.json 裁剪配置:")
print(f"   x={plant_config.get('x', 0)}, y={plant_config.get('y', 0)}")
print(f"   width={plant_config.get('width', 0)}, height={plant_config.get('height', 0)}")

json_width = plant_config.get('width', 100)
json_height = plant_config.get('height', 114)

# 3. 测试倍率检测
scale = tool.detect_image_scale(img, json_width, json_height)
print(f"\n3. 倍率检测结果: {scale}x")
print(f"   宽度倍率: {img.get_width()} / {json_width} = {img.get_width()/json_width:.2f}")
print(f"   高度倍率: {img.get_height()} / {json_height} = {img.get_height()/json_height:.2f}")
print(f"   差异: {abs(img.get_width()/json_width - img.get_height()/json_height):.2f}")
print(f"   差异百分比: {abs(img.get_width()/json_width - img.get_height()/json_height) / (img.get_width()/json_width) * 100:.1f}%")

# 4. 计算裁剪区域
crop_x = int(0 * scale)
crop_y = int(0 * scale)
crop_w = int(json_width * scale)
crop_h = int(json_height * scale)
print(f"\n4. 裁剪区域:")
print(f"   x={crop_x}, y={crop_y}, width={crop_w}, height={crop_h}")
print(f"   裁剪后尺寸: {crop_w} x {crop_h}")

# 5. 获取 display_config.json 配置
display_config = tool.getDisplayConfig('plants', 'Chomper')
target_w = display_config.get('width', json_width)
target_h = display_config.get('height', json_height)
scale_mode = display_config.get('scale_mode', 'keep_ratio')
print(f"\n5. display_config.json 显示配置:")
print(f"   target_width={target_w}, target_height={target_h}")
print(f"   scale_mode={scale_mode}")

# 6. 实际测试 get_image_hd
try:
    result_img = tool.get_image_hd(
        img, 0, 0, json_width, json_height,
        c.BLACK, 1,
        category='plants', name='Chomper'
    )
    print(f"\n6. get_image_hd 结果:")
    print(f"   最终图片尺寸: {result_img.get_width()} x {result_img.get_height()}")

    # 检查是否全透明
    pixels_checked = 0
    non_transparent = 0
    step = 10
    for x in range(0, result_img.get_width(), step):
        for y in range(0, result_img.get_height(), step):
            pixels_checked += 1
            color = result_img.get_at((x, y))
            if color[3] > 0:  # alpha > 0
                non_transparent += 1

    print(f"   检查了 {pixels_checked} 个像素")
    print(f"   非透明像素: {non_transparent} ({non_transparent/pixels_checked*100:.1f}%)")

except Exception as e:
    print(f"\n6. get_image_hd 失败: {e}")
    import traceback
    traceback.print_exc()

# 7. 建议的修复方案
print(f"\n7. 问题分析:")
if scale == 1.0:
    print(f"   ⚠ 倍率检测失败！检测为 1.0x")
    print(f"   原因: 图片比例不匹配")
    print(f"   图片比例: {img.get_width()}:{img.get_height()} = {img.get_width()/img.get_height():.3f}")
    print(f"   配置比例: {json_width}:{json_height} = {json_width/json_height:.3f}")
    print(f"\n   解决方案:")
    print(f"   方案1: 修改 plant.json 中 Chomper 的裁剪配置")
    new_width = int(json_height * img.get_width() / img.get_height())
    print(f"   {{\"Chomper\": {{\"x\": 0, \"y\": 0, \"width\": {new_width}, \"height\": {json_height}}}}}")
    print(f"\n   方案2: 提供比例正确的图片")
    print(f"   期望比例: {json_width}:{json_height}")
    print(f"   如果图片高度保持 {img.get_height()}，宽度应该是: {int(img.get_height() * json_width / json_height)}")
else:
    print(f"   ✓ 倍率检测成功: {scale}x")

print("\n" + "=" * 70)
pg.quit()
