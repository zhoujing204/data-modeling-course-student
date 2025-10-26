# 开发环境的安装

1. 安装Python SDK 3.12+, 下载安装地址：[www.python.org/downloads/](https://www.python.org/downloads/)
2. 打开Windows终端cmd，切换到课程的根目录`data-modeling-course-student`，在终端cmd中运行下面的命令创建并激活Python虚拟环境：

   ```bash
   python -m venv venv
   "venv/Scripts/activate"
   ```

3. 在终端中运行命令： `pip install -r requirements.txt` 来安装课程需要的Python包。
4. 使用playwright安装Chromium浏览器，运行命令： `python -m playwright install chromium`
5. 安装集成开发环境VS Code，下载安装地址：[code.visualstudio.com/download](https://code.visualstudio.com/download)
6. 在VS Code中安装课程需要的插件：

   - Python Extension Pack
   - Jupyter
   - Code Runner
   - Data Wrangler
   - Markdown All in One
   - Markdown Math
   - markdownlint
   - Print
   - vscode-icons
   - code spell checker