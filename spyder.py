# -*- coding: utf-8 -*-
"""
Created on Wed Jun 19 15:20:27 2019

@author: Like
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
        self.account = '****'
        self.password = '****'
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
        
    def get_now_followings(self, url):
        #url 为博主首页
        #函数功能：获取当前博主的关注用户，并加入self.followings
        self.browser.get(url)
        time.sleep(5)
        self.browser.find_elements_by_class_name('g47SY')[2].click()
        time.sleep(5)
        nodes = self.browser.find_elements_by_class_name('FPmhX')
        print("关注人数：", str(len(nodes)))
        for i in range(min(len(nodes), 2)):
            self.followings.append(nodes[i].get_attribute('title'))
            
    def spyder(self):
        url_index = 'https://www.instagram.com/'
        path_base = 'D:\\instagram\\data\\'
        size = len(self.followings)
        for i in range(size):
            item = self.followings[i]
            url = url_index + item + '/'
            path_name = path_base + item
            #获取当前博主的关注用户，最多2个，进行层序爬取
            self.get_now_followings(url)
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
            self.browser.back()
            time.sleep(5)
            nodes = self.browser.find_elements_by_class_name('v1Nh3.kIKUG._bz0w')
            for node in nodes:
                shortcode.append(node.find_element_by_xpath("./a").get_attribute('href'))
            dr = 0    #dr记录每一个博主下面的子贴，从0开始编号，即子文件夹的名字
            for sc in shortcode:
                #请求博主的每一个帖子的url
#                url_now = url_index + 'p/' + sc
                print("正在爬取的帖子:" + sc)
                #每个帖子的保存路径
                path_one = path_name + '\\' + str(dr)
                if not os.path.exists(path_one):
                    # 如果不存在则创建目录
                    os.makedirs(path_one) 
                    print(path_one + ' 帖子子目录创建成功')
                else:
                    # 如果目录存在则不创建，并提示目录已存在
                    print(path_one + ' 帖子子目录已存在')
                dr += 1    
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
                        else:
                            self.download_video(node["video_url"], path_one)
                        #其他内容写进content.txt
                        f = open(path_one + '\\' + 'content.txt','w', encoding = 'utf-8')
                        f.writelines("username:" + node["username"])
                        f.writelines("title:" + node["title"] + ' \r\n')
                        f.writelines("content:" + node["content"] + ' \r\n')
                        f.writelines("is_video:" + str(node["is_video"]) + "\r\n")
                        if(node["is_video"]):
                            f.writelines("video_url" + node["video_url"] + "\r\n")
                        else:
                            f.writelines("pic_url" + node["pic_url"] + "\r\n")
                        f.close()
        self.followings = self.followings[size:]
        
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
            print("图片下载失败:", dic)
        
    def download_video(self, url, file_path):
        try:
            res = requests.get(url, stream=True)
            # 写入收到的视频数据
            file_name = self.get_time_as_filename() + '.mp4'
            file_path += '\\' + file_name
            with open(file_path, 'ab') as file:
                file.write(res.content)
                file.flush()
        except Exception as e:
            dic = {'url': url, 'file_path': file_path}
            print("视频下载失败:", dic)
                   
if __name__ == '__main__':
    while True:
        s = input("Please input the number of degree:")
        if s.isdigit():
            break
        else:
            print("Error! Please input an Integer!")
    ins = Ins_Crawler()
    ins.get_page()
    for i in range(int(s)):
        if(len(ins.followings) > 0):
            ins.spyder()
    ins.browser.close()
    print("Done!")
