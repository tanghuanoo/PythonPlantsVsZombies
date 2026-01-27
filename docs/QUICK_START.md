# 快速部署清单

## 安装步骤

### 1. 安装客户端依赖

```bash
pip install pygame==1.9.6 requests>=2.25.0
```

或使用 requirements.txt：

```bash
pip install -r requirements.txt
```

### 2. 安装服务端依赖

```bash
cd server
pip install Flask>=2.0.0 Flask-CORS>=3.0.0
```

或使用 requirements.txt：

```bash
cd server
pip install -r requirements.txt
cd ..
```

## 启动步骤

### 🚀 方式A：一键启动（最简单）

**Windows / macOS / Linux 通用**

```bash
# 首次使用（添加执行权限）
chmod +x start.sh

# 启动脚本
./start.sh
```

**Windows 用户**: 在项目文件夹右键选择 "Git Bash Here"，然后运行上述命令

脚本会自动：
- ✅ 检测操作系统
- ✅ 检测并安装依赖
- ✅ 提供图形化菜单选择启动模式
- ✅ 自动管理服务器进程

---

### 方式B：完整在线模式（手动）

**终端1 - 启动服务器：**

```bash
python start_server.py
```

输出应显示：

```
Starting server on 0.0.0.0:5000
Access the server at http://0.0.0.0:5000
Press Ctrl+C to stop the server
```

**终端2 - 启动游戏：**

```bash
python start_game.py
```

### 方式C：离线模式（手动）

```bash
python main.py
```

游戏会自动进入离线模式。

## 验证安装

运行验证脚本：

```bash
python test_setup.py
```

应看到：

```
[OK] constants
[OK] config.ini
[OK] level_0.json
[SUCCESS] All tests passed!
```

## 配置服务器地址（局域网部署）

1. 在服务器机器上启动服务端
2. 记录服务器IP（例如：192.168.1.100）
3. 在客户端机器上编辑 `source/config.ini`：

```ini
[Server]
url = http://192.168.1.100:5000
timeout = 5
```

4. 启动游戏客户端

## 游戏控制

- **Tab键**：切换输入框（登录页面）
- **回车键**：提交登录
- **鼠标点击**：所有其他操作

## 常见问题

### Q: 提示 "No module named 'pygame'"

**A:** 安装 pygame：

```bash
pip install pygame==1.9.6
```

### Q: 提示 "No module named 'flask'"

**A:** 安装 Flask（仅服务端需要）：

```bash
pip install Flask Flask-CORS
```

### Q: 无法连接到服务器

**A:**
1. 检查服务器是否启动
2. 检查防火墙设置
3. 确认服务器地址配置正确
4. 游戏会自动进入离线模式

### Q: 中文显示乱码

**A:**
1. 确保系统安装了 SimHei 字体
2. 或修改代码使用其他中文字体

## 游戏流程

1. **Loading页面**（10秒）
2. **登录页面**（输入姓名和工号）
3. **主菜单**（点击 Adventure）
4. **疯狂模式**（120秒）
   - 初始阳光：1000
   - 右上角显示：分数、时间、击杀数
5. **游戏报告**
   - 显示分数、排名、击杀统计
   - 可导出截图、再来一局、退出

## 僵尸积分

| 僵尸 | 分数 |
|------|------|
| 普通僵尸 | 10 |
| 旗帜僵尸 | 15 |
| 报纸僵尸 | 20 |
| 锥形头僵尸 | 25 |
| 桶形头僵尸 | 50 |

## 文件结构

```
PythonPlantsVsZombies/
├── main.py                 # 主程序
├── start_game.py          # 游戏启动脚本
├── start_server.py        # 服务器启动脚本
├── test_setup.py          # 验证脚本
├── requirements.txt       # 客户端依赖
├── README_CRAZY_MODE.md   # 完整文档
├── source/
│   ├── config.ini         # 客户端配置
│   ├── language.py        # 多语言支持
│   ├── network.py         # 网络模块
│   ├── state/
│   │   ├── loading.py     # Loading页面
│   │   ├── login.py       # 登录页面
│   │   └── report.py      # 游戏报告
│   └── data/map/
│       ├── level_0.json   # 疯狂模式配置
│       └── level_crazy.json
└── server/
    ├── server.py          # Flask主程序
    ├── api.py             # API接口
    ├── database.py        # 数据库操作
    ├── models.py          # 数据模型
    ├── config.py          # 服务器配置
    └── requirements.txt   # 服务端依赖
```

## 性能优化建议

如果游戏卡顿，编辑 `source/data/map/level_0.json`：

```json
{
    "zombie_spawn_config": {
        "initial_interval": 5000,    // 增加初始间隔
        "min_interval": 2000,        // 增加最小间隔
        "interval_decrease_rate": 0.98  // 减慢加速度
    }
}
```

## 获取帮助

查看完整文档：`README_CRAZY_MODE.md`

查看实施总结：`IMPLEMENTATION_SUMMARY.md`

---

**开始游戏！祝您玩得愉快！** 🌻🧟‍♂️
