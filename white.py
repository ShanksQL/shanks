# -*- coding: utf-8 -*-
__author__ = "shanks"
__date__ = '2019/5/30 9:25 AM'

import requests

# 机器人链接
url = 'https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=c02e4ea1-9629-4628-ba26-5f7779736298'
headers = {'Content-Type': 'application/json'}
form_data = {
    "msgtype": "text",
    "text": {
        "content": "你今天真好看"
    }
}
requests.post(url=url, headers=headers, json=form_data)

"""
form_data样板
# 文本
{
    "msgtype": "text",
    "text": {
        "content": "广州今日天气：29度，大部分多云，降雨概率：60%",  
        "mentioned_list":["wangqing","@all"],
        "mentioned_mobile_list":["13800001111","@all"] 
    }
}
content # 文本内容，最长不超过2048个字节，必须是utf8编码
mentioned_list  # userid的列表，提醒群中的指定成员(@某个成员)，@all表示提醒所有人，如果开发者获取不到userid，可以使用mentioned_mobile_list
mentioned_mobile_list  # 手机号列表，提醒手机号对应的群成员(@某个成员)，@all表示提醒所有人

# markdown
{
    "msgtype": "markdown",
    "markdown": {
        "content": "实时新增用户反馈<font color=\"warning\">132例</font>，请相关同事注意。\n
         >类型:<font color=\"comment\">用户反馈</font> \n
         >普通用户反馈:<font color=\"comment\">117例</font> \n
         >VIP用户反馈:<font color=\"comment\">15例</font>"
    }
}
# markdown内容，最长不超过2048个字节，必须是utf8编码

# 图片模式
{
    "msgtype": "image",
    "image": {
        "base64": "DATA",
        "md5": "MD5"
    }
}
base64 # 图片内容的base64编码
md5 # 图片内容（base64编码前）的md5值

# 图文类型
{
    "msgtype": "news",
    "news": {
       "articles" : [
           {
               "title" : "中秋节礼品领取",
               "description" : "今年中秋节公司有豪礼相送",
               "url" : "URL",
               "picurl" : "http://res.mail.qq.com/node/ww/wwopenmng/images/independent/doc/test_pic_msg1.png"
           }
        ]
    }
}
title # 标题
description # 描述
url # 点击后跳转的链接
picurl # 图文消息的图片链接，支持JPG、PNG格式，较好的效果为大图 1068*455，小图150*150。
"""
