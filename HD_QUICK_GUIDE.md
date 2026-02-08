# 高清图片使用快速指南

## 快速开始 (3 步)

### 1. 准备高清图片
- 建议倍率: 2x-3x (例如: 原图 64x90 → 高清图 192x270 或 256x360)
- 支持任意比例 (系统会自动调整)
- 文件名保持不变 (直接替换原文件)

### 2. 替换图片
```
resources/graphics/
├── Plants/
│   ├── Peashooter/
│   │   ├── Peashooter_0.png  ← 替换为高清版本
│   │   ├── Peashooter_1.png  ← 替换为高清版本
│   │   └── ...
│   └── ...
├── Zombies/
│   └── ...
└── Screen/
    └── ...
```

### 3. 运行游戏
```bash
python main.py
```

就这么简单! 系统会自动:
- 检测图片倍率 (1x, 2x, 3x, 4x)
- 使用多级降采样缩放到正确尺寸
- 自动适配比例

## 常见问题

### Q1: 我的图片比例不对怎么办?
**A**: 不用担心! 编辑 `source/data/entity/display_config.json`:

```json
{
  "plants": {
    "specific": {
      "Peashooter": {
        "scale_mode": "keep_ratio"  // 保持比例 (推荐)
        // 或 "stretch" (拉伸) 或 "cover" (裁剪)
      }
    }
  }
}
```

### Q2: 图片显示太大或太小?
**A**: 调整配置中的 width 和 height:

```json
{
  "plants": {
    "specific": {
      "Peashooter": {
        "width": 100,   // 原来是 71，现在调大到 100
        "height": 100
      }
    }
  }
}
```

### Q3: 图片还是有锯齿?
**A**: 调整降采样参数，提高质量:

```json
{
  "default": {
    "multipass_threshold": 2.0,  // 降低阈值 (原来 3.0)
    "max_step_size": 1.5         // 减小步长 (原来 2.0)
  }
}
```

### Q4: 游戏启动太慢?
**A**: 调整降采样参数，提高性能:

```json
{
  "default": {
    "multipass_threshold": 5.0,  // 提高阈值
    "max_step_size": 2.5         // 增大步长
  }
}
```

## 缩放模式对比

### keep_ratio (保持比例) - 推荐
```
原图: 200x300 (比例 2:3)
目标: 100x100 (比例 1:1)
结果: 67x100 (保持 2:3，适配高度)

优点: 不变形
缺点: 可能有透明边
```

### stretch (拉伸)
```
原图: 200x300 (比例 2:3)
目标: 100x100 (比例 1:1)
结果: 100x100 (强制拉伸为 1:1)

优点: 填满目标尺寸
缺点: 可能轻微变形
```

### cover (覆盖裁剪)
```
原图: 200x300 (比例 2:3)
目标: 100x100 (比例 1:1)
结果: 100x100 (缩放到 67x100 后裁剪上下)

优点: 不变形且填满
缺点: 可能裁掉边缘
```

## 配置模板

### 游戏整体使用高清图 (平衡模式)
```json
{
  "default": {
    "scale_mode": "keep_ratio",
    "quality": "smooth",
    "enable_multipass": true,
    "multipass_threshold": 3.0,
    "max_step_size": 2.0
  }
}
```

### 追求极致画质
```json
{
  "default": {
    "scale_mode": "keep_ratio",
    "quality": "smooth",
    "enable_multipass": true,
    "multipass_threshold": 2.0,   // 更低阈值
    "max_step_size": 1.5          // 更小步长
  }
}
```

### 追求快速性能
```json
{
  "default": {
    "scale_mode": "keep_ratio",
    "quality": "fast",            // 快速模式
    "enable_multipass": true,
    "multipass_threshold": 5.0,   // 更高阈值
    "max_step_size": 2.5          // 更大步长
  }
}
```

## 批量调整示例

### 所有植物统一调大 20%
```json
{
  "plants": {
    "default_size": {
      "width": 96,   // 原来 80 × 1.2
      "height": 96
    }
  }
}
```

### 特定僵尸单独调整
```json
{
  "zombies": {
    "specific": {
      "Zombie": {
        "width": 110,
        "height": 130
      },
      "ConeheadZombie": {
        "width": 100,
        "height": 140
      }
    }
  }
}
```

### UI 元素使用拉伸模式
```json
{
  "ui": {
    "specific": {
      "MainMenu": {
        "width": 1600,
        "height": 1200,
        "scale_mode": "stretch"  // 背景图强制拉伸填满
      }
    }
  }
}
```

## 测试检查清单

在替换高清图后，测试以下项目:

- [ ] 运行 `python test_multipass.py` 确认功能正常
- [ ] 启动游戏，检查窗口大小 (1600x1200)
- [ ] 观察植物、僵尸、UI 是否清晰
- [ ] 检查锯齿是否明显减少
- [ ] 测试游戏性能 (FPS 是否稳定 60)
- [ ] 检查不同关卡的图片显示
- [ ] 测试窗口缩放功能

## 支持的图片格式

- PNG (推荐，支持透明)
- JPG (较小文件)
- BMP
- GIF

## 注意事项

1. **备份原图**: 替换前备份到 `resources/graphics_backup/`
2. **统一倍率**: 建议所有图片使用相同倍率 (2x 或 3x)
3. **文件大小**: 高清图会增大文件，注意磁盘空间
4. **透明背景**: 确保 PNG 图片保留透明通道

## 获取帮助

遇到问题查看:
- `HD_IMPLEMENTATION_SUMMARY.md` - 详细技术文档
- `test_multipass.py` - 测试脚本

或检查:
- `source/data/entity/display_config.json` - 配置文件
- `source/tool.py` - 核心代码

---

**提示**: 修改配置后需要重启游戏才能生效
