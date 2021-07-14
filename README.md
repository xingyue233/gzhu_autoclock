# 写在前面

![https://img.shields.io/badge/flask-v1.1.1-blue](https://img.shields.io/badge/flask-v1.1.1-blue)![](https://img.shields.io/badge/bootstrap-v3-blue)![](https://img.shields.io/badge/requests-2.25.1-green)![](https://img.shields.io/badge/urllib3-1.26.2-green)![](https://img.shields.io/badge/pytesseract-0.3.7-green)![](https://img.shields.io/badge/platform-Windows%7CMac%20ox%7CUbuntu%7CCentos-lightgrey)

本仓库是在 [gzhu_no_clock_in](https://github.com/situ2001/gzhu_no_clock_in) 下进行代码封装，添加了`webserver`并提供用户操作界面。

本打卡辅助程序仅供学习交流使用，请勿过分依赖。开发者对使用或不使用本脚本造成的问题不负任何责任，不对脚本执行效果做出任何担保，原则上不提供任何形式的技术支持。



# 目录说明

├── aurun.sh  // Linux部署进程守护

├── clocktime.txt //打卡时间文件

├── cookies  //cookies储存

├── load_from_cookies.py

├── log.txt //日志

├── login.py  //登录文件

├── main.py //打卡运行入口

├── msession.py 

├── ocr.py //OCR验证码识别

├── static //Flask静态文件储存

│  ├── .DS_Store

│  └── favicon.ico

├── templates //Flask模版文件储存

│  └── index.html

├── users.txt //用户名密码数据

└── webserver.py //Flask服务器



# 如何使用

## python环境激活

推荐使用Anaconda等工具搭建python环境

```bash
// conda activate envsname
```

此步骤可跳过



## 依赖库安装

```bash
pip install flask requests
```



## 部署

文件分两部分部署，`webserver.py`和`main.py`

### Windows

- python 安装 tesseract

```
pip install pytesseract
```

- Windows tesseract install

从 [tesseract](https://digi.bib.uni-mannheim.de/tesseract/)安装 `tesseract` ，并且将相应安装目录添加进环境变量

- 运行

```bash
python webserver.py
python main.py
```



### Ubuntu/Macos

- 安装tesseract

```bash
sudo apt-get install tesseract-ocr //Ubuntu
brew install tesseract //Macos
```



- python 安装 tesseract

```
pip install pytesseract
```



- 运行

  - 普通方式运行（若用ssh链接因Linux系统进程调度进程会终止）

  ```
  python webserver.py
  python main.py
  ```

  - 以`nohup`进程守护运行

  ```bash
  sh autorun.sh
  
  // autorun.sh
  // nohup python3 main.py >> main.log 2>&1 &
  // nohup python3 webserver.py >> webserver.log 2>&1 &
  ```



# 输出日志

`main.py`日志储存于`main.log`文件

`webserver.log`日志储存于`webserver.log`文件



# 访问用户网页

```
http://localhost/ //80端口内网访问
```

同时也可以进行外网访问



# 端口映射

若主机没有公网IP，可以采用[花生壳内网穿透](https://hsk.oray.com)进行外网访问



# 运行截图

## PC

[![WeW2Gj.png](https://z3.ax1x.com/2021/07/15/WeW2Gj.png)](https://imgtu.com/i/WeW2Gj)

## iPhone

[![WeWhMq.png](https://z3.ax1x.com/2021/07/15/WeWhMq.png)](https://imgtu.com/i/WeWhMq)