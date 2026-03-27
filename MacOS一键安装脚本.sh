#!/usr/bin/env bash

# ============================================================
# 数据建模课程 - macOS 环境配置脚本
# ============================================================

# 设置颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}  数据建模课程 - macOS 环境配置${NC}"
echo -e "${GREEN}============================================================${NC}\n"

# 切换到脚本所在目录（确保路径正确）
cd "$(dirname "$0")" || exit

# ------------------------------------------------------------
# 步骤 0: 验证当前目录
# ------------------------------------------------------------
if [ ! -f "requirements.txt" ]; then
    echo -e "${RED}[错误] 未找到 requirements.txt。${NC}"
    echo "请在 DATA-MODELING-COURSE-STUDENT 目录下运行此脚本。"
    exit 1
fi
echo -e "${GREEN}[成功] 已检测到课程根目录。${NC}\n"

# ------------------------------------------------------------
# 步骤 1: 检查并安装 Python 3
# ------------------------------------------------------------
echo "[步骤 1] 正在检查 Python 3..."

if command -v python3 &>/dev/null; then
    PY_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    echo -e "${GREEN}[成功] 已安装 Python $PY_VERSION。${NC}"
else
    echo -e "${YELLOW}未检测到 Python 3。正在下载官方安装包...${NC}"
    # 使用官方 macOS 安装包 (Universal 适配 Intel 和 M1/M2/M3 芯片)
    curl -L -o python-installer.pkg "https://www.python.org/ftp/python/3.12.2/python-3.12.2-macos11.pkg"

    echo "正在安装 Python (可能需要输入您的 Mac 登录密码)..."
    sudo installer -pkg python-installer.pkg -target /

    if [ $? -ne 0 ]; then
        echo -e "${RED}[错误] Python 安装失败。${NC}"
        exit 1
    fi
    echo -e "${GREEN}[成功] Python 安装完成。${NC}"
    rm python-installer.pkg
fi
echo ""

# ------------------------------------------------------------
# 步骤 2 & 3: 创建并激活虚拟环境
# ------------------------------------------------------------
echo "[步骤 2] 正在创建 Python 虚拟环境..."
if [ -f "venv/bin/activate" ]; then
    echo -e "${GREEN}[成功] 虚拟环境已存在。${NC}"
else
    python3 -m venv venv
    if [ $? -ne 0 ]; then
        echo -e "${RED}[错误] 创建虚拟环境失败。${NC}"
        exit 1
    fi
    echo -e "${GREEN}[成功] 虚拟环境创建完毕。${NC}"
fi

echo "[步骤 3] 正在激活虚拟环境..."
source venv/bin/activate
echo -e "${GREEN}[成功] 虚拟环境已激活。${NC}\n"

# ------------------------------------------------------------
# 步骤 4: 安装所需的 Python 包
# ------------------------------------------------------------
echo "[步骤 4] 正在安装 requirements.txt 中的依赖包 (使用清华源加速)..."
python3 -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple >/dev/null 2>&1
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

if [ $? -ne 0 ]; then
    echo -e "${RED}[错误] 依赖包安装失败。${NC}"
    exit 1
fi
echo -e "${GREEN}[成功] 依赖包安装完成。${NC}\n"

# ------------------------------------------------------------
# 步骤 5: 安装 Playwright Chromium
# ------------------------------------------------------------
echo "[步骤 5] 正在安装 Playwright Chromium 浏览器..."
export PLAYWRIGHT_DOWNLOAD_HOST=https://npmmirror.com/mirrors/playwright
playwright install chromium
if [ $? -ne 0 ]; then
    echo -e "${RED}[错误] Playwright Chromium 安装失败。${NC}"
    exit 1
fi
echo -e "${GREEN}[成功] Playwright Chromium 安装完成。${NC}\n"

# ------------------------------------------------------------
# 步骤 6: 下载并安装 VS Code
# ------------------------------------------------------------
echo "[步骤 6] 正在检查 VS Code..."

# 将 VS Code 路径临时加入环境变量以供检测
export PATH="$PATH:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"

if command -v code &>/dev/null || [ -d "/Applications/Visual Studio Code.app" ]; then
    echo -e "${GREEN}[成功] VS Code 已安装。${NC}"
else
    echo -e "${YELLOW}未检测到 VS Code。正在解析国内加速节点...${NC}"

    # 获取真实下载地址并替换为国内 CDN (与 Windows 逻辑相同)
    REAL_URL=$(curl -s -w "%{redirect_url}" -o /dev/null "https://code.visualstudio.com/sha/download?build=stable&os=darwin-universal")
    MIRROR_URL="${REAL_URL/az764295.vo.msecnd.net/vscode.cdn.azure.cn}"

    echo "正在从国内镜像下载 VS Code (ZIP格式)..."
    curl -L -o vscode.zip "$MIRROR_URL"

    echo "正在解压并安装到 /Applications..."
    unzip -q vscode.zip

    # 移动到应用程序文件夹，如果需要权限则使用 sudo
    if [ -w "/Applications" ]; then
        mv "Visual Studio Code.app" "/Applications/"
    else
        echo "请求权限将 VS Code 移动到 /Applications..."
        sudo mv "Visual Studio Code.app" "/Applications/"
    fi

    rm vscode.zip
    echo -e "${GREEN}[成功] VS Code 安装完成。${NC}"
fi
echo ""

# ------------------------------------------------------------
# 步骤 7: 安装 VS Code 插件
# ------------------------------------------------------------
echo "[步骤 7] 正在安装 VS Code 插件..."

EXTENSIONS=(
    "ms-python.python"
    "ms-python.vscode-pylance"
    "ms-toolsai.jupyter"
    "formulahendry.code-runner"
    "ms-toolsai.data-wrangler"
    "yzhang.markdown-all-in-one"
    "goessner.mdmath"
    "DavidAnson.vscode-markdownlint"
    "pdconsec.vscode-print"
    "vscode-icons-team.vscode-icons"
    "tomoki1207.pdf"
    "streetsidesoftware.code-spell-checker"
)

# 确保 code 命令可用
export PATH="$PATH:/Applications/Visual Studio Code.app/Contents/Resources/app/bin"

for ext in "${EXTENSIONS[@]}"; do
    echo "  正在安装 $ext ..."
    code --install-extension "$ext" --force >/dev/null 2>&1
    if [ $? -ne 0 ]; then
        echo -e "${YELLOW}  [警告] 无法安装 $ext，可能需要手动安装。${NC}"
    else
        echo -e "${GREEN}  [成功] $ext 已安装。${NC}"
    fi
done
echo ""

# ------------------------------------------------------------
# 完成
# ------------------------------------------------------------
echo -e "${GREEN}============================================================${NC}"
echo -e "${GREEN}  环境配置全部完成！${NC}"
echo -e "${GREEN}============================================================${NC}\n"
echo "下一步操作："
echo "  1. 脚本已自动为您配置好依赖，您可以直接打开 VS Code。"
echo "  2. 在终端输入: code . (即可在当前目录打开 VS Code)"
echo "  3. 在 VS Code 中打开任意 Python 或 Notebook 文件，选择右下角的 Python 解释器为 venv 即可！"
echo ""
echo "如需在新的终端窗口手动激活虚拟环境，请输入："
echo "  source venv/bin/activate"
echo ""