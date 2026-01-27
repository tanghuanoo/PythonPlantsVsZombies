# 植物大战僵尸疯狂模式

## 项目简介

这是一个基于 Python 和 Pygame 实现的植物大战僵尸疯狂模式改造版本。游戏特性：

- **2分钟计时疯狂模式**：固定120秒游戏时长，高频率僵尸生成
- **初始阳光1000**：快速开局
- **积分系统**：不同僵尸分配不同分数
- **联机排名系统**：局域网内排名
- **多语言支持**：中英文切换
- **Loading页面**：展示安全产品故事
- **游戏报告**：显示分数、排名、击杀统计

## 安装依赖

### 客户端依赖

```bash
pip install -r requirements.txt
```

### 服务端依赖

```bash
cd server
pip install -r requirements.txt
```

## 运行游戏

### 方式1：启动完整系统（服务端 + 客户端）

**步骤1：启动服务器**

```bash
python start_server.py
```

服务器将在 `http://0.0.0.0:5000` 上运行，可在局域网内访问。

**步骤2：启动游戏客户端**

在新的终端窗口中：

```bash
python start_game.py
```

或者直接运行：

```bash
python main.py
```

### 方式2：离线模式（仅客户端）

如果服务器未启动，游戏会自动进入离线模式（无排名功能）：

```bash
python start_game.py
```

## 游戏流程

1. **Loading页面**（约10秒）：显示安全产品故事，文字渐入效果
2. **登录页面**：输入姓名和工号
3. **主菜单**：点击 "Adventure" 开始游戏
4. **疯狂模式**（120秒）：
   - 初始阳光1000
   - 右上角显示分数、倒计时、击杀数
   - 僵尸高频率生成，间隔逐渐缩短
   - 击杀僵尸获得分数
5. **游戏报告页面**：
   - 显示最终分数、排名、击杀统计
   - 显示排行榜（在线模式）
   - 导出截图、再来一局、退出游戏

## 配置文件

### 客户端配置：`source/config.ini`

```ini
[Server]
url = http://localhost:5000
timeout = 5

[Game]
language = zh_CN
default_level = 0
```

### 服务端配置：`server/config.py`

```python
PORT = 5000
HOST = '0.0.0.0'
DATABASE_PATH = 'game.db'
DEBUG = True
```

## 僵尸积分表

| 僵尸类型 | 分数 |
|---------|------|
| 普通僵尸 (Zombie) | 10 |
| 旗帜僵尸 (FlagZombie) | 15 |
| 报纸僵尸 (NewspaperZombie) | 20 |
| 锥形头僵尸 (ConeheadZombie) | 25 |
| 桶形头僵尸 (BucketheadZombie) | 50 |

## 关卡配置

疯狂模式关卡配置文件：`source/data/map/level_0.json`

```json
{
    "background_type": 0,
    "init_sun_value": 1000,
    "game_mode": "crazy",
    "game_duration": 120000,
    "zombie_list": [],
    "zombie_spawn_config": {
        "initial_interval": 3000,
        "min_interval": 1000,
        "interval_decrease_rate": 0.95,
        "spawn_probability": {
            "Zombie": 0.4,
            "ConeheadZombie": 0.25,
            "BucketheadZombie": 0.15,
            "FlagZombie": 0.1,
            "NewspaperZombie": 0.1
        }
    }
}
```

## 系统要求

- Python 3.7+
- Pygame 1.9+
- requests 2.25+
- Flask 2.0+ (服务端)
- Flask-CORS 3.0+ (服务端)

## 局域网部署

### 服务端部署

1. 在服务器机器上启动服务端：

```bash
python start_server.py
```

2. 记录服务器 IP 地址（例如：192.168.1.100）

### 客户端配置

在每台客户端机器上，修改 `source/config.ini`：

```ini
[Server]
url = http://192.168.1.100:5000
timeout = 5
```

然后启动游戏：

```bash
python start_game.py
```

## 故障排除

### 问题1：无法连接到服务器

**解决方案**：
- 检查服务器是否启动
- 检查防火墙是否允许端口5000
- 确认客户端配置文件中的服务器 URL 正确
- 游戏会自动进入离线模式

### 问题2：中文显示乱码

**解决方案**：
- 确保系统安装了中文字体（SimHei）
- 在 loading.py 中修改字体为其他中文字体

### 问题3：游戏卡顿

**解决方案**：
- 降低僵尸生成频率（修改 level_0.json 中的 initial_interval）
- 增加最小生成间隔（min_interval）

## 开发说明

### 添加新关卡

1. 在 `source/data/map/` 创建 `level_X.json`
2. 设置 `game_mode: "crazy"` 启用疯狂模式
3. 配置僵尸生成参数

### 修改积分系统

编辑 `source/constants.py` 中的 `ZOMBIE_SCORES` 字典：

```python
ZOMBIE_SCORES = {
    NORMAL_ZOMBIE: 10,
    FLAG_ZOMBIE: 15,
    # ...
}
```

### 切换语言

游戏内点击登录页面的"语言"按钮，或修改配置文件：

```ini
[Game]
language = en_US  # 或 zh_CN
```

## 许可证

本项目基于原始植物大战僵尸游戏代码改造，仅供学习和研究使用。

## 作者

- 原作者: marble_xu
- 疯狂模式改造: Claude Code
