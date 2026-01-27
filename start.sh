#!/bin/bash

# 跨平台一键启动脚本
# 支持: Windows (Git Bash/MSYS2), macOS, Linux

# 检测操作系统
detect_os() {
    case "$(uname -s)" in
        Linux*)     OS="Linux";;
        Darwin*)    OS="Mac";;
        CYGWIN*|MINGW*|MSYS*)    OS="Windows";;
        *)          OS="Unknown";;
    esac
}

detect_os

# 设置颜色（检测终端支持）
if [ -t 1 ] && command -v tput &> /dev/null && [ "$(tput colors)" -ge 8 ]; then
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    RED='\033[0;31m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    GREEN=''
    YELLOW=''
    RED=''
    BLUE=''
    NC=''
fi

# 清屏
clear

echo "═══════════════════════════════════════════════════"
echo "   植物大战僵尸 - 疯狂模式 🌻🧟"
echo "═══════════════════════════════════════════════════"
echo ""
echo -e "${BLUE}检测到系统: ${OS}${NC}"
echo ""

# 检查 Python 是否安装
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo -e "${RED}[错误]${NC} 未检测到 Python，请先安装 Python 3.7+"
    echo ""
    echo "安装方法："
    if [ "$OS" = "Mac" ]; then
        echo "  brew install python3"
    elif [ "$OS" = "Linux" ]; then
        echo "  sudo apt install python3 python3-pip  # Debian/Ubuntu"
        echo "  sudo yum install python3 python3-pip  # CentOS/RHEL"
    elif [ "$OS" = "Windows" ]; then
        echo "  访问 https://www.python.org/downloads/"
    fi
    exit 1
fi

# 使用 python3 或 python
if command -v python3 &> /dev/null; then
    PYTHON=python3
    PIP=pip3
else
    PYTHON=python
    PIP=pip
fi

echo -e "${GREEN}[✓]${NC} Python 环境已就绪"
echo ""

# 检查依赖
echo "正在检查游戏依赖..."
if ! $PYTHON -c "import pygame" &> /dev/null; then
    echo -e "${YELLOW}[!]${NC} 缺少 pygame 依赖，正在安装..."
    $PIP install pygame requests
fi

if ! $PYTHON -c "import flask" &> /dev/null; then
    echo -e "${YELLOW}[!]${NC} 缺少 Flask 依赖（服务端），正在安装..."
    cd server
    $PIP install -r requirements.txt
    cd ..
fi

echo -e "${GREEN}[✓]${NC} 所有依赖已就绪"
echo ""

# 显示菜单
echo "请选择启动模式："
echo ""
echo "  ${BLUE}[1]${NC} 完整在线模式（推荐）- 包含排行榜和数据统计"
echo "  ${BLUE}[2]${NC} 离线模式 - 无需服务器，单机游戏"
echo "  ${BLUE}[3]${NC} 仅启动服务器"
echo "  ${BLUE}[4]${NC} 退出"
echo ""

read -p "请输入选项 (1-4): " choice

case $choice in
    1)
        echo ""
        echo "═══════════════════════════════════════════════════"
        echo "   正在启动完整在线模式..."
        echo "═══════════════════════════════════════════════════"
        echo ""
        echo "[1/2] 正在启动游戏服务器..."

        # 启动服务器（后台运行）
        $PYTHON start_server.py > server.log 2>&1 &
        SERVER_PID=$!

        # 等待服务器启动
        echo "等待服务器启动..."
        sleep 3

        echo "[2/2] 正在启动游戏客户端..."
        echo ""
        echo -e "${YELLOW}提示：${NC}关闭游戏窗口后，服务器将自动停止"
        echo ""

        # 启动游戏
        $PYTHON start_game.py

        # 游戏结束后停止服务器
        echo ""
        echo "正在停止服务器..."

        # 跨平台停止进程
        if [ "$OS" = "Windows" ]; then
            # Windows 下使用 taskkill
            taskkill //PID $SERVER_PID //F 2>/dev/null || kill $SERVER_PID 2>/dev/null
        else
            # Unix 系统使用 kill
            kill $SERVER_PID 2>/dev/null
        fi

        # 确保服务器进程已停止
        sleep 1
        echo -e "${GREEN}服务器已停止${NC}"
        ;;
    2)
        echo ""
        echo "═══════════════════════════════════════════════════"
        echo "   正在启动离线模式..."
        echo "═══════════════════════════════════════════════════"
        echo ""
        $PYTHON main.py
        ;;
    3)
        echo ""
        echo "═══════════════════════════════════════════════════"
        echo "   正在启动游戏服务器..."
        echo "═══════════════════════════════════════════════════"
        echo ""
        echo -e "服务器地址: ${GREEN}http://localhost:5000${NC}"
        echo "按 Ctrl+C 停止服务器"
        echo ""
        $PYTHON start_server.py
        ;;
    4)
        echo "退出"
        exit 0
        ;;
    *)
        echo -e "${RED}[错误]${NC} 无效选项，请重新运行脚本"
        exit 1
        ;;
esac

echo ""
echo "游戏已关闭，感谢游玩！"
sleep 2

# 清理临时文件
if [ -f "server.log" ]; then
    rm -f server.log 2>/dev/null
fi

