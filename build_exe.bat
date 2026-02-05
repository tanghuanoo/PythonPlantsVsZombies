@echo off
chcp 65001 >nul
echo ========================================
echo   植物大战僵尸 - 打包工具
echo ========================================
echo.
echo   [1] 离线版（仅游戏，无需服务端）
echo   [2] 在线版（游戏 + 服务端，支持排行榜）
echo.
set /p choice="请选择打包方式 (1/2): "

if "%choice%"=="1" goto MODE_OFFLINE
if "%choice%"=="2" goto MODE_ONLINE
echo [错误] 无效选择
pause
exit /b 1

:CHECK_ENV
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python
    pause
    exit /b 1
)
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [提示] 正在安装 PyInstaller...
    pip install pyinstaller
    if errorlevel 1 (
        echo [错误] PyInstaller 安装失败
        pause
        exit /b 1
    )
)
goto :eof

:CLEAN
echo [1/3] 清理旧的构建文件...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
goto :eof

:MODE_OFFLINE
call :CHECK_ENV
call :CLEAN
echo [2/3] 开始打包（离线版）...
echo.
pyinstaller PlantsVsZombies.spec --noconfirm
if errorlevel 1 goto BUILD_FAIL
echo.
echo [3/3] 打包完成！
echo.
echo 输出: dist\PlantsVsZombies\PlantsVsZombies.exe
goto DONE

:MODE_ONLINE
call :CHECK_ENV
call :CLEAN
echo [2/3] 开始打包（在线版）...
echo.
pyinstaller PlantsVsZombies.spec --noconfirm
if errorlevel 1 goto BUILD_FAIL
echo      复制服务端文件...
mkdir "dist\PlantsVsZombies\server" >nul 2>&1
xcopy /s /e /q "server\*.py" "dist\PlantsVsZombies\server\" >nul
xcopy /s /e /q "server\static" "dist\PlantsVsZombies\server\static\" >nul
copy /y "start_server.py" "dist\PlantsVsZombies\" >nul
echo @echo off> "dist\PlantsVsZombies\启动服务端.bat"
echo chcp 65001 ^>nul>> "dist\PlantsVsZombies\启动服务端.bat"
echo python start_server.py>> "dist\PlantsVsZombies\启动服务端.bat"
echo pause>> "dist\PlantsVsZombies\启动服务端.bat"
echo.
echo [3/3] 打包完成！
echo.
echo 游戏: dist\PlantsVsZombies\PlantsVsZombies.exe
echo 服务端: dist\PlantsVsZombies\启动服务端.bat
goto DONE

:BUILD_FAIL
echo.
echo [错误] 打包失败，请检查错误信息
pause
exit /b 1

:DONE
echo.
echo ========================================
set /p open_dir="是否打开输出目录? (Y/N): "
if /i "%open_dir%"=="Y" explorer "dist\PlantsVsZombies"
pause
