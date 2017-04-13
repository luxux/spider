# AutoGetSs
### 介绍

这个嘛！自然懒的原因，不想手动的粘贴复制。更重要的是~~没钱、没钱、没钱~~。:joy: :joy: :joy:

### 需求

- [x] 获取网站(~~好的网站，求推存~~)
    - [x] [doub.io](https://doub.io/sszhfx/)
    - [x] [frss.ml](http://frss.ml/)
    - [x] [vpsml](http://ss.vpsml.site/)
    - [x] [vbox](https://www.vbox.co/)
    - [x] [shadowsocks8](http://free.shadowsocks8.cc/)
    - [x] [ishadow](https://ishadow.info/)
    - [x] [mianfei](http://www.shadowsocks.asia/mianfei/10.html)
    - [x] [sishadow](http://ishadow.info/)
    - [x] [yhyhd](https://xsjs.yhyhd.org/free-ss/)
    - [x] [new-pac](https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7)
- [ ] 调试日志
- [x] 不和原有配置发生冲突
- [x] 多系统支持
- [ ] 自动运行

### 效果
![](./img/getSs_img.jpg)

![](./img/Ss_img.jpg)

### install
[ShadowsocksR使用详解](https://doub.io/ss-jc10/)

#### Windows(源码)

1. 你需要安装python2.7，[下载地址](https://www.python.org/)

2. 需要安装chardet和requests等模块，在管理员终端运行如下命令

   ```cmd
   py -2 -m pip install -r requirements.txt
   ```

3. 将Auto_Ssx.x.x.py放在ShadowsocksR文件夹内

4. 需要ShadowsocksR文件夹内有gui-config.json文件

5. 在管理员终端运行如下命令，需要打开全局代理。
    ```cmd
    py -2 Auto_Ssx.x.x.py
    ```

#### Windows(exe)

1. 下载Auto_Ss0.x.x.exe到ShadowsocksR文件夹

2. 管理员运行Auto_Ss0.x.x.exe,需要打开全局代理。

3. ShadowsocksR更新加载gui-config.json文件

4. 下载地址[Releases](https://github.com/luxux/spider/releases)

### 注意: 在加载的过程中有什么任何错误提示，都可以打开ShadowsocksR全局代理。管理员运行Auto_Ss0.x.x.exe **多次**
