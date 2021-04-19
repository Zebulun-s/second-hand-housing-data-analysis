#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#爬取链家网上饶市二手房成交数据
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


# In[62]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib as mpl
import os


# In[3]:


os.chdir("D:\\32189\\python  pyCharm 代码\\项目1\\")


# In[4]:


data=pd.read_csv("lianjia—shangrao数据.csv.csv")


# In[5]:


## 3) 判断是否有缺失值
data.isnull().sum()


# In[6]:


#删除缺省值
data.dropna(inplace = True)


# In[7]:


#检查是否删除空值
data.isnull().sum()


# In[8]:


## 1）数据总体情况
print(f'样本量共有 {data.shape[0]} 行')


# In[9]:


## 4) 查看数据类型
data.dtypes


# In[10]:


#重复值处理
data.drop_duplicates(inplace=True)


# In[11]:


## 1）数据总体情况
print(f'处理后样本量共有 {data.shape[0]} 行')


# In[12]:


# 描述性分析
data.describe()
#该地区的平均总价为86.102万元，最小成交价为15万元，最贵的房子为728万元
#该地区的平均单价为每平8083.34元，最便宜的为每平1061元，


# In[13]:


data.head()


# In[14]:


#python DataFrame筛选符合特定条件的行,查看最贵的房子的详细信息
data[data['成交价（万元）']==max(data['成交价（万元）'])]


# In[15]:


#查看成交单价超过300万元的成交单字，数目占比不大可当异常值处理
(data['成交价（万元）'] > 300.0).sum()


# In[16]:


# 将高于房价300万的删除,当作异常值进行处理
data.drop(index = data[data['成交价（万元）'] > 300.0].index, inplace=True)


# In[17]:


#新增一列月份
data.loc[:,"月份"]=data["成交时间"].map(lambda x:x[:7])
data.loc[:,'小区'] = data['成交小区'].map(lambda x:x.split()[0])
data.loc[:,'户型'] = data['成交小区'].map(lambda x:x.split()[1])


# In[18]:


#避免格式不对会造成数据格式转换错误，过滤格式不符的行
(data['成交小区'].str.split().map(len) != 3).sum()


# In[19]:


#以两个空格为格式
data=data[data['成交小区'].str.split().map(len) == 3]


# In[20]:


data.loc[:,'面积'] = data['成交小区'].map(lambda x:x.split()[2])


# In[21]:


del data["成交小区"]


# In[22]:


data.loc[:,'楼层'] = data['成交楼层'].map(lambda x:x.split("(")[0])
data.loc[:,'楼型'] = data['成交楼层'].map(lambda x:x.split(")")[1])
data.loc[:,'朝向细节'] = data['朝向'].map(lambda x:x.split("|")[0])
data.loc[:,'装修'] = data['朝向'].map(lambda x:x.split("|")[1])


# In[23]:


del data["朝向"]


# In[24]:


data['面积'] = data['面积'].str.replace('平米','').astype(np.float32)


# In[25]:


data['面积'] = data['面积'].astype(np.int)


# In[48]:


#如果
louceng=["南","南北","东南"]
data["朝向细节"]=['其它' if i not in louceng else i for i in data["朝向细节"]]


# In[49]:


#对朝向进行统计，太多特殊朝向，所以将特殊朝向改为”其它“
data["朝向细节"].value_counts()


# In[29]:


print("上饶二手房的平均单价为：{}元/每平".format(round(data["单价每平（元）"].mean(),2)))


# In[32]:


y1= round(data.groupby(by=['月份'])['成交价（万元）'].sum(),2)


# In[33]:


y1


# In[34]:


#设置字体
mpl.rcParams['font.sans-serif'] = ['KaiTi']
plt.rcParams['axes.unicode_minus']=False


# In[64]:


plt.figure(figsize=(8,6))
plt.title("每个月的成交量情况",fontsize=25)
plt.bar(y1.index,y1,color="Fuchsia")
'''
2021年3月份成交额最大，前一个月2021年2月成交额最小，其它月份波动不大
'''


# In[65]:


#sns.countplot()函数,以bar的形式展示每个类别的数量
plt.figure(figsize=(8,4))
plt.title("每个月的成交量情况",fontsize=25)
order = sorted(data['月份'].value_counts().index)
sns.countplot(x=data['月份'],order=order)
#每个月的成交量和每月成交额基本吻合


# In[66]:


plt.figure(figsize=(20,4))
#统计小区的房数,打印拍前面成交数量前15的小区
plt.title("成交数量排名在前15的小区",fontsize=25)
top15=data['小区'].value_counts()[:15].index
sns.countplot(x=data['小区'],order=top15)


# In[40]:


print(top15)


# In[67]:


f,[ax1,ax2] = plt.subplots(1,2,figsize = (20,10))
ax1.set_title('房源面积出售情况',fontsize=25)
ax2.set_title('房源面积和出售价格的关系',fontsize=25)
#通过柱状图可知，房源面积大多超过100平米以上
x3=data["面积"]
sns.distplot(x3,bins = 20,ax = ax1,color = 'g')
sns.kdeplot(x3,shade = True,ax = ax1)

# 建房面积和出售价格的关系,画散点图，基本呈线上关系
sns.regplot(x = '面积',y = '成交价（万元）',data = data,ax =ax2)


# In[68]:


#由图像知中低高楼层、装修、朝向占比分布
f,[ax1,ax2,ax3] = plt.subplots(1,3,figsize = (20,10))
color1=["#DA70D6","#BA55D3","#9932CC"]
color2=["#EE6AA7","#CD6090","#8B0A50","#FF82AB"]
color3=["#FFFF00","#CDCD00","#FFD700","#EEB422"]
ax1.set_title('房屋楼层分布',fontsize=25)
ax2.set_title('房屋装修分布',fontsize=25)
ax3.set_title('房屋朝向分布',fontsize=25)
data["楼层"].value_counts().plot.pie(autopct='%.2f%%',colors=color1,ax = ax1,fontsize=12,figsize=(15,5))
data["装修"].value_counts().plot.pie(autopct='%.2f%%',colors=color2,ax = ax2,fontsize=12,figsize=(15,5))
data["朝向细节"].value_counts().plot.pie(autopct='%.2f%%',colors=color3,ax = ax3,fontsize=12,figsize=(15,5))


# In[45]:


#房屋户型分布：3室2厅最多，然后4室2厅
f,ax1 = plt.subplots(figsize = (10,10))
sns.countplot(y = '户型',data = data,ax = ax1)
ax1.set_title('房屋户型分布',fontsize=25)
ax1.set_xlabel('数量')
ax1.set_ylabel('户型')


# In[40]:


data


# In[ ]:




