# -*- coding: UTF-8 -*-

'''
Created on 2019-12-26
Jason
@author: 15108
'''

import requests
import time
import os
import uuid
import datetime
import random
from bs4 import BeautifulSoup

# 图片保存路径
#root_path = "D://11-Picture"
root_path = "D://11-Picture//20191225-2"

user_agents = [
    'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
    'Opera/9.25 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.8.0.12) Gecko/20070731 Ubuntu/dapper-security Firefox/1.5.0.12',
    'Lynx/2.8.5rel.1 libwww-FM/2.14 SSL-MM/1.4.1 GNUTLS/1.2.9',
    "Mozilla/5.0 (X11; Linux i686) AppleWebKit/535.7 (KHTML, like Gecko) Ubuntu/11.04 Chromium/16.0.912.77 Chrome/16.0.912.77 Safari/535.7",
    "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:10.0) Gecko/20100101 Firefox/10.0 ",
]


def download_image(url, folder):
    try:
        time.sleep(0.2)
        if url is None:
            return ""

        response = requests.get(url)
        img = response.content
        # 将他拷贝到本地文件 w 写  b 二进制  wb代表写入二进制文本
        # 保存路径
        ext = os.path.splitext(url)
        # time_format = datetime.datetime.now().strftime("%Y%m%d")
        relative_path = "/" + folder + "/"
        absolute_path = root_path + relative_path

        if not os.path.exists(absolute_path):
            os.makedirs(absolute_path)

        imgName = folder + "_" + str(uuid.uuid1()).replace("-", "") + ext[1]
        relative_path = relative_path + imgName
        absolute_path = absolute_path + imgName

        with open(absolute_path, 'wb') as f:
            f.write(img)
        print(folder, url, "******下载成功")
        return relative_path
    except Exception as ex:
        print(folder, url, "--------出错继续----", ex)
    return ""


def parse_sonp(html):
    try:
        return BeautifulSoup(html, "html5lib")
    except Exception as e:
        print(e)
    return None


def request(url):
    try:
        time.sleep(1)
        print("发出请求：", url)
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
        }
        htmlobj = requests.get(url,
                               timeout=4,
                               headers=headers)
        htmlcount = htmlobj.text
        htmlcount = htmlcount.encode("gbk", 'ignore').decode("gbk", "ignore")
        if len(htmlcount) > 0:
            return htmlcount
    except Exception as e:
        print("request", e)

    return None


def get_article_url():
    article_set = set()
    url = "https://cb.bbcb.xyz/thread0806.php?fid=16&search=&page="
    for i in range(1, 166):
        try:
            visitedurl = url + str(i)

            htmlcontent = request(visitedurl)
            if htmlcontent is None or len(htmlcontent) == 0:
                continue

            sonpobj = parse_sonp(htmlcontent)
            if sonpobj is None:
                continue

            tableobj = sonpobj.find("table", {"id": "ajaxtable"})
            elea = tableobj.find_all("a")
            for a in elea:
                href = a.get("href")
                if href.find("htm_data") != -1:
                    article_set.add("https://cb.bbcb.xyz/" + href)

        except Exception as e:
            print(e)
    return article_set


def get_image():
    article_set = get_article_url()
    index = 1
    dirname = ""
    for articel_url in iter(article_set):
        # 图片链接对照文件
        unionFile = open('D://11-Picture//20191225-2//union.txt', 'a', encoding='utf8')
        dirname = "gai-" + str(index)
        try:
            htmlcontent = request(articel_url)
            if htmlcontent is None or len(htmlcontent) == 0:
                continue

            sonpobj = parse_sonp(htmlcontent)
            if sonpobj is None:
                continue

            # <img>
            imgobjs = sonpobj.find_all("img")
            for img in imgobjs:
                imgurl = img.get("src")
                if imgurl is None or len(imgurl) == 0:
                    imgurl = img.get("data-src")
                if imgurl is not None and len(imgurl) != 0:
                    download_image(imgurl, dirname)
            # <input>
            inputobjs = sonpobj.find_all("input")
            for inputimg in inputobjs:
                imgurl = inputimg.get("src")
                if imgurl is None or len(imgurl) == 0:
                    imgurl = inputimg.get("data-src")
                if imgurl is not None and len(imgurl) != 0:
                    download_image(imgurl, dirname)

        except Exception as e:
            print(e)
        finally:
            unionFile.write(articel_url + "    ###   " + dirname + "\n")
            unionFile.close()
            index += 1


get_image()
