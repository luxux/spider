# AutoGetSs
### 介绍 Introduction

免费的ss分享站在频繁的更换。~~根本原因是没钱~~。

### 需求 TODO

- [x] 支持[doub.io](https://doub.io/sszhfx/),[frss.ml](http://frss.ml/),[vpsml](http://ss.vpsml.site/),[isx](http://isx.yt/)
- [x] 调试日志
- [x] 不和原有配置发生冲突
- [ ] 多系统支持
      - [ ] Linux
      - [x] windows
      - [ ] osx

### 安装 Install

#### Windows

1. 你需要安装python2.7，[下载地址](https://www.python.org/)

2. 需要安装chardet,lxml和requests模块，在管理员终端运行如下命令

   ```cmd
   py -2 -m pip install requests
   py -2 -m pip install beautifulsoup4
   ```

3. 将autogetss.py放在ShadowsocksR文件夹内
