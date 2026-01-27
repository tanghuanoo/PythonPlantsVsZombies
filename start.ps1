# 植物大战僵尸 - PowerShell 启动脚本
# 支持 Windows PowerShell 5.1+ 和 PowerShell Core 7+

# 设置编码
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

# 设置颜色
function Write-ColorText {
    param(
        [string]$Text,
        [string]$Color = "White"
    )
    Write-Host $Text -ForegroundColor $Color
}

# 清屏
Clear-Host

Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   植物大战僵尸 - 疯狂模式 🌻🧟" -ForegroundColor Green
Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-ColorText "检测到系统: Windows (PowerShell)" "Blue"
Write-Host ""

# 检查 Python 是否安装
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} else {
    Write-ColorText "[错误] 未检测到 Python，请先安装 Python 3.7+" "Red"
    Write-Host ""
    Write-Host "下载地址: https://www.python.org/downloads/"
    Write-Host "安装时请勾选 'Add Python to PATH'"
    Write-Host ""
    Read-Host "按回车键退出"
    exit 1
}

Write-ColorText "[✓] Python 环境已就绪" "Green"
Write-Host ""

# 检查依赖
Write-Host "正在检查游戏依赖..."

# 检查 pygame
$pygameInstalled = & $pythonCmd -c "import pygame" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-ColorText "[!] 缺少 pygame 依赖，正在安装..." "Yellow"
    & $pythonCmd -m pip install pygame requests
}

# 检查 Flask
$flaskInstalled = & $pythonCmd -c "import flask" 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-ColorText "[!] 缺少 Flask 依赖（服务端），正在安装..." "Yellow"
    Push-Location server
    & $pythonCmd -m pip install -r requirements.txt
    Pop-Location
}

Write-ColorText "[✓] 所有依赖已就绪" "Green"
Write-Host ""

# 显示菜单
Write-Host "请选择启动模式："
Write-Host ""
Write-ColorText "  [1] 完整在线模式（推荐）- 包含排行榜和数据统计" "Cyan"
Write-ColorText "  [2] 离线模式 - 无需服务器，单机游戏" "Cyan"
Write-ColorText "  [3] 仅启动服务器" "Cyan"
Write-ColorText "  [4] 退出" "Cyan"
Write-Host ""

$choice = Read-Host "请输入选项 (1-4)"

switch ($choice) {
    "1" {
        Write-Host ""
        Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host "   正在启动完整在线模式..." -ForegroundColor Green
        Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "[1/2] 正在启动游戏服务器..."

        # 启动服务器（后台运行）
        $serverProcess = Start-Process -FilePath $pythonCmd -ArgumentList "start_server.py" -PassThru -WindowStyle Normal -RedirectStandardOutput "server.log" -RedirectStandardError "server_error.log"

        Write-Host "等待服务器启动..."
        Start-Sleep -Seconds 3

        Write-Host "[2/2] 正在启动游戏客户端..."
        Write-Host ""
        Write-ColorText "提示：关闭游戏窗口后，服务器将自动停止" "Yellow"
        Write-Host ""

        # 启动游戏（前台运行）
        & $pythonCmd start_game.py

        # 游戏结束后停止服务器
        Write-Host ""
        Write-Host "正在停止服务器..."

        if ($serverProcess -and !$serverProcess.HasExited) {
            Stop-Process -Id $serverProcess.Id -Force -ErrorAction SilentlyContinue
        }

        Start-Sleep -Seconds 1
        Write-ColorText "服务器已停止" "Green"
    }
    "2" {
        Write-Host ""
        Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host "   正在启动离线模式..." -ForegroundColor Green
        Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host ""
        & $pythonCmd main.py
    }
    "3" {
        Write-Host ""
        Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host "   正在启动游戏服务器..." -ForegroundColor Green
        Write-Host "═══════════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host ""
        Write-ColorText "服务器地址: http://localhost:5000" "Green"
        Write-Host "按 Ctrl+C 停止服务器"
        Write-Host ""
        & $pythonCmd start_server.py
    }
    "4" {
        Write-Host "退出"
        exit 0
    }
    default {
        Write-ColorText "[错误] 无效选项，请重新运行脚本" "Red"
        exit 1
    }
}

Write-Host ""
Write-Host "游戏已关闭，感谢游玩！"
Start-Sleep -Seconds 2

# 清理临时文件
if (Test-Path "server.log") {
    Remove-Item "server.log" -Force -ErrorAction SilentlyContinue
}
if (Test-Path "server_error.log") {
    Remove-Item "server_error.log" -Force -ErrorAction SilentlyContinue
}
