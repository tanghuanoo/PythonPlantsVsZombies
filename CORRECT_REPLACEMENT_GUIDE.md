# 高清图片替换正确流程

## ⚠️ 重要原则

**不裁剪，只缩放！**

当您替换高清图片时，系统应该使用**整张图片**进行缩放，而不是裁剪。

## 📋 正确的替换步骤

### 步骤 1：准备高清图片

准备您的高清图片（任意倍率，任意比例）。

### 步骤 2：修改 plant.json 或 zombie.json

**关键步骤**：将裁剪配置改为图片的实际尺寸。

#### 示例：替换 Chomper

1. **检查图片尺寸**
```bash
python -c "import pygame as pg; pg.init(); img = pg.image.load('resources/graphics/Plants/Chomper/Chomper/Chomper_0.png'); print(f'{img.get_width()} x {img.get_height()}'); pg.quit()"
```

输出：`705 x 962`

2. **修改 plant.json**
```json
{
  "plant_image_rect": {
    "Chomper": {"x": 0, "y": 0, "width": 705, "height": 962}
  }
}
```

**注意**：
- `x` 和 `y` 保持为 0（从左上角开始）
- `width` 和 `height` 设置为图片的**实际尺寸**

### 步骤 3：调整 display_config.json

设置游戏中的显示尺寸（这个尺寸是游戏逻辑尺寸）：

```json
{
  "plants": {
    "specific": {
      "Chomper": {
        "width": 100,
        "height": 137,
        "scale_mode": "keep_ratio"
      }
    }
  }
}
```

**作用**：
- 图片会从 705x962 缩放到 100x137 显示
- 使用 `keep_ratio` 保持图片比例

### 步骤 4：准备所有动画帧

如果是动画对象，准备所有帧：

```bash
# Chomper 需要 13 帧
resources/graphics/Plants/Chomper/Chomper/
├── ChomperDigest_0.png
├── Chomper_1.png
├── ...
└── Chomper_12.png
```

如果只有一张图，临时复制多份：
```bash
cd resources/graphics/Plants/Chomper/Chomper
for i in {1..12}; do cp ChomperDigest_0.png Chomper_$i.png; done
```

### 步骤 5：测试游戏

```bash
python main.py
```

## 📐 工作原理

### 旧的裁剪方式（有问题）

```
原始图片 705x962
    ↓
裁剪 100x114 (只取左上角一小块) ❌
    ↓
缩放到 101x137
    ↓
结果：只能看到图片的左上角一小部分
```

### 新的整图缩放方式（正确）

```
原始图片 705x962
    ↓
使用整图 705x962 ✅
    ↓
缩放到 100x137 (保持比例)
    ↓
结果：能看到完整图片
```

## 🛠️ 快速替换工具

创建一个辅助脚本 `prepare_image.py`：

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""辅助工具：准备高清图片配置"""

import pygame as pg
import sys
import json

if len(sys.argv) < 3:
    print("用法: python prepare_image.py <对象名> <图片路径>")
    print("示例: python prepare_image.py Chomper resources/graphics/Plants/Chomper/Chomper/ChomperDigest_0.png")
    sys.exit(1)

name = sys.argv[1]
image_path = sys.argv[2]

pg.init()
img = pg.image.load(image_path)
width = img.get_width()
height = img.get_height()
pg.quit()

print(f"\n图片尺寸: {width} x {height}")
print(f"\n添加到 plant.json:")
print(f'    "{name}": {{"x": 0, "y": 0, "width": {width}, "height": {height}}}')

# 计算合适的显示尺寸（保持比例，高度约 120）
target_height = 120
target_width = int(width * target_height / height)

print(f"\n建议的 display_config.json:")
print(f'    "{name}": {{"width": {target_width}, "height": {target_height}}}')
```

使用方法：
```bash
python prepare_image.py Chomper resources/graphics/Plants/Chomper/Chomper/ChomperDigest_0.png
```

## 📝 完整示例

### 替换 SunFlower

1. **图片尺寸**：`800 x 820`

2. **修改 plant.json**：
```json
"SunFlower": {"x": 0, "y": 0, "width": 800, "height": 820}
```

3. **修改 display_config.json**：
```json
"SunFlower": {"width": 73, "height": 74, "scale_mode": "keep_ratio"}
```

4. **结果**：
   - 图片从 800x820 缩放到约 73x75 显示
   - 保持原图比例

### 替换 Zombie

1. **图片尺寸**：`1200 x 1500`

2. **修改 zombie.json**：
```json
"Zombie": {"x": 0, "width": 1200}
```

**注意**：zombie.json 只有 x 和 width，没有 y 和 height

3. **修改 display_config.json**：
```json
"Zombie": {"width": 115, "height": 144, "scale_mode": "keep_ratio"}
```

## 🔍 调试工具

使用 `debug_chomper.py` 检查加载过程：

```bash
python debug_chomper.py
```

查看：
- 倍率检测结果
- 裁剪区域
- 最终显示尺寸
- 非透明像素百分比

## ⚡ 常见问题

### Q1: 为什么我的图片看不见？

**A**: 检查 plant.json 中的配置是否使用了图片的实际尺寸。

错误❌：
```json
"Chomper": {"x": 0, "y": 0, "width": 100, "height": 114}  // 图片是 705x962
```

正确✅：
```json
"Chomper": {"x": 0, "y": 0, "width": 705, "height": 962}  // 使用实际尺寸
```

### Q2: 图片太大或太小怎么办？

**A**: 调整 display_config.json 中的 width 和 height。

### Q3: 图片变形了怎么办？

**A**: 确保使用 `scale_mode: "keep_ratio"`。

### Q4: 我需要裁剪掉图片的透明边框怎么办？

**A**: 在替换高清图片前，先用图片编辑工具裁剪掉透明边框，然后再替换。

## 📊 对比：plant.json vs display_config.json

| 配置文件 | 作用 | 何时修改 |
|---------|------|---------|
| **plant.json** | 定义**裁剪区域**（使用图片的哪一部分） | 替换图片时，改为图片的实际尺寸 |
| **display_config.json** | 定义**显示尺寸**（游戏中多大） | 想调整游戏中显示大小时修改 |

### 示例说明

```json
// plant.json - 裁剪配置
"Chomper": {"x": 0, "y": 0, "width": 705, "height": 962}
// 意思：使用从 (0,0) 开始的 705x962 区域（整图）

// display_config.json - 显示配置
"Chomper": {"width": 100, "height": 137}
// 意思：在游戏中显示为 100x137 的大小
```

流程：
```
图片 705x962 → 使用区域 705x962 → 缩放到 100x137 → 游戏显示
```

## ✅ 总结

替换高清图片的核心原则：

1. **plant.json/zombie.json**：使用图片的**实际尺寸**（不裁剪）
2. **display_config.json**：设置游戏中的**显示尺寸**（缩放）
3. **scale_mode**：使用 `keep_ratio` 保持比例

记住：**不裁剪，只缩放！**
