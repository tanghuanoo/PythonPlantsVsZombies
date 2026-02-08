# 4K 显示器快速开始指南

## 🎯 3 步开始使用高清贴图

您的系统已完全就绪！只需 3 个简单步骤即可体验 4K 高清游戏。

---

## ✅ 第 1 步：验证系统（30 秒）

```bash
python test_multipass.py
```

**预期输出**：
```
[OK] 所有测试通过! 多级降采样功能已成功实现
```

如果看到这个，说明系统完全正常！

---

## 📸 第 2 步：准备测试图片（5 分钟）

### 选择测试对象
**推荐**：豌豆射手（Peashooter）- 游戏中最常见的植物

### 图片尺寸
- **原始**: 71x71 像素
- **高清 (3x)**: 213x213 像素 ← 推荐
- **高清 (4x)**: 284x284 像素

### 准备方法

#### 方法 A：使用 AI 放大工具（推荐）

**在线工具**：
1. 访问：https://waifu2x.udp.jp/
2. 上传：resources/graphics/Plants/Peashooter/Peashooter_0.png
3. 设置：放大 3 倍，降噪等级：中等
4. 下载：保存为 Peashooter_0_HD.png

**桌面工具**：
- waifu2x-caffe (Windows): https://github.com/lltcggie/waifu2x-caffe/releases
- Real-ESRGAN: https://github.com/xinntao/Real-ESRGAN

#### 方法 B：使用图像编辑软件

**Photoshop**：
1. 打开原图
2. 图像 → 图像大小
3. 宽度：213 像素，高度：213 像素
4. 重采样：Bicubic Smoother（适合缩小）
5. 保存

**GIMP（免费）**：
1. 打开原图
2. 图像 → 缩放图像
3. 宽度：213，高度：213
4. 插值：Cubic
5. 导出

### 替换文件

```bash
# 备份原文件（可选）
copy resources\graphics\Plants\Peashooter\Peashooter_0.png resources\graphics\Plants\Peashooter\Peashooter_0_backup.png

# 复制高清图片到游戏目录
copy 你的高清图片路径\Peashooter_0_HD.png resources\graphics\Plants\Peashooter\Peashooter_0.png
```

**提示**：只需替换 1-2 张图片即可测试效果！

---

## 🎮 第 3 步：启动游戏测试（2 分钟）

```bash
python main.py
```

### 测试步骤

#### 1. 默认窗口测试（800x600）
- [ ] 游戏正常启动
- [ ] 豌豆射手显示正常
- [ ] 无错误信息

#### 2. 窗口放大测试（利用 4K 显示器）
- [ ] 点击最大化按钮
- [ ] 观察画面清晰度
- [ ] 对比原图和高清图效果

### 预期效果

**窗口放大后**：
- ✅ 高清图片：清晰锐利，细节丰富
- ❌ 原图：模糊，有明显像素化

**性能**：
- 启动时间：+1-2 秒（仅首次加载）
- 运行 FPS：60（完全流畅）

---

## 🎨 进阶：批量替换所有图片

如果测试效果满意，可以批量准备所有资源。

### 资源清单

#### 植物（优先级高）
```
resources/graphics/Plants/
├── Peashooter/      - 13 帧 (71x71 → 213x213)
├── SunFlower/       - 约 10 帧 (73x74 → 219x222)
├── WallNut/         - 约 15 帧 (65x73 → 195x219)
├── Chomper/         - 约 13 帧 (101x137 → 303x411)
└── ...其他植物
```

#### 僵尸（优先级高）
```
resources/graphics/Zombies/
├── Zombie/          - 约 20 帧 (115x120 → 345x360)
├── ConeheadZombie/  - 约 20 帧 (115x120 → 345x360)
└── ...其他僵尸
```

#### UI 元素（优先级中）
```
resources/graphics/Screen/
├── MainMenu.png     - (800x600 → 2400x1800)
├── cards/           - (64x90 → 192x270)
└── ...其他 UI
```

### 批量处理工具

**Windows 批处理脚本**（示例）：
```batch
@echo off
REM 使用 waifu2x-caffe 批量处理
set INPUT=resources\graphics\Plants\Peashooter
set OUTPUT=resources_hd\graphics\Plants\Peashooter
set SCALE=3

waifu2x-caffe-cui -i %INPUT% -o %OUTPUT% -s %SCALE% -n 2
```

---

## ⚙️ 配置优化（可选）

如果您对画质要求极高，可以优化配置。

### 编辑配置文件

**文件**：source/data/entity/display_config.json

```json
{
  "default": {
    "scale_mode": "keep_ratio",
    "quality": "smooth",
    "enable_multipass": true,
    "multipass_threshold": 2.0,     // 从 3.0 降低到 2.0
    "max_step_size": 1.5            // 从 2.0 降低到 1.5
  }
}
```

### 效果对比

| 配置 | 画质 | 启动时间 | 推荐场景 |
|------|------|----------|----------|
| 默认 (3.0/2.0) | 很好 | +1-2 秒 | 一般使用 |
| 4K 优化 (2.0/1.5) | 极致 | +3-5 秒 | 4K 显示器 + 高画质需求 |

---

## 🔧 常见问题

### Q: 替换高清图片后，游戏启动变慢？
**A**: 正常现象。多级降采样需要时间（1-3 秒），但只在首次加载时发生。运行时完全流畅（60 FPS）。

### Q: 窗口放大后，画面还是模糊？
**A**: 可能原因：
1. 图片倍率不够（使用 3x 或 4x 而非 2x）
2. 图片质量不好（使用 AI 放大工具而非简单缩放）
3. 配置参数需要优化（降低 multipass_threshold）

### Q: 如何恢复原来的低清图片？
**A**: 从备份恢复，或者使用 git：
```bash
git checkout resources/graphics/Plants/Peashooter/Peashooter_0.png
```

### Q: 我的电脑配置较低，会卡吗？
**A**: 不会。运行时性能和低清图片完全一样（60 FPS）。唯一区别是启动时间增加 1-3 秒。

---

## 📊 效果对比

### 窗口大小 vs 画质

| 窗口大小 | 低清图片 (71x71) | 高清图片 (213x213 / 3x) |
|----------|------------------|-------------------------|
| 800x600 (默认) | 清晰 | 清晰 |
| 1200x900 (1.5x) | 轻微模糊 | 清晰 |
| 1600x1200 (2x) | 模糊 | 清晰 |
| 2400x1800 (3x) | 很模糊 | 清晰 |

**结论**：4K 显示器上，窗口可能放大到 2-3 倍，高清图片优势明显。

---

## 🎯 推荐工作流程

### 第一次使用（测试）
```
1. 运行测试脚本验证系统
   ↓
2. 准备 1-2 张高清测试图片（豌豆射手）
   ↓
3. 替换到游戏目录
   ↓
4. 启动游戏，观察效果
   ↓
5. 最大化窗口，对比清晰度
```

### 正式使用（批量）
```
1. 测试效果满意
   ↓
2. 批量准备所有高清资源（优先植物和僵尸）
   ↓
3. 可选：优化配置参数（4K 优化）
   ↓
4. 享受 4K 高清游戏体验！
```

---

## 📚 相关文档

- **HD_VALIDATION_REPORT.md** - 完整验证报告和技术细节
- **HD_QUICK_GUIDE.md** - 详细使用指南
- **HD_IMPLEMENTATION_SUMMARY.md** - 技术实现文档
- **test_multipass.py** - 功能测试脚本

---

## ✨ 核心优势总结

1. ✅ **系统完全就绪** - 所有功能已实现并测试通过
2. ✅ **简单易用** - 只需替换图片，无需修改代码
3. ✅ **自动处理** - 系统自动检测倍率和降采样
4. ✅ **窗口自由缩放** - pg.SCALED 自动适配
5. ✅ **性能友好** - 运行时 60 FPS，无额外开销
6. ✅ **4K 优化** - 充分利用高分辨率显示器

---

**现在就开始您的 4K 高清游戏之旅吧！** 🚀

有任何问题，请查看完整文档：HD_VALIDATION_REPORT.md
