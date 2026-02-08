# 配置文件尺寸说明

## 重要概念

`display_config.json` 中的 `width` 和 `height` 是**当前游戏资源的原始尺寸**（基准尺寸），而不是您要替换的高清图片的尺寸。

## 工作原理

1. **配置设定基准**：例如 `menubar width=522, height=87`
2. **检测图片倍率**：如果您的图片是 1044x174，系统检测为 2x
3. **自动缩放**：系统将 1044x174 自动缩放回 522x87 显示

## 示例说明

| 配置基准 | 您的图片（2x） | 检测倍率 | 最终显示 |
|---------|--------------|---------|---------|
| 522x87  | 1044x174     | 2.0x    | 522x87  |
| 522x87  | 1566x261     | 3.0x    | 522x87  |
| 522x87  | 522x87       | 1.0x    | 522x87  |

## 当前游戏的基准尺寸

以下是当前游戏资源的原始尺寸（已在 `display_config.json` 中正确设置）：

### UI 元素
- **MenuBar 背景** (ChooserBackground.png): 522 x 87
- **Panel 背景** (PanelBackground.png): 465 x 513
- **MoveBar 背景** (MoveBackground.png): 516 x 86
- **卡片** (card_*.png): 64 x 90

### 植物
- **SunFlower** (向日葵): 73 x 74
- **Peashooter** (豌豆射手): 71 x 71
- **WallNut** (坚果墙): 65 x 73
- **Chomper** (大嘴花): 100 x 114

### 僵尸
- **Zombie** (普通僵尸): 115 x 120
- **ConeheadZombie** (路障僵尸): 115 x 120
- **BucketheadZombie** (铁桶僵尸): 115 x 120

### 子弹
- **PeaNormal** (普通豌豆): 28 x 34
- **PeaIce** (冰冻豌豆): 30 x 34

## 如何调整显示大小

### 场景 1：替换高清图片后大小合适
无需修改配置，系统会自动检测倍率并缩放到基准尺寸。

### 场景 2：替换高清图片后显示太大
减小配置中的基准尺寸：

```json
{
  "zombies": {
    "specific": {
      "Zombie": {
        "width": 90,    // 从 115 改为 90
        "height": 100   // 从 120 改为 100
      }
    }
  }
}
```

### 场景 3：替换高清图片后显示太小
增大配置中的基准尺寸：

```json
{
  "plants": {
    "specific": {
      "Peashooter": {
        "width": 85,    // 从 71 改为 85
        "height": 85    // 从 71 改为 85
      }
    }
  }
}
```

### 场景 4：图片比例不对
选择合适的缩放模式：

```json
{
  "zombies": {
    "specific": {
      "Zombie": {
        "width": 115,
        "height": 120,
        "scale_mode": "cover"  // keep_ratio / stretch / cover
      }
    }
  }
}
```

- **keep_ratio**：保持原图比例（推荐，不会变形）
- **stretch**：强制拉伸（可能变形）
- **cover**：覆盖裁剪（不变形但裁边）

## 快速验证

运行验证脚本查看当前配置：

```bash
python verify_ui_config.py
```

这会显示所有 UI 元素的配置是否匹配原始图片尺寸。

## 调整流程

1. **替换高清图片**到 `resources/graphics/` 目录
2. **运行游戏**查看效果
3. 如果大小不合适，**修改** `display_config.json` 中的 width/height
4. **重启游戏**查看新效果
5. 重复步骤 3-4 直到满意

## 注意事项

- 修改配置后需要**重启游戏**才能生效
- 配置中的尺寸是**最终显示尺寸**，不是高清图片尺寸
- 系统会自动检测高清图片倍率，您只需关心最终显示效果
- 建议先用 `keep_ratio` 模式，如果有问题再尝试其他模式
