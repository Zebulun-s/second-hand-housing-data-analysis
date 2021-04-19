import requests
from lxml import etree
import time
import os
import csv
#请求网页，爬取数据
if not os.path.exists("lianjia"):
    os.mkdir("./lianjia")
#写模式打开csv文件,循环，模式写“a"
csv_obj = open('lianjia.csv', 'a', encoding="utf-8-sig")
#写入一行标题
csv.writer(csv_obj).writerow(["成交小区", "成交价(万元)", "成交楼层", "单价每平（元）", "朝向","成交时间"])
#爬取前40页
for page in range(1, 60):
    print('===========================正在下载第{}页数据================================'.format(page))
    time.sleep(1)
    url = 'https://sr.lianjia.com/chengjiao/pg{}/'.format(page)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36'
    }

    response = requests.get(url=url, headers=headers).text
    time.sleep(1)
    #print(response)
    #parsel.Selector将请求后的字符串格式解析成re,xpath,css进行内容的匹配
    tree = etree.HTML(response)
    li_text = tree.xpath('/html/body/div[5]/div[1]/ul/li')
    # xpath解析最好用复制法
    for li in li_text:
        ti = li.xpath("./div/div[1]/a/text()")
        zongjia = li.xpath("./div/div[2]/div[3]/span/text()|./div/div[2]/div[3]/text()")
        lou = li.xpath("./div/div[3]/div[1]/text()")
        danjia = li.xpath("./div/div[3]/div[3]/span/text()")
        chaoxiang = li.xpath("./div/div[2]/div[1]/text()")
        cjshijian=li.xpath("./div/div[2]/div[2]/text()")
        csv.writer(csv_obj).writerow([ti, zongjia, lou, danjia, chaoxiang,cjshijian])
csv_obj.close()
print("数据下载完成")
