# Ins_spyder 

基本说明
1.获取关注的人, 在网页首先登录, 点击标识，到达个人页面

2.点击“正在关注”

3.获取所关注的人的帖子

    点击某一个关注的人，则出现此人的帖子页面，分析此网页的源码返回，点击右键“检查”，分析源码，定位帖子中的图片
 
4.分析结果可见，帖子图片、视频、内容、username等信息是在<script>里，实际里面是json字符串

    "display_url"：图片的地址
    "is_video"：是否是视频
    "video_url":如果是视频，则获取视频地址
    "title"获取到文章的标题，有时为空
    "edge_media_to_caption"-"edges"-"node"-"text"：获取到文章的内容。
    
5.成功找到我们所需要的数据，就可以进行下载保存等存储操作了，包括存储到mysql数据库和下载图片、视频文件。
获取关注的人

一、获取关注人列表
1.	在网页首先登录
如图1，请求https://www.instagram.com/accounts/login/?source=auth_switcher
 
![image](https://raw.githubusercontent.com/buptlk/Ins_spyder/master/picture/t1.png)
图1

2.	输入账号密码，点击“登录”，得到图2结果
 
![image](https://raw.githubusercontent.com/buptlk/Ins_spyder/master/picture/t2.png)
图2

3.	点击“以后再说”，得到如图3的结果。
 
![image](https://raw.githubusercontent.com/buptlk/Ins_spyder/master/picture/t3.png)
图3

4.	点击进入“个人主页”，得到图4结果。
  
![image](https://raw.githubusercontent.com/buptlk/Ins_spyder/master/picture/t4.png)
图4

5.	点击“正在关注”，到下图5
 
 
![image](https://raw.githubusercontent.com/buptlk/Ins_spyder/master/picture/t5.png)
   图5

6.	右键“检查”，分析图6 的Elements，发现有且仅有关注的用户元素具有相同的class_name，即”FPmhX”。通过定位这个类元素获取其”title”，可以得到所有用户名。
 
![image](https://raw.githubusercontent.com/buptlk/Ins_spyder/master/picture/t6.png)
  图6
  
二、获取所关注的人的帖子

1.	点击图5中的关注的用户，进入此用户的主页。用户主页的url可以通过” https://www.instagram.com/” + 图6获取的用户名组成。
 
![image](https://raw.githubusercontent.com/buptlk/Ins_spyder/master/picture/t7.png)
图7

2.	分析此网页的源码。
点击右键“检查”，进入界面源码分析，并定位到帖子元素，发现有且仅有帖子同时具有v1Nh3 kIKUG _bz0w三种class_name
 
![image](https://raw.githubusercontent.com/buptlk/Ins_spyder/master/picture/t8.png)
图8

3.	进入主贴界面。
点击其中一条帖子，如图9，发现每一条帖子的url都可以通过图8中定位元素的字标签href属性得到。
 
![image](https://raw.githubusercontent.com/buptlk/Ins_spyder/master/picture/t9.png)
图9
4.	右键“检查”获取“Network”处的“Response”。

![image](https://raw.githubusercontent.com/buptlk/Ins_spyder/master/picture/t10.png)
 图10
5.	分析可知，结果是在<script>里，实际里面是json字符串，可将此行的所有结果都拿出来，放在“json在线格式化”，可清晰看出返回的内容，如图11
 
![image](https://raw.githubusercontent.com/buptlk/Ins_spyder/master/picture/t11.png)
图11

6.  分析图11中的结果。
        1.”display_url“：图片的地址
        2.”is_video“：是否是视频
        3.”video_url“:如果是视频，则获取视频地址
        4.”title”获取到文章的标题，有时为空
        5.“edge_media_to_caption”-”edges”-”node”-”text”：获取到文章的内容。
        如果”"is_video":true“，则此处还会有一个”video_url“字段值。所以，此地址https://www.instagram.com/p/BzEkKbnHV0K/ 的请求结果，就是我们所需要的。而此地址的组成，是基本地址”https://www.instagram.com/“+图8中定位元素的字标签href属性组成。

总结：
1.	通过“获取关注的人”获取到的图6 的结果，获取到关注用户字段值，组成地址“https://www.instagram.com/jaychou/”，请求此地址，获取到关注人的主页。
2.	通过关注的人定位图8中的每一条帖子的元素，组成地址“https://www.instagram.com/p/ByqNmF7i1_x/”，获取到图9的结果。
3. 分析图9源码，定位得到包含我们所需数据的json字符串，并解析字符串。
4. 下载图片、视频、博主id、帖子内容等数据。

主要代码：
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 15:20:27 2019

@author: LiKan
"""
import time
from selenium import webdriver
import requests
from lxml import etree
import json
#import pymysql
import os
from PIL import Image
from io import BytesIO

class Ins_Crawler:
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.followings = []
        self.account = 'sanxin0624'
        self.password = '00000OOOOO'
#        self.link_db()
        
#    def link_db(self):
#        try:
#            db = pymysql.Connect(host='10.1.30.10/24', port=3306, user='root', 
#                                 passwd='123', db='ins', charset='utf8')
#            print("Database connected!")
#            return db
#        except Exception as e:
#            print("connection failed")
#            return None
        
    def get_page(self):
        self.browser.get("https://www.instagram.com/accounts/login/?source=auth_switcher")
        time.sleep(5)
        self.browser.maximize_window()
        self.browser.find_element_by_name('username').send_keys(self.account)
        print('已输入账号！')
        self.browser.find_element_by_name('password').send_keys(self.password)
        print('已输入密码！')
        #点击登录  或者使用send_keys(KeysENTER) 输入回车
        self.browser.find_element_by_class_name("_0mzm-.sqdOP.L3NKy").click()
        print('已登录！')
        time.sleep(10)
        #处理弹窗，点击“以后再说”
        self.browser.find_element_by_class_name("aOOlW.HoLwm").click()
        print("已关闭弹窗！")
        #点击“个人主页”
        self.browser.find_element_by_class_name("glyphsSpriteUser__outline__24__grey_9.u-__7").click()
        #点击“正在关注”
        #相同'g47SY'属性的class有三个，选择list中的第三个为“正在关注”
        time.sleep(10)
        self.browser.find_elements_by_class_name('g47SY')[2].click()
        #每个关注用户相同的class name:'FPmhX notranslate _0imsa '
        time.sleep(5)
        nodes = self.browser.find_elements_by_class_name('FPmhX')
        print("关注人数：" + str(len(nodes)))
        for item in nodes:
            self.followings.append(item.get_attribute('title'))
            print("item:" + item.get_attribute('title'))
        
    def spyder(self):
        url_index = 'https://www.instagram.com/'
        path_base = 'D:\\instagram\\data\\'
        for item in self.followings:
            url = url_index + item + '/'
            path_name = path_base + item
            if not os.path.exists(path_name):
                # 如果不存在则创建目录
                os.makedirs(path_name) 
                print(path_name + ' 创建成功')
            else:
                # 如果目录存在则不创建，并提示目录已存在
                print(path_name + ' 目录已存在')
                
            #当前博主的所有帖子链接
            shortcode = []
            print("正在爬取博主链接：" + url)
            self.browser.get(url)
            time.sleep(5)
            nodes = self.browser.find_elements_by_class_name('v1Nh3.kIKUG._bz0w')
            for node in nodes:
                shortcode.append(node.find_element_by_xpath("./a").get_attribute('href'))
            index = 0
            for sc in shortcode:
                #请求博主的每一个帖子的url
#                url_now = url_index + 'p/' + sc
                print("正在爬取的帖子:" + sc)
                #每个帖子的保存路径
                path_one = path_name + '\\' + str(index)
                if not os.path.exists(path_one):
                    # 如果不存在则创建目录
                    os.makedirs(path_one) 
                    print(path_one + ' 帖子子目录创建成功')
                else:
                    # 如果目录存在则不创建，并提示目录已存在
                    print(path_one + ' 帖子子目录已存在')
                index += 1
                response = requests.get(sc)
                html = etree.HTML(response.content.decode())  
                all_a_tags = html.xpath('//script[@type="text/javascript"]/text()')  
                for a_tag in all_a_tags:  
                    if a_tag.strip().startswith('window._sharedData'):  
                        index = a_tag.find('{')  
                        data = a_tag[index:len(a_tag) - 1]  
                        js_data = json.loads(data)  
                        media_dict = js_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]  
                        # 存储文章内容字典  
                        node = {}  
                        # 1,获取文章标题  
                        if 'title' in media_dict:  
                            node["title"] = media_dict["title"]  
                        else:  
                            node["title"] = ""  
                        # 2,获取文章内容  
                        node["content"] = media_dict["edge_media_to_caption"]["edges"][0]["node"]["text"]  
                        # 3,is_video  
                        node["is_video"] = media_dict["is_video"]  
                        # 4,获取图片或视频  
                        if node["is_video"]:  
                            node["video_url"] = media_dict["video_url"]  
                        else:  
                            node["pic_url"] = media_dict["display_url"]  
                        # 5,获取此文章的作者  
                        node["username"] = media_dict["owner"]["username"]  
                        # 6，获取文章的shortcode  
                        node["shortcode"] = media_dict["shortcode"] 
                        
                        if not node["is_video"]:
                            self.download_image(node["pic_url"], path_one)
#                        else:
#                            self.download_video(node["video_url"], path_one)
                        #其他内容写进content.txt
                        f = open(path_one + '\\' + 'content.txt','w')
                        f.writelines(node["title"])
                        f.writelines(node["content"])
                        f.writelines(node["username"])
                        f.close()
                        
    def get_time_as_filename(self):
        now_time = time.time()
        now_time_Array = time.localtime(now_time)
        file_name = time.strftime("%Y_%m_%d_%H%M%S", now_time_Array)
        return file_name
    
    def download_image(self, url, file_path):
        try:
            html = requests.get(url)
            image = Image.open(BytesIO(html.content))
            file_name = self.get_time_as_filename() + '.jpg'
            file_path += '\\' + file_name
            image.save(file_path)
        except:
            dic = {'url': url, 'file_path': file_path}
            print("下载失败:", dic)
        
    def download_video(self, url, file_path):
        try:
            res = requests.get(url, stream=True)
            # 写入收到的视频数据
            with open(file_path, 'ab') as file:
                file.write(res.content)
                file.flush()
        except Exception as e:
            dic = {'url': url, 'file_path': file_path}
            print("下载失败:", dic)
                   
if __name__ == '__main__':
    ins = Ins_Crawler()
    ins.get_page()
    ins.spyder()
    print("Done!")
