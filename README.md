#摘要

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

一、	实现功能：
1. 登录自己的Instagram账户，获取关注用户列表；
2. 爬取Instagram关注用户的帖子，包括图片、视频、名称、内容、标题等数据。
3. 循环爬取关注用户的关注用户的帖子。

二、主要技术：
1. Webdriver
通过selenium库中的webdriver实现了登录instagram网站、输入账号密码、点击登录、定位网页元素并提取数据等操作。
2. requests
	通过requests库中的get()等功能，实现了对目标url的请求功能，并通过其响应得到Instagram上的视频、图片、文本等数据。
3. python3
	通过python实现了一些简单类和功能，完成了下载视频、下载图片、保存文本、循环爬取等操作。

三、具体实现


详细内容：
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
