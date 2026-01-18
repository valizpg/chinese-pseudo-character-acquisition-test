[ 1. 先决条件 ]
在运行本实验前，请确保您的电脑已经安装了 Python 3。


[ 2. 安装步骤 ]

1. 下载项目
   将本项目所有文件下载或克隆（Clone）到您的本地文件夹中。

2. 安装依赖库
   本项目需要 Flask, pandas, 和 openpyxl 三个 Python 库。
   请打开终端或命令提示符（Terminal/CMD），运行以下命令：

   pip install flask pandas openpyxl


[ 3. 运行实验 ]

1. 启动服务器
   在终端中，进入项目所在的根目录，运行以下命令：

   python web_runner.py

2. 开始实验
   运行命令后，程序通常会默认打开浏览器。
   如果未自动打开，请手动将此网址复制到浏览器中访问：

   http://127.0.0.1:5000/


[ 4. 主要文件与文件夹说明 ]

* web_runner.py
  └── 实验的主程序，负责启动 web 服务和处理数据。

* web_experiment.html
  └── 实验的网页前端界面。

* file_checker.py
  └── 用于检查所有实验所需文件是否齐全的脚本。

* definitions.xlsx
  └── 存放“伪汉字”的定义的 Excel 文件。

* stimuli/
  └── [文件夹] 存放所有实验材料。

* images/
  └── [文件夹] 存放“伪汉字”的图片。

* meanings/
  └── [文件夹] 存放“伪汉字”的含义图片。

* pronunciations/
  └── [文件夹] 存放“伪汉字”的发音。

* radical_awareness/
  └── [文件夹] 存放部首测试相关的图片。

* data/
  └── [文件夹] 存放实验结果数据。

* trials/
  └── [文件夹] 存放预设的试次信息。