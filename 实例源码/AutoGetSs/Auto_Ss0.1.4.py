#!python2
# -*- coding: utf-8 -*-
# @Author: koosuf
# @Date:   2017-02-06 02:21:38
# @Last Modified by:   KOOSUF\koosuf
# @Last Modified time: 2017-03-20 14:28:35

import re
import os
import sys
import time
import json
import base64
import chardet
import requests
import grequests
from lxml import etree
from concurrent.futures import ThreadPoolExecutor

configs = []
# d代理处理
proxies = {
    "http": "http://127.0.0.1:1080",
    "http":  "http://106.46.136.125:808",
}


def decode_qr(qr_img_url):
    # 二维码解码
    url = 'http://cli.im/Api/Browser/deqr'
    Headres = {
        "Accept": "*/*",
        "Referer": "http://cli.im/deqr",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36",
        "Host": "cli.im",
        "Origin": "http://cli.im"
    }
    Params = {
        'data': qr_img_url
    }
    try:
        req = requests.post(url, params=Params)
        str_qr = req.json()
        qr = str_qr['data']['RawData'].encode('utf-8')
        data_qr = base64.b64decode(qr[5:])
    except Exception as e:
        req = requests.post(url, params=Params)
        str_qr = req.json()
        qr = str_qr['data']['RawData'].encode('utf-8')
        data_qr = base64.b64decode(qr[5:])
    return data_qr


def encode_deal(src_html):
    # 编码处理
    cat_encode = chardet.detect(src_html)
    enc = cat_encode['encoding']     # enc = req.encoding 不是很准

    if enc == None:
        html = None
    elif enc == 'utf-8' or enc == 'UTF-8':
        html = src_html
    else:
        html = src_html.decode(enc, 'ignore').encode('utf-8')
    return html.decode('utf-8')


def load_Sslist(Ss_user, Ss_passwd, Ss_port, Ss_Enc=['aes-256-cfb']):
    num = min(len(Ss_user), len(Ss_passwd), len(Ss_port))
    for i in range(num):
        config = {}
        if "del" in str(Ss_user[i]):
            continue
        if Ss_user[i] is None:
            continue
        try:
            config['remarks'] = u"updata_" + \
                time.strftime("%Y.%m.%d %H:%M:%S", time.localtime())
            config['server'] = Ss_user[i]
            config['server_port'] = int(Ss_port[i])
            config['password'] = Ss_passwd[i]
            config['method'] = Ss_Enc[i]
            config['auth'] = False
            config['timeout'] = 5
            print('{:<20} {:<12}   {:<20} {}'.format(Ss_user[i],
                                                     int(Ss_port[i]), Ss_passwd[i], Ss_Enc[i]))
            configs.append(config)
        except ValueError:
            continue
    return 0


def load_config(filename="gui-config.json"):
    Ssconfig = {}
    try:
        with open(filename, 'r') as fp:
            Ssconfig = json.load(fp)
    except IOError:
        msg = u"文件 " + filename + u" 并不存在，请确认程序运行在ShadowsocksR目录中！"
        print(msg)
    return Ssconfig


def save_config(filename, data):
    try:
        with open(filename, 'w') as fp:
            fp.write(json.dumps(data, indent=4))
    except IOError:
        msg = u"文件 " + filename + u" 并不存在，请确认程序运行在ShadowsocksR目录中！"
        print(msg)
    return 0


def get_ss_ishadow(r):
    html_doc = encode_deal(r.content)

    Ss_users = re.findall('服务器地址:(.*?)</h4>', html_doc, re.S)
    Ss_passwds = re.findall('密码:(.*?)</h4>', html_doc, re.S)
    # 端口
    Ss_ports = re.findall('<h4>端口:(.*?)</h4>', html_doc, re.S)
    # 加密方式
    Ss_Encs = re.findall('<h4>加密方式:(.*?)</h4>', html_doc, re.S)

    load_Sslist(Ss_users, Ss_passwds, Ss_ports, Ss_Encs)


def get_ss_vbox(r):
    html_doc = encode_deal(r.content)
    Ss_users = re.findall(
        '服务器地址：<span class="pull-right">(.*?)</span></li>', html_doc, re.S)
    # 端口
    Ss_ports = re.findall(
        '端口：<span class="pull-right">(.*?)</span></li>', html_doc, re.S)
    # 密码
    Ss_passwds = re.findall(
        '密码：<span class="pull-right">(.*?)</span></li>', html_doc, re.S)
    # 加密方式
    Ss_Encs = re.findall(
        '加密：<span class="pull-right">(.*?)</span></li>', html_doc, re.S)

    load_Sslist(Ss_users, Ss_passwds, Ss_ports, Ss_Encs)


def get_ss_vpsml(r):
    html_doc = encode_deal(r.content)
    # 服务器地址
    Ss_users = re.findall(
        '<h4>服务器:(.*?)</h4>', html_doc, re.S)
    # 端口
    Ss_ports = re.findall(
        '<h4>端口:(.*?)</h4>', html_doc, re.S)
    # 密码
    Ss_passwds = re.findall(
        '<h4>密码:(.*?)</h4>', html_doc, re.S)
    # 加密方式
    Ss_Encs = re.findall(
        '<h4>加密:(.*?)</h4>', html_doc, re.S)

    load_Sslist(Ss_users, Ss_passwds, Ss_ports, Ss_Encs)


def get_ss_frss(r):
    Ss_users = []
    Ss_passwds = []
    Ss_ports = []
    Ss_Encs = []
    html_doc = encode_deal(r.content)
    Ss_r = html_doc.split('alert')
    for uu in Ss_r[1:]:
        uu = uu.replace('IP', '').replace('：', '').replace(
            r'\n', '').replace('，', '')
        uu = uu.decode('utf-8')
        Ss_ = re.findall(
            u'"(.*?)端口(.*?)密码(.*?)method(.*?)不定期改密码请先加入收藏夹"', uu, re.S)
        Ss_users.append(Ss_[0][0])
        Ss_passwds.append(Ss_[0][2])
        Ss_ports.append(Ss_[0][1])
        Ss_Encs.append(Ss_[0][3])
    load_Sslist(Ss_users, Ss_passwds, Ss_ports, Ss_Encs)


def get_ss_doubi(r):
    Ss_users = []
    Ss_passwds = []
    Ss_ports = []
    Ss_Encs = []
    html_doc = encode_deal(r.content)
    doubi_string = re.findall(
        "<tbody[^>]*>[\s\S]*?<\/tbody>", html_doc)[0]
    page = etree.HTML(doubi_string)

    tr_list = page.xpath('//tr')
    for tr in tr_list[1:]:
        Ss_users.append(tr[1].text)
        Ss_passwds.append(tr[3].text)
        Ss_ports.append(tr[2].text)
        Ss_Encs.append(tr[4].text)

    load_Sslist(Ss_users, Ss_passwds, Ss_ports, Ss_Encs)


def get_ss_yhyhd(r):
    # https://xsjs.yhyhd.org/free-ss
    Ss_users = []
    Ss_passwds = []
    Ss_ports = []
    Ss_Encs = []
    html_doc = encode_deal(r.content)
    Ss_br = re.findall(
        "<strong>(.*?)</strong>", html_doc, re.S)
    for Ss_i in range(int(len(Ss_br) / 4)):
        Ss_users.append(Ss_br[0 + Ss_i * 4])
        Ss_passwds.append(Ss_br[3 + Ss_i * 4])
        Ss_ports.append(Ss_br[1 + Ss_i * 4])
        Ss_Encs.append(Ss_br[2 + Ss_i * 4])
    load_Sslist(Ss_users, Ss_passwds, Ss_ports, Ss_Encs)


def get_ss_sspw(r):
    # http://www.shadowsocks.asia/mianfei/10.html
    Ss_users = []
    Ss_passwds = []
    Ss_ports = []
    Ss_Encs = []
    html_doc = encode_deal(r.content)
    p = re.compile('\s+')
    html_doc = re.sub(p, '', html_doc)
    # 服务器地址
    re_str = re.findall(
        '">服务器(.*?)服务器端口(\d+)密码(.*?)代理端口(\d+)加密方式(.*?)临时账号', html_doc, re.S)
    for r in re_str:
        Ss_users.append(r[0][-12:])
        # # 端口
        Ss_ports.append(r[1])
        # # 密码
        Ss_passwds.append(r[2])
        # # 加密方式
        Ss_Encs.append(r[4])

    load_Sslist(Ss_users, Ss_passwds, Ss_ports, Ss_Encs)


def get_ss_shadowsocks8(r):
    shadowsocks8_list = [
        'http://free.shadowsocks8.cc/images/server01.png',
        'http://free.shadowsocks8.cc/images/server02.png',
        'http://free.shadowsocks8.cc/images/server03.png'
    ]
    Ss_users = []
    Ss_passwds = []
    Ss_ports = []
    Ss_Encs = []
    for x in shadowsocks8_list:
        try:
            qrstr = decode_qr(x)
            arr = qrstr.split(':')
            Ss_Encs.append(arr[0])
            Ss_passwds.append(arr[1].split('@')[0])
            Ss_users.append(arr[1].split('@')[1])
            Ss_ports.append(arr[2])
        except Exception as e:
            continue
    load_Sslist(Ss_users, Ss_passwds, Ss_ports, Ss_Encs)


def get_ss_sishadow(r):
    # https://ishadow.info/
    Ss_users = []
    Ss_passwds = []
    Ss_ports = []
    Ss_Encs = []
    html_doc = encode_deal(r.content)
    all_ = re.findall(
        '<div class="hover-text">(.*?)<h4><a href', html_doc, re.S)
    for div in all_:
        # 服务器地址
        Ss_up = re.findall(
            '">(.*?)</span>', div, re.S)
        # # 端口
        Ss_port = re.findall(
            '<h4>Port：(.*?)</h4>', div, re.S)
        # 加密方式
        Ss_Enc = re.findall(
            '<h4>Method:(.*?)</h4>', div, re.S)
        Ss_users.append(Ss_up[0])
        Ss_passwds.append(Ss_up[2])
        Ss_ports.append(Ss_port[0])
        Ss_Encs.append(Ss_Enc[0])
    load_Sslist(Ss_users, Ss_passwds, Ss_ports, Ss_Encs)


def get_ss_Alvin9999(r):
    # "https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7"
    Ss_users = []
    Ss_passwds = []
    Ss_ports = []
    Ss_Encs = []
    comp = re.compile(
        "<p>服务器\d*.*?([\w\.]+)\s*端口.*?(\d*)\s*密码.*?([\w\.-]*)\s*加密方式.*?([\w-]*)</p>")  #
    comp_encs = re.compile("加密方式：([\w-]*)\s*")

    html_doc = encode_deal(r.content)
    html_doc = re.findall("<p>服务器.*</p>", html_doc)
    for i in html_doc:
        res = re.match(comp, i)
        if res.group(4) == '':
            ree = re.findall(comp_encs, i)
            if len(ree) != 0:
                Ss_Encs.append(ree[0])
                Ss_users.append(res.group(1))
                Ss_passwds.append(res.group(3))
                Ss_ports.append(res.group(2))
        else:
            Ss_Encs.append(res.group(4))
            Ss_users.append(res.group(1))
            Ss_passwds.append(res.group(3))
            Ss_ports.append(res.group(2))

    load_Sslist(Ss_users, Ss_passwds, Ss_ports, Ss_Encs)


def start_get_ss():
    urls_dict = {
        'https://xsjs.yhyhd.org/free-ss/': get_ss_yhyhd,
        'https://doub.io/sszhfx/':  get_ss_doubi,
        'http://frss.ml/': get_ss_frss,
        'https://www.vbox.co/': get_ss_vbox,
        'http://ishadow.info/': get_ss_ishadow,
        'http://ss.vpsml.site/': get_ss_vpsml,
        'http://free.shadowsocks8.cc/': get_ss_shadowsocks8,
        'http://www.shadowsocks.asia/mianfei/10.html': get_ss_sspw,
        'https://ishadow.info/': get_ss_sishadow,
        r'https://github.com/Alvin9999/new-pac/wiki/ss%E5%85%8D%E8%B4%B9%E8%B4%A6%E5%8F%B7': get_ss_Alvin9999
    }
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
    pool = ThreadPoolExecutor(len(urls_dict.keys()) + 1)
    rs = (grequests.get(u, timeout=10, proxies=proxies, headers=headers)
          for u in urls_dict.keys())
    for r in grequests.imap(rs, size=3):
        try:
            print("{:-^72}".format(r.url))
            func = urls_dict.get(r.url, u"没有匹配项！！！")
            pool.submit(func(r))

        except Exception as e:
            print(u"错误提示:" + str(e))
            continue


def main():
    Tstart = time.time()
    print("{:#^72}".format(
        ' {} Shadowsocks Update '.format(time.strftime('%Y-%m-%d %H:%M:%S'))
    ))
    start_get_ss()
    filename = 'gui-config.json'
    Ssconfig = load_config(filename)
    Ssconfig['configs'] = configs
    save_config(filename, Ssconfig)
    print(u'此次更新了------------' + str(len(configs)) +
          u'-------------条数据,时间%f' % (time.time() - Tstart))
    os.system('pause')


def restart_program():
    # 程序重启
    python = sys.executable
    os.execl(python, python, * sys.argv)

if __name__ == '__main__':
    main()
