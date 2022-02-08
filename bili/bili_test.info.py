#!/usr/bin/env python
# -*- coding:utf-8 -*-

import requests
import time
import threading

from concurrent import futures

from plotly.graph_objs import Bar
from plotly import offline



result=[]
lock=threading.Lock()
total=1

def run(url):
	'''获得数据并存储'''
	#启动爬虫
	global total
	#测试网址：https://api.bilibili.com/x/web-interface/archive/stat?aid=15906633
	headers = {
    "X-Requested-With": "XMLHttpRequest",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
	}
	r=requests.get(url,headers=headers,timeout=6)
	time.sleep(0.5) #延迟，避免太频繁。
	#print(f"Status code:{r.status_code}")
	#将API响应赋给一个变量
	req_dict=r.json()

	#分解获得需要的数据。
	try:
		data=req_dict["data"]
		if data["view"]!="--" and data["aid"]!=0:
			video=(
				data["aid"],		#视频编号
				data["view"],		#播放量
				data["danmaku"],	#弹幕数
				data["reply"],		#评论数
				data["favorite"],	#收藏数
				data["coin"],		#硬币数
				data["share"],		#分享数
				"",		#视频名称，暂时为空
			)
			with lock:
				result.append(video)
				if total%100==0:
					print(total)
				total+=1
	except:
		pass

def save_file():
	'''将数据保存到文件中'''
	temp=""

	for row in result:
		temp+=(f"\n{row}")
	filename="bili_data.csv"
	with open(filename,'w') as fo:
		fo.write("视频编号,播放量,弹幕数,评论数,收藏数,硬币数,分享数,视频名称")
		fo.write(temp)



if __name__=="__main__":
	#create_db()
	print("启动爬虫，开始爬取数据")
	for i in range(1590663,1590669):
		begin=10*i
		urls=[
			f"https://api.bilibili.com/x/web-interface/archive/stat?aid={j}"
			for j in range(begin,begin+10)
		]
		with futures.ThreadPoolExecutor(64) as executor:
			executor.map(run,urls)

	save_file()

	print(f"爬虫结束，共为您爬取到{total}条数据。")
