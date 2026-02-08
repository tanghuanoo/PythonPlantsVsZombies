# 高清图片替换常见问题及解决方案

## 问题 1：Chomper 替换后看不见

### 症状
替换了 Chomper_0.png 后，在游戏中点击放置后无法看见这个植物。

### 原因分析

1. **缺少动画帧**
   - Chomper 是动画植物，需要 13 帧（Chomper_0.png 到 Chomper_12.png）
   - 只替换 Chomper_0.png 会导致游戏加载其他帧时失败

2. **图片尺寸比例不匹配**
   - 原始图片：130 x 114
   - 新图片：705 x 962
   - 配置尺寸：100 x 114
   - 倍率不一致：宽度 7.05x，高度 8.4x

### 解决方案

#### 方案 1：准备完整动画帧（推荐）
准备 Chomper 的所有 13 帧动画：
```
resources/graphics/Plants/Chomper/Chomper/
├── Chomper_0.png
├── Chomper_1.png
├── ...
└── Chomper_12.png
```

#### 方案 2：使用单帧复制
如果只有一张图片，复制为多帧：
```bash
cd resources/graphics/Plants/Chomper/Chomper
for i in {1..12}; do cp ChomperDigest_0.png Chomper_$i.png; done
```

#### 方案 3：调整配置尺寸
修改 `display_config.json` 匹配图片比例：
```json
{
  "plants": {
    "specific": {
      "Chomper": {"width": 101, "height": 137}
    }
  }
}
```

### 已应用的修复
✅ 自动复制了 Chomper_0.png 为 13 帧
✅ 调整配置为 101 x 137（匹配 705:962 比例）

---

## 问题 2：StartButton 点击后被放大

### 症状
StartButton.png 在点击后突然被放大。

### 原因分析

StartButton 使用 Panel.loadFrame() 加载，但该方法没有为 StartButton 提供专门配置，导致使用了默认的 'panel' 配置（465x513），将按钮错误地缩放了。

实际尺寸：154 x 37
错误配置：465 x 513（panel 的尺寸）

### 解决方案

1. 在 `display_config.json` 添加 StartButton 配置：
```json
{
  "ui": {
    "specific": {
      "startbutton": {
        "width": 154,
        "height": 37,
        "scale_mode": "keep_ratio"
      }
    }
  }
}
```

2. 修改 `Panel.loadFrame()` 方法识别 StartButton：
```python
def loadFrame(self, name):
    if name == 'ChooserBackground':
        config_name = 'menubar'
    elif name == 'PanelBackground':
        config_name = 'panel'
    elif name == 'StartButton':
        config_name = 'startbutton'
    else:
        config_name = 'panel'
```

### 已应用的修复
✅ 添加了 StartButton 配置（154 x 37）
✅ 修改了 Panel.loadFrame() 方法

---

## 通用原则：替换高清图片的注意事项

### 1. 检查是否需要多帧
某些对象是动画，需要多帧：

| 对象类型 | 需要帧数 | 示例 |
|---------|---------|------|
| 植物（动画） | 多帧 | Chomper (13帧), SunFlower (18帧) |
| 植物（静态） | 单帧 | WallNut |
| 僵尸 | 多帧 | 行走、攻击、死亡等状态 |
| UI 元素 | 单帧 | 按钮、背景 |

查看原始目录 `resources/origin_graphics/` 了解需要多少帧。

### 2. 检查图片尺寸和比例

使用检查脚本：
```bash
python -c "import pygame as pg; pg.init(); img = pg.image.load('your_image.png'); print(f'{img.get_width()} x {img.get_height()}'); pg.quit()"
```

对比配置文件中的基准尺寸：
```json
"Chomper": {"width": 100, "height": 114}  // 基准尺寸
```

检查倍率是否一致：
- 宽度倍率：实际宽度 / 配置宽度
- 高度倍率：实际高度 / 配置高度
- **两个倍率应该相近**（允许 ±20% 误差）

### 3. 图片比例不对时的处理

如果图片比例与配置不匹配：

#### 选项 1：调整配置尺寸（推荐）
修改 `display_config.json` 中的 width 和 height，使其匹配图片比例。

例如：图片 705x962 (0.733:1)
```json
"Chomper": {"width": 101, "height": 137}  // 保持 0.733:1 比例
```

#### 选项 2：使用不同的缩放模式
```json
"Chomper": {
  "width": 100,
  "height": 114,
  "scale_mode": "stretch"  // 强制拉伸
}
```

- `keep_ratio`: 保持比例（可能有透明边）
- `stretch`: 强制拉伸（可能变形）
- `cover`: 覆盖裁剪（不变形但裁边）

### 4. 验证步骤

1. **替换图片**到对应目录
2. **检查帧数**是否完整
3. **检查尺寸**和比例
4. **运行游戏**测试显示效果
5. 如果不对，**调整配置**
6. **重启游戏**验证

## 调试工具

### 检查图片信息
```bash
python check_chomper.py  # 检查 Chomper
python check_image_size.py  # 检查其他图片
```

### 验证配置
```bash
python verify_ui_config.py  # 验证 UI 配置
```

### 测试高清化功能
```bash
python test_hd.py  # 测试所有高清化功能
```

## 快速参考

### 常见植物帧数

| 植物 | 闲置帧数 | 其他动画 |
|------|---------|---------|
| Chomper | 13 | ChomperAttack (9帧), ChomperDigest (7帧) |
| SunFlower | 18 | - |
| Peashooter | 13 | - |
| WallNut | 16 | WallnutCracked1 (11帧), WallnutCracked2 (11帧) |

### 当前配置的基准尺寸

参考 `CONFIG_SIZE_GUIDE.md` 查看完整列表。

### 常见错误及解决

| 错误 | 原因 | 解决方案 |
|------|------|---------|
| 植物/僵尸看不见 | 缺少动画帧 | 补全所有帧或复制单帧 |
| 显示变形 | 比例不匹配 | 调整配置或使用 keep_ratio |
| 按钮被放大 | 使用了错误配置 | 添加专门配置 |
| 图片模糊 | 倍率检测错误 | 检查尺寸是否是配置的整数倍 |

## 总结

替换高清图片的核心原则：
1. ✅ 确保帧数完整（动画对象）
2. ✅ 保持图片比例与配置匹配
3. ✅ 为每种 UI 元素提供专门配置
4. ✅ 测试后根据实际效果调整配置

遇到问题时：
1. 检查帧数是否完整
2. 检查图片尺寸和比例
3. 调整 display_config.json
4. 重启游戏测试
