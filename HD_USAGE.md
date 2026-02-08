# 游戏高清化功能使用说明

## 功能概述

本次更新实现了游戏的高清化方案，支持：

1. **智能倍率检测**：自动识别图片是 1x、2x、3x 或 4x 高清资源
2. **比例自动调整**：支持三种缩放模式（keep_ratio/stretch/cover）
3. **统一配置管理**：通过 JSON 配置文件集中管理所有对象的显示尺寸
4. **向后兼容**：低清图片和高清图片可以混用
5. **不影响游戏逻辑**：碰撞检测、布局、速度等保持不变

## 核心文件

### 1. 配置文件

**位置**：`source/data/entity/display_config.json`

这是所有显示配置的中心，包含：

- **default**：全局默认配置（缩放模式和质量）
- **plants**：植物类的配置
  - `default_size`：默认显示尺寸
  - `specific`：每个具体植物的配置
- **zombies**：僵尸类的配置
- **bullets**：子弹类的配置
- **ui**：UI 元素的配置
- **sun**：阳光的配置
- **effects**：特效的配置

### 2. 核心函数（tool.py）

- `loadDisplayConfig()`：加载显示配置
- `getDisplayConfig(category, name)`：获取指定对象的配置
- `detect_image_scale(sheet, json_width, json_height)`：检测图片倍率
- `apply_scale_mode(image, target_w, target_h, scale_mode, quality)`：应用缩放模式
- `get_image_hd(...)`：智能图片加载函数，替代原有的 `get_image()`

## 使用方法

### 方法 1：替换高清图片（最简单）

如果您的高清图片**比例正确**（与原图比例一致），直接替换即可：

```bash
# 1. 备份原图（可选）
cp -r resources/graphics resources/graphics_backup

# 2. 替换为高清图片（保持文件名和目录结构不变）
# 例如将 2x 高清图片放入对应目录
cp your_hd_images/Zombie_0.png resources/graphics/Zombies/Zombie/

# 3. 运行游戏
python main.py
```

**系统会自动**：
- 检测图片倍率（2x、3x、4x）
- 缩放到游戏逻辑尺寸
- 保持图片比例

### 方法 2：调整图片显示尺寸

如果您想调整某个对象的显示大小，编辑 `display_config.json`：

**示例 1：调大向日葵**

```json
{
  "plants": {
    "specific": {
      "SunFlower": {
        "width": 90,     // 原来是 73，现在改为 90
        "height": 90,    // 原来是 74，现在改为 90
        "scale_mode": "keep_ratio"
      }
    }
  }
}
```

**示例 2：调整所有植物的默认尺寸**

```json
{
  "plants": {
    "default_size": {"width": 100, "height": 100},  // 改为 100x100
    "specific": {
      // 只有需要特殊尺寸的植物才在这里配置
    }
  }
}
```

### 方法 3：处理比例不对的图片

如果您的高清图片**比例不对**（例如原图是 1:1.5，高清图是 1:2），可以选择三种缩放模式：

#### 1. keep_ratio（保持比例，推荐）

图片会保持原始比例，可能会有透明边界。

```json
{
  "zombies": {
    "specific": {
      "Zombie": {
        "width": 90,
        "height": 120,
        "scale_mode": "keep_ratio"  // 保持原图比例
      }
    }
  }
}
```

**效果**：如果原图是 300x600（1:2），目标是 90x120（3:4），会缩放为 60x120（保持 1:2），左右有透明边。

#### 2. stretch（强制拉伸）

图片会强制拉伸到目标尺寸，可能轻微变形。

```json
{
  "zombies": {
    "specific": {
      "Zombie": {
        "width": 90,
        "height": 120,
        "scale_mode": "stretch"  // 强制拉伸
      }
    }
  }
}
```

**效果**：图片会强制变为 90x120，可能会变形。

#### 3. cover（覆盖裁剪）

图片会覆盖整个目标区域，多余部分会被裁剪。

```json
{
  "zombies": {
    "specific": {
      "Zombie": {
        "width": 90,
        "height": 120,
        "scale_mode": "cover"  // 覆盖裁剪
      }
    }
  }
}
```

**效果**：图片会缩放到覆盖 90x120，多余部分（上下或左右）会被裁掉。

### 方法 4：调整缩放质量

如果游戏加载慢，可以改为快速缩放：

```json
{
  "default": {
    "scale_mode": "keep_ratio",
    "quality": "fast"  // 改为 "fast"（原来是 "smooth"）
  }
}
```

- **smooth**：高质量，使用 `smoothscale`，稍慢
- **fast**：快速，使用 `scale`，较快

## 配置示例

### 完整的配置文件示例

```json
{
  "default": {
    "scale_mode": "keep_ratio",
    "quality": "smooth"
  },
  "plants": {
    "default_size": {"width": 80, "height": 80},
    "scale_mode": "keep_ratio",
    "specific": {
      "SunFlower": {"width": 90, "height": 90},
      "Peashooter": {"width": 71, "height": 71},
      "WallNut": {"width": 70, "height": 80}
    }
  },
  "zombies": {
    "default_size": {"width": 90, "height": 120},
    "scale_mode": "keep_ratio",
    "specific": {
      "Zombie": {"width": 115, "height": 120}
    }
  },
  "ui": {
    "specific": {
      "cards": {
        "width": 64,
        "height": 90,
        "scale_mode": "keep_ratio"
      },
      "menubar": {
        "width": 522,
        "height": 87,
        "scale_mode": "keep_ratio"
      },
      "panel": {
        "width": 465,
        "height": 513,
        "scale_mode": "keep_ratio"
      },
      "movebar": {
        "width": 516,
        "height": 86,
        "scale_mode": "keep_ratio"
      }
    }
  }
}
```

**重要**：配置文件中的尺寸是当前游戏资源的原始尺寸。如果您替换了高清图片，这些尺寸会作为"标准尺寸"参考，系统会自动检测实际图片的倍率并缩放回这个尺寸。

## 测试

运行测试脚本验证功能：

```bash
python test_hd.py
```

测试内容包括：
- 配置文件加载
- 新增函数检查
- 配置查询
- 倍率检测
- 缩放模式

## 常见问题

### Q1: 如何知道我的高清图片是几倍的？

**A**: 系统会自动检测。例如：
- 原图 JSON 配置：100x150
- 实际图片：200x300 → 检测为 2x
- 实际图片：300x450 → 检测为 3x
- 实际图片：400x600 → 检测为 4x

允许 ±20% 误差，所以 190x290 也会被识别为 2x。

### Q2: 我的图片比例不对怎么办？

**A**: 使用三种缩放模式之一：
- 如果希望**不变形**：使用 `keep_ratio`（可能有透明边）
- 如果**不介意轻微变形**：使用 `stretch`
- 如果希望**裁剪多余部分**：使用 `cover`

### Q3: 如何批量调整所有植物的大小？

**A**: 修改 `default_size`：

```json
{
  "plants": {
    "default_size": {"width": 100, "height": 100}  // 所有植物默认 100x100
  }
}
```

只有需要特殊尺寸的植物才在 `specific` 中单独配置。

### Q4: 低清图片和高清图片能混用吗？

**A**: 可以。系统会独立检测每个图片的倍率。

### Q5: 游戏变慢了怎么办？

**A**: 改为快速缩放模式：

```json
{
  "default": {
    "quality": "fast"
  }
}
```

### Q6: 修改配置后需要重启游戏吗？

**A**: 是的，配置文件在游戏启动时加载，修改后需要重启游戏。

## 技术细节

### 倍率检测原理

系统会比较实际图片尺寸和 JSON 配置的尺寸：

```
实际尺寸 / JSON 尺寸 = 倍率
```

允许 ±20% 误差以容忍透明边界。

### 缩放模式对比

| 模式 | 优点 | 缺点 | 适用场景 |
|------|------|------|---------|
| keep_ratio | 不变形 | 可能有透明边 | 大部分情况（推荐） |
| stretch | 填满整个区域 | 可能变形 | 比例差异小的情况 |
| cover | 填满 + 不变形 | 可能裁掉边缘 | 比例差异大且不希望变形 |

### 性能优化

- 倍率检测只在加载时执行一次
- 缩放后的图片会被 Pygame 缓存
- 使用 smoothscale 仅在降采样 ≥2x 时

## 升级路径

### 从低清到高清

1. 准备高清图片（2x 或 3x）
2. 保持文件名和目录结构不变
3. 直接替换到 `resources/graphics/` 对应目录
4. 运行游戏测试

### 从高清回到低清

1. 从备份恢复：`cp -r resources/graphics_backup/* resources/graphics/`
2. 或者直接替换为低清图片
3. 系统会自动检测为 1x

## 文件修改记录

本次更新修改了以下文件：

1. **新增**：`source/data/entity/display_config.json` - 显示配置
2. **修改**：`source/tool.py` - 添加高清化函数
3. **修改**：`source/component/plant.py` - 植物加载使用 get_image_hd
4. **修改**：`source/component/zombie.py` - 僵尸加载使用 get_image_hd
5. **修改**：`source/component/menubar.py` - UI 元素加载使用 get_image_hd
6. **新增**：`test_hd.py` - 高清化功能测试脚本

## 总结

通过这次更新，您可以：

1. ✅ 只需提供一套高清图片（2x、3x 或 4x）
2. ✅ 系统自动检测倍率并缩放到正确尺寸
3. ✅ 图片比例不对也能自动调整（keep_ratio/stretch/cover）
4. ✅ 在一个 JSON 文件中统一管理所有对象的显示尺寸
5. ✅ 低清和高清图片可以混用
6. ✅ 不影响游戏逻辑（碰撞、速度等）
7. ✅ 窗口最大化时画质清晰（Pygame SCALED 已支持）

开始享受高清游戏体验吧！
