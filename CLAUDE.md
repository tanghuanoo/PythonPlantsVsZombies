# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个使用 Python 和 Pygame 实现的植物大战僵尸游戏克隆版本。游戏包含多种植物类型、僵尸类型和关卡模式。

## 运行和测试

### 启动游戏
```bash
python main.py
```

### 系统要求
- Python 3.7 (推荐，但不强制)
- Python-Pygame 1.9

## 代码架构

### 核心架构模式

项目使用**状态机模式**管理游戏流程：
- `tool.Control` 类是游戏主控制器，管理状态转换和事件循环
- `tool.State` 是所有游戏状态的抽象基类
- 游戏状态包括：主菜单 (MAIN_MENU)、关卡 (LEVEL)、胜利屏幕 (GAME_VICTORY)、失败屏幕 (GAME_LOSE)

### 目录结构

```
source/
├── main.py              # 游戏入口，初始化状态机
├── tool.py              # 核心工具类：Control、State、图像加载函数
├── constants.py         # 所有游戏常量定义
├── state/               # 游戏状态实现
│   ├── level.py         # 关卡状态（游戏主逻辑）
│   ├── mainmenu.py      # 主菜单状态
│   └── screen.py        # 胜利/失败屏幕
├── component/           # 游戏实体组件
│   ├── plant.py         # 植物类：Car、Bullet、Sun、各种植物
│   ├── zombie.py        # 僵尸类及其变种
│   ├── map.py           # 地图网格管理
│   └── menubar.py       # 植物卡片选择栏
└── data/                # 游戏数据文件
    ├── entity/          # 实体配置 (plant.json, zombie.json)
    └── map/             # 关卡配置 (level_0.json 至 level_5.json)
```

### 关键设计模式

**1. 精灵组管理（Pygame Sprite Groups）**
- `level.py` 中按地图行（map_y）组织精灵组
- 每行有独立的 plant_groups、zombie_groups、bullet_groups
- 这样设计便于碰撞检测和行级交互

**2. JSON 数据驱动**
- 关卡数据存储在 `source/data/map/level_X.json`
- 每个关卡定义：背景类型、初始阳光值、僵尸生成时间和位置
- 实体图像矩形信息存储在 `source/data/entity/` 中的 JSON 文件

**3. 帧动画系统**
- `tool.load_image_frames()` 从目录加载按编号排序的帧序列
- 所有精灵使用 `frames` 列表和 `frame_index` 实现动画
- 图像资源按层级目录组织在 `resources/graphics/` 下

### 核心游戏循环

1. **事件处理**（`tool.Control.event_loop()`）
   - 捕获鼠标点击和键盘输入
   - 鼠标位置和点击状态存储在 Control 实例中

2. **状态更新**（`tool.Control.update()`）
   - 调用当前状态的 `update()` 方法
   - 状态完成后通过 `flip_state()` 切换到下一个状态

3. **关卡状态**（`level.Level`）
   - 两个子状态：CHOOSE（选择植物卡片）和 PLAY（游戏进行中）
   - `setupGroups()` 创建多个精灵组用于不同实体类型
   - `setupZombies()` 根据时间线从 JSON 数据加载僵尸生成队列

### 坐标系统和网格

- 屏幕尺寸：800x600 像素
- 游戏地图：9x5 网格 (GRID_X_LEN × GRID_Y_LEN)
- 每个网格：80x100 像素 (GRID_X_SIZE × GRID_Y_SIZE)
- 背景偏移：`BACKGROUND_OFFSET_X = 220`
- 地图偏移：`MAP_OFFSET_X = 35`, `MAP_OFFSET_Y = 100`
- `map.Map` 类提供网格位置和像素坐标之间的转换方法

### 植物和僵尸系统

**植物特性：**
- 所有植物继承自 `pg.sprite.Sprite`
- 通过状态机控制行为（IDLE、ATTACK、DIGEST 等）
- 植物卡片有冷却时间（frozen_time）和阳光成本（sun_cost）
- 特殊植物：向日葵产生阳光、豌豆射手发射子弹、樱桃炸弹爆炸

**僵尸特性：**
- 有健康值、速度、伤害属性
- 支持装备系统（头盔、路障等）
- 失去头部后继续移动（losHead 状态）
- 冰冻减速机制（ice_slow_ratio）
- 特殊僵尸：报纸僵尸失去报纸后加速

### 关卡类型

通过修改 `source/constants.py` 中的 `START_LEVEL_NUM` 切换关卡：
- Level 1-2: 白昼模式（BACKGROUND_DAY）
- Level 3: 夜晚模式（BACKGROUND_NIGHT）
- Level 4: 传送带模式（CHOOSEBAR_MOVE）- 植物卡片自动刷新
- Level 5: 坚果保龄球模式（CHOSSEBAR_BOWLING）- 用坚果滚动攻击僵尸

### 资源加载

**图像资源：**
- `tool.load_all_gfx()` 递归加载 `resources/graphics/` 下所有图像
- 支持多帧动画（如 Peashooter_0.png, Peashooter_1.png...）
- 图像矩形数据从 JSON 加载，定义精灵的碰撞区域和显示区域

**资源组织：**
```
resources/graphics/
├── Screen/          # 菜单和屏幕图像
├── Plants/          # 植物动画帧
├── Zombies/         # 僵尸动画帧
└── ...
```

## 常见开发任务

### 添加新植物

1. 在 `constants.py` 定义植物名称常量和卡片常量
2. 在 `component/plant.py` 创建植物类
3. 在 `component/menubar.py` 的列表中添加卡片和植物信息
4. 在 `source/data/entity/plant.json` 添加图像矩形数据
5. 将植物图像帧放入 `resources/graphics/Plants/PlantName/` 目录

### 添加新僵尸

1. 在 `constants.py` 定义僵尸名称和健康值常量
2. 在 `component/zombie.py` 创建僵尸子类
3. 在 `source/data/entity/zombie.json` 添加图像矩形数据
4. 在关卡 JSON 文件的 zombie_list 中配置生成时间和位置

### 创建新关卡

1. 在 `source/data/map/` 创建 `level_X.json` 文件
2. 定义以下字段：
   - `background_type`: 0 (白昼) 或 1 (夜晚)
   - `init_sun_value`: 初始阳光值
   - `zombie_list`: 僵尸生成列表 `[{"time": 毫秒, "map_y": 行号, "name": "僵尸名"}]`
   - `choosebar_type` (可选): 选择栏类型
   - `card_pool` (可选): 可用植物卡片池

### 调试技巧

- 控制台会输出鼠标点击位置和状态（见 `tool.py:77`）
- 僵尸生成时间以毫秒为单位（游戏启动后的 current_time）
- 检查 `map.Map.isValid()` 确认网格坐标是否在有效范围内
- 使用 `state` 和 `done` 属性追踪实体状态机转换

## 代码约定

- 所有文件使用 `__author__ = 'marble_xu'` 标识
- 状态常量在 `constants.py` 中集中定义
- 使用 Pygame 的颜色键（colorkey）处理图像透明度
- 时间间隔使用毫秒为单位
- 网格坐标：(x, y) 其中 x 是列，y 是行
- 像素坐标：使用 Pygame 的 Rect 系统
