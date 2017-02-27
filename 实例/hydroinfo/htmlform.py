#!python2
# -*- coding: utf-8 -*-
# @Author: koosuf
# @Date:   2017-02-25 16:38:35
# @Last Modified by:   koosuf
# @Last Modified time: 2017-02-25 21:33:56

import time
from spider import Postdata

gg = Postdata()
tree = Postdata.fetch_html_data(gg, "sk")
tr_list = tree[0].xpath('//tr')

output_list = []
for i in tr_list:
    liuyu = i.xpath('.//td')[0].xpath('./text()')[0]
    xingzhengqu = i.xpath('.//td')[1].xpath('./text()')[0]
    heming = i.xpath('.//td')[2].xpath('./text()')[0]
    kuming = i.xpath('.//td')[3].xpath('./font/text()')[0]
    kushuiwei = i.xpath('.//td')[4].xpath('./font/text()')[0]
    kushuiwei_delta_flag = i.xpath('.//td')[4].xpath('./font/font/text()')[0]
    xushuiliang = i.xpath('.//td')[5].xpath('./text()')[0]
    ruku = i.xpath('.//td')[6].xpath('./text()')[0]
    didinggaocheng = i.xpath('.//td')[7].xpath('./text()')[0]
    print(liuyu.decode('unicode-escape').encode('utf-8'))
    print(didinggaocheng)
    output_list.append(
        dict(
            liuyu=liuyu.decode('unicode-escape').encode('gb2312'),
            xingzhengqu=xingzhengqu.decode('unicode-escape').encode('gb2312'),
            heming=heming.decode('unicode-escape').encode('utf-8'),
            kuming=kuming.decode('unicode-escape').encode('utf-8'),
            kushuiwei=kushuiwei.replace(u' ', ''),
            kushuiwei_delta_flag=kushuiwei_delta_flag.decode(
                'unicode-escape').encode('utf-8'),
            xushuiliang=xushuiliang.decode('unicode-escape').encode('gb2312'),
            ruku=ruku,
            didinggaocheng=didinggaocheng.replace(u' ', ''),
        )
    )
# print output_list

table_content = u''
for each in output_list:
    table_content += u'''

    <tr>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
        <td>{}</td>
    </tr>
    '''.format(unicode(each['liuyu'], 'gb2312'),
               unicode(each['xingzhengqu'], 'gb2312'),
               unicode(each['heming'], 'utf-8'),
               unicode(each['kuming'], 'utf-8'),
               unicode(each['kushuiwei']),
               unicode(each['kushuiwei_delta_flag'], 'utf-8'),
               unicode(each['xushuiliang'], 'gb2312'),
               unicode(each['ruku']),
               unicode(each['didinggaocheng'])
               )

table_html = u'''
<table border="1">
  <tr>
    <th>流域</th>
    <th>行政区</th>
    <th>河名</th>
    <th>水库名</th>
    <th>水库水位(米)</th>
    <th>水库水位变化</th>
    <th>需水量(亿立方米)</th>
    <th>入库(立方米/秒)</th>
    <th>堤顶高程(米)</th>
  </tr>
  {}
  </table>
'''.format(table_content)

unix_time = int(time.time())
html = open('daxingshuiku-{}.html'.format(unix_time), 'w')

html.write(
    u"""
    <html>
    <head>
    <title>大型水库报告</title>
    </head>
    <body>
""".encode('gb2312')
)

print(table_html)
html.write(table_html.encode('GBK'))
html.close()
