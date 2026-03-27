@echo off
chcp 65001 >nul
title 数据建模课程 - 环境配置

echo.
echo ============================================================
echo   数据建模课程 - 环境配置
echo ============================================================
echo.

REM ------------------------------------------------------------
REM 步骤 0: 验证当前目录
REM ------------------------------------------------------------
if not exist "requirements.txt" (
    echo [错误] 未找到 requirements.txt。
    echo 请在 DATA-MODELING-COURSE-STUDENT 目录下运行此脚本。
    pause
    exit /b 1
)
echo [成功] 已检测到课程根目录。
echo.

REM ------------------------------------------------------------
REM 步骤 1: 检查并安装 Python 3.13
REM ------------------------------------------------------------
echo [步骤 1] 正在检查 Python 3.13...

set "PYTHON_INSTALLED=0"
for /f "delims=" %%i in ('where python 2^>nul ^| findstr /v "WindowsApps"') do (
    "%%i" --version 2>nul | findstr /C:"3.13" >nul
    if not errorlevel 1 set "PYTHON_INSTALLED=1"
)

if "%PYTHON_INSTALLED%"=="1" (
    echo [成功] 已安装真实的 Python 3.13。
    goto SKIP_PYTHON_INSTALL
)

echo 未找到 Python 3.13。正在从镜像下载安装程序...
set "PY_EXE=python-3.13-installer.exe"
if exist "%PY_EXE%" del "%PY_EXE%"

REM 使用华为云镜像加速下载
curl -k -L --retry 3 -o "%PY_EXE%" "https://mirrors.huaweicloud.com/python/3.13.1/python-3.13.1-amd64.exe"
if errorlevel 1 (
    echo [错误] 下载 Python 安装程序失败。
    pause
    exit /b 1
)

echo.
echo 正在启动 Python 安装程序...
start "" "%PY_EXE%" /passive InstallAllUsers=0 PrependPath=1 Include_test=0

echo 正在后台安装 Python 3.13 [请观察弹出的进度条，请勿关闭窗口，大约5分钟]...
:WAIT_PY
timeout /t 3 /nobreak >nul
REM 检查任务管理器中是否还有这个安装进程
tasklist /FI "IMAGENAME eq %PY_EXE%" 2>nul | find /I "%PY_EXE%" >nul
if not errorlevel 1 goto WAIT_PY

REM 进程消失后，检查是否成功写入了 python.exe
if not exist "%LOCALAPPDATA%\Programs\Python\Python313\python.exe" (
    echo [错误] 未找到 python.exe，安装可能被手动取消或失败。
    pause
    exit /b 1
)

echo [成功] Python 3.13 安装完成。
if exist "%PY_EXE%" del "%PY_EXE%"

REM 强制刷新本窗口的环境变量 PATH
set "PATH=%LOCALAPPDATA%\Programs\Python\Python313\Scripts\;%LOCALAPPDATA%\Programs\Python\Python313\;%PATH%"

:SKIP_PYTHON_INSTALL
echo.


REM ------------------------------------------------------------
REM 步骤 2 & 3: 创建并激活虚拟环境
REM ------------------------------------------------------------
echo [步骤 2] 正在创建 Python 虚拟环境...
if exist "venv\Scripts\activate.bat" (
    echo [成功] 虚拟环境已存在。
) else (
    python -m venv venv
    if errorlevel 1 (
        echo [错误] 创建虚拟环境失败。
        pause
        exit /b 1
    )
    echo [成功] 虚拟环境创建完毕。
)

echo [步骤 3] 正在激活虚拟环境...
call "venv\Scripts\activate.bat"
if errorlevel 1 (
    echo [错误] 激活虚拟环境失败。
    pause
    exit /b 1
)
echo [成功] 虚拟环境已激活。
echo.


REM ------------------------------------------------------------
REM 步骤 4: 安装所需的 Python 包
REM ------------------------------------------------------------
echo [步骤 4] 正在安装 requirements.txt 中的依赖包 (使用清华源加速)...
python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple >nul 2>&1
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
if errorlevel 1 (
    echo [错误] 依赖包安装失败。
    pause
    exit /b 1
)
echo [成功] 依赖包安装完成。
echo.


REM ------------------------------------------------------------
REM 步骤 5: 安装 Playwright Chromium
REM ------------------------------------------------------------
echo [步骤 5] 正在安装 Playwright Chromium 浏览器...
set PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright
python -m playwright install chromium
if errorlevel 1 (
    echo [错误] Playwright Chromium 安装失败。
    pause
    exit /b 1
)
echo [成功] Playwright Chromium 安装完成。
echo.


REM ------------------------------------------------------------
REM 步骤 6: 下载并安装 VS Code
REM ------------------------------------------------------------
echo [步骤 6] 正在检查 VS Code...
where code >nul 2>&1
if not errorlevel 1 (
    echo [成功] VS Code 已安装。
    goto SKIP_VSCODE_INSTALL
)

echo 未找到 VS Code。正在下载安装程序 (大约9分钟)...
set "VS_EXE=vscode-installer.exe"
if exist "%VS_EXE%" del "%VS_EXE%"

REM 直接使用官方链接，利用 -L 参数自动重定向到国内 Azure CDN
curl -k -L --retry 3 -o "%VS_EXE%" "https://code.visualstudio.com/sha/download?build=stable&os=win32-x64-user"
if errorlevel 1 (
    echo [错误] 下载 VS Code 失败。请检查网络。
    pause
    exit /b 1
)

echo.
echo 正在启动 VS Code 安装程序...
start "" "%VS_EXE%" /SILENT /NORESTART /MERGETASKS=!runcode,addcontextmenufiles,addcontextmenufolders,associatewithfiles,addtopath

echo 正在后台安装 VS Code [请观察弹出的进度条]...
:WAIT_VS
timeout /t 3 /nobreak >nul
tasklist /FI "IMAGENAME eq %VS_EXE%" 2>nul | find /I "%VS_EXE%" >nul
if not errorlevel 1 goto WAIT_VS

echo [成功] VS Code 安装完成。
if exist "%VS_EXE%" del "%VS_EXE%"
set "PATH=%PATH%;%LOCALAPPDATA%\Programs\Microsoft VS Code\bin"

:SKIP_VSCODE_INSTALL
echo.


REM ------------------------------------------------------------
REM 步骤 7: 安装 VS Code 插件
REM ------------------------------------------------------------
echo [步骤 7] 正在安装 VS Code 插件...
set EXTENSIONS=ms-python.python ms-python.vscode-pylance ms-toolsai.jupyter formulahendry.code-runner ms-toolsai.data-wrangler yzhang.markdown-all-in-one goessner.mdmath DavidAnson.vscode-markdownlint pdconsec.vscode-print vscode-icons-team.vscode-icons tomoki1207.pdf streetsidesoftware.code-spell-checker

for %%e in (%EXTENSIONS%) do (
    echo   正在安装 %%e ...
    call code --install-extension %%e --force >nul 2>&1
    if errorlevel 1 (
        echo   [警告] 无法安装 %%e，可能需要手动安装。
    ) else (
        echo   [成功] %%e 已安装。
    )
)
echo.

REM ------------------------------------------------------------
REM 完成
REM ------------------------------------------------------------
echo ============================================================
echo   环境配置全部完成！
echo ============================================================
echo.
echo 下一步操作：
echo   1. 打开VS Code, 打开文件夹DATA-MODELING-COURSE-STUDENT(文件夹下应该
echo      有 requirements.txt 和 venv 文件夹等文件)
echo   2. 打开实验.ipynb文件，选择右上角的select kernel ->
echo      Python Environment... -> venv
echo   3. 点击最上面的按钮Run All，到这里就可以开始实验了。
echo.
pause