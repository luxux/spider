#!python2
# -*- coding: utf-8 -*-
# @Author: koosuf
# @Date:   2017-02-06 02:21:38
# @Last Modified by:   koosuf
# @Last Modified time: 2017-03-14 00:24:44

import re
import os
import sys
import time
import json
import chardet
import requests
import subprocess
from lxml import etree

configs = []


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
        req = requests.get(Src_allurl, headers=headers, timeout=80)
        src_html = str(req.content)
        if req.status_code == requests.codes.ok or len(src_html):
            print(u"获取：" + Src_allurl + u" 页面正确!")
        else:
            print(u"获取：" + Src_allurl + u" 页面错误!")
            req.raise_for_status()
    except (requests.exceptions.ConnectionError, requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as er:
        print(u"异常类型：" + str(er))
    except requests.HTTPError as f:
        print(u'服务器无法满足请求.')

    return encode_deal(src_html)


def load_Sslist(Ss_user, Ss_passwd, Ss_port, Ss_Enc=['aes-256-cfb']):
    '''
    "configs" : [{
      "server": "86.107.110.163",
      "server_port": 10093,
      "password": "forfree",
      "method": "aes-256-cfb",
      "remarks": "罗马尼亚无视版权",
      "auth": false,
      "timeout": 5
    }
    '''
    num = min(len(Ss_user), len(Ss_passwd), len(Ss_port))
    for i in range(num):
        config = {}
        if "del" in str(Ss_user[i]):
            continue
        if Ss_user[i] is None:
            continue
        try:
            config['remarks'] = u"无视版权_".encode('utf-8') + str(i)
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
    print(u'此次更新了' + str(len(configs)) + u'条数据')
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
    print(u'正在写入文件……')
    try:
        with open(filename, 'w') as fp:
            fp.write(json.dumps(data, indent=4))
    except IOError:
        msg = u"文件 " + filename + u" 并不存在，请确认程序运行在ShadowsocksR目录中！"
        print(msg)
    print(u'写入文件完成！')
    return 0


def get_ss_ishadow(Src_url_ishadow):
    html_doc = requests_htmls(Src_url_ishadow)
    if html_doc is None:
        print(u'解析失败:' + Src_url_ishadow)
        return -1
    # Ａ
    Ss_users_A = re.findall('<h4>A服务器地址:(.*?)</h4>', html_doc, re.S)
    Ss_passwd_A = re.findall('<h4>A密码:(.*?)</h4>', html_doc, re.S)
    # B
    Ss_users_B = re.findall('<h4>B服务器地址:(.*?)</h4>', html_doc, re.S)
    Ss_passwd_B = re.findall('<h4>B密码:(.*?)</h4>', html_doc, re.S)
    # C
    Ss_users_C = re.findall('<h4>C服务器地址:(.*?)</h4>', html_doc, re.S)
    Ss_passwd_C = re.findall('<h4>C密码:(.*?)</h4>', html_doc, re.S)
    # 端口
    Ss_ports = re.findall('<h4>端口:(.*?)</h4>', html_doc, re.S)
    # 加密方式
    Ss_enc = re.findall('<h4>加密方式:(.*?)</h4>', html_doc, re.S)

    load_Sslist(Ss_users_A, Ss_passwd_A, [Ss_ports[0]], Ss_enc)
    load_Sslist(Ss_users_B, Ss_passwd_B, [Ss_ports[1]], Ss_enc)
    load_Sslist(Ss_users_C, Ss_passwd_C, [Ss_ports[2]], Ss_enc)


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


def main():
    print("{:#^72}".format(
        ' {} Shadowsocks Update '.format(time.strftime('%Y-%m-%d %H:%M:%S'))
    ))
    get_ss_frss(Src_url_frss='http://frss.ml/')
    get_ss_doubi(Src_url_doubi='https://doub.io/sszhfx/')
    get_ss_vpsml(Src_url_vpsml='http://ss.vpsml.site/')
    get_ss_ishadow(Src_url_ishadow='http://isx.yt/')  # 备用网址 isx.yt
    get_ss_vbox(Src_url_vbox='https://www.vbox.co/')
    filename = 'gui-config.json'
    Ssconfig = load_config(filename)
    Ssconfig['configs'] = configs
    save_config(filename, Ssconfig)

    os.system('pause')

if __name__ == '__main__':
    main()
