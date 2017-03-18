#!python2
# -*- coding: utf-8 -*-
# @Author: koosuf
# @Date:   2017-02-06 02:21:38
# @Last Modified by:   KOOSUF\koosuf
# @Last Modified time: 2017-03-19 03:19:55

import re
import os
import sys
import time
import json
import base64
import chardet
import requests
from lxml import etree

configs = []
proxies = {
    "http": "http://127.0.0.1:1080",
}


def decode_qr(qr_img_url):
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
    return html


def requests_htmls(Src_allurl):
    src_html = ''
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'}
    # 异常处理
    try:
        req = requests.get(Src_allurl, proxies=proxies,
                           headers=headers, timeout=80)
        src_html = str(req.content)
        if req.status_code == requests.codes.ok or len(src_html):
            print("{:-^72}".format(Src_allurl))
        else:
            print(u"获取：" + Src_allurl + u" 页面错误!")
            req.raise_for_status()
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as er:
        print(u"异常类型：" + str(er))
    except requests.HTTPError as f:
        print(u'服务器无法满足请求.')

    return encode_deal(src_html)


def load_Sslist(Ss_user, Ss_passwd, Ss_port, Ss_Enc=['aes-256-cfb']):
    num = min(len(Ss_user), len(Ss_passwd), len(Ss_port))
    for i in range(num):
        config = {}
        if "del" in str(Ss_user[i]):
            continue
        if Ss_user[i] is None:
            continue
        try:
            config['remarks'] = u"无视版权_".encode(
                'utf-8') + str(len(configs) + 1)
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


def get_ss_ishadow(Src_url_ishadow):
    html_doc = requests_htmls(Src_url_ishadow)
    if html_doc is None:
        print(u'解析失败:' + Src_url_ishadow)
        return -1
    Ss_users = re.findall('服务器地址:(.*?)</h4>', html_doc, re.S)
    Ss_passwds = re.findall('密码:(.*?)</h4>', html_doc, re.S)
    # 端口
    Ss_ports = re.findall('<h4>端口:(.*?)</h4>', html_doc, re.S)
    # 加密方式
    Ss_Encs = re.findall('<h4>加密方式:(.*?)</h4>', html_doc, re.S)

    load_Sslist(Ss_users, Ss_passwds, Ss_ports, Ss_Encs)


def get_ss_vbox(Src_url_vbox):
    html_doc = requests_htmls(Src_url_vbox)
    if html_doc is None:
        print(u'解析失败:' + Src_url_vbox)
        return -1
    # 服务器地址
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


def get_ss_vpsml(Src_url_vpsml):
    html_doc = requests_htmls(Src_url_vpsml)
    if html_doc is None:
        print(u'解析失败:' + Src_url_vpsml)
        return -1

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


def get_ss_frss(Src_url_frss):
    Ss_users = []
    Ss_passwds = []
    Ss_ports = []
    Ss_Encs = []
    html_doc = requests_htmls(Src_url_frss)
    if html_doc is None:
        print(u'解析失败:' + Src_url_frss)
        return -1
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


def get_ss_doubi(Src_url_doubi):
    Ss_users = []
    Ss_passwds = []
    Ss_ports = []
    Ss_Encs = []
    html_doc = requests_htmls(Src_url_doubi)
    if html_doc is None:
        print(u'解析失败:' + Src_url_doubi)
        return -1
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


def get_ss_yhyhd(Src_url_yhyhd):
    # https://xsjs.yhyhd.org/free-ss
    Ss_users = []
    Ss_passwds = []
    Ss_ports = []
    Ss_Encs = []
    html_doc = requests_htmls(Src_url_yhyhd)
    if html_doc is None:
        print(u'解析失败:' + Src_url_yhyhd)
        return -1
    Ss_br = re.findall(
        "<strong>(.*?)</strong>", html_doc, re.S)
    for Ss_i in range(len(Ss_br) / 4):
        Ss_users.append(Ss_br[0 + Ss_i * 4])
        Ss_passwds.append(Ss_br[3 + Ss_i * 4])
        Ss_ports.append(Ss_br[1 + Ss_i * 4])
        Ss_Encs.append(Ss_br[2 + Ss_i * 4])
    load_Sslist(Ss_users, Ss_passwds, Ss_ports, Ss_Encs)


def get_ss_shadowsocks8(Src_url_ss8):
    shadowsocks8_list = [
        Src_url_ss8 + 'images/server01.png',
        Src_url_ss8 + 'images/server02.png',
        Src_url_ss8 + 'images/server03.png'
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


def get_ss_sspw(Src_url_sspw):
    # http://www.shadowsocks.asia/mianfei/10.html
    Ss_users = []
    Ss_passwds = []
    Ss_ports = []
    Ss_Encs = []
    html_doc = requests_htmls(Src_url_sspw)
    if html_doc is None:
        print(u'解析失败:' + Src_url_sspw)
        return -1
    p = re.compile('\s+')
    html_doc = re.sub(p, '', html_doc)
    # print(html_doc)
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


def get_ss_sishadow(Src_url_sishadow):
    # https://ishadow.info/
    Ss_users = []
    Ss_passwds = []
    Ss_ports = []
    Ss_Encs = []
    html_doc = requests_htmls(Src_url_sishadow)
    if html_doc is None:
        print(u'解析失败:' + Src_url_sishadow)
        return -1
    # print(html_doc)

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


def start_get_ss():
    Tstart = time.time()
    get_ss_yhyhd(Src_url_yhyhd='https://xsjs.yhyhd.org/free-ss/')
    get_ss_doubi(Src_url_doubi='https://doub.io/sszhfx/')
    get_ss_vpsml(Src_url_vpsml='http://ss.vpsml.site/')
    get_ss_ishadow(Src_url_ishadow='http://isx.yt/')
    get_ss_vbox(Src_url_vbox='https://www.vbox.co/')
    get_ss_frss(Src_url_frss='http://frss.ml/')
    get_ss_shadowsocks8(Src_url_ss8='http://free.shadowsocks8.cc/')
    get_ss_sspw(Src_url_sspw='http://www.shadowsocks.asia/mianfei/10.html')
    get_ss_sishadow(Src_url_sishadow='https://ishadow.info/')
    print(time.time() - Tstart)


def main():
    print("{:#^72}".format(
        ' {} Shadowsocks Update '.format(time.strftime('%Y-%m-%d %H:%M:%S'))
    ))
    start_get_ss()
    filename = 'gui-config.json'
    Ssconfig = load_config(filename)
    Ssconfig['configs'] = configs
    save_config(filename, Ssconfig)

    print(u'此次更新了------------' + str(len(configs)) + u'-------------条数据')
    os.system('pause')

if __name__ == '__main__':
    main()
