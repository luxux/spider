# -*- coding: utf-8 -*-
# @Author: koosuf
# @Date:   2017-02-25 16:49:49
# @Last Modified by:   koosuf
# @Last Modified time: 2017-02-25 21:21:45

import re
import copy
import requests
import datetime
from lxml import etree, html


class Postdata(object):
    Urlold = "http://xxfb.hydroinfo.gov.cn/svg/svgwait.jsp"
    Urlnew = "http://xxfb.hydroinfo.gov.cn/dwr/call/plaincall/IndexDwr.getSreachData.dwr"
    Headres = {
        "Accept": "*/*",
        "REFERER": "http://xxfb.hydroinfo.gov.cn/svg/svghtml.html",
        "Accept-Encoding": "gzip, deflate",
        "User-Agent": "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E)",
        "Host": "xxfb.hydroinfo.gov.cn",
    }
    Params = {
        "gcxClass": "1",
        "gcxKind": "2",
        "DateL": "",
        "DateM": "",
        "gcxData": "7",
        "site": "",
    }
    Data_sk = {
        'callCount': 1,
        'page': '/ssIndex.html',
        'httpSessionId': 'AD86D68AC7071780898FE6C20A690666.tomcat1',
        'scriptSessionId': 'EFD5366A67FBD70A9F1C9AF0410971B4471',
        'c0-scriptName': 'IndexDwr',
        'c0-methodName': 'getSreachData',
        'c0-id': 0,
        'c0-param0': 'string:sk',
        'c0-param1': 'string:',
        'c0-param2': 'string:',
        'batchId': 1
    }
    Data_hd = {
        'callCount': 1,
        'page': '/ssIndex.html',
        'httpSessionId': '1B9DA8BF1A88F8A39E36D4561EB23803.tomcat1',
        'scriptSessionId': 'C537A5E7EA9798EDE9190BC0BC01670F100',
        'c0-scriptName': 'IndexDwr',
        'c0-methodName': 'getSreachData',
        'c0-id': 0,
        'c0-param0': 'string:hd',
        'c0-param1': 'string:',
        'c0-param2': 'string:',
        'batchId': 0
    }
    Cookies = dict(
        zhuzhan='57527109',
        wdcid='7089a8c7d50714ff',
        JSESSIONID='AD86D68AC7071780898FE6C20A690666.tomcat1',
        wdlast='1487431437'
    )

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(self.Headres)

    def build_params(self, site_id, start_time):
        params = copy.deepcopy(self.Params)
        params["DateL"] = str(start_time)
        params["DateM"] = datetime.date.today()
        params["site"] = str(site_id)
        return params

    def fetch_history_data(self, site_id, start_time):
        params = self.build_params(site_id, start_time)
        rep = self.session.get(self.Urlold, params=params)

        if rep.status_code != 200:
            print("request_error status=%s" % rep.status_code)
        return rep.text

    def fetch_html_data(self, cls):
        if cls == "hd":
            rep = self.session.post(
                self.Urlnew, data=self.Data_hd, cookies=self.Cookies)
            tree = html.fromstring(rep.content)

        elif cls == "sk":
            rep = self.session.post(
                self.Urlnew, data=self.Data_sk, cookies=self.Cookies)
            tree = html.fromstring(rep.content)
        return tree, cls
if __name__ == '__main__':
    get_data = Postdata()
    text2 = get_data.fetch_html_data("hd")
    print(text2)
