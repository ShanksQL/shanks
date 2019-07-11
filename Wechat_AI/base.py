# -*- coding: utf-8 -*-
__author__ = "shanks"
__date__ = '2019/6/27 6:43 PM'


import itchat
from itchat.content import *
from .redis_server import RedisServer
import time
import logging
from concurrent.futures import ThreadPoolExecutor
from random import randint


class Application(object):
    user_list = dict()
    user_dict = dict()
    executor = ThreadPoolExecutor(max_workers=30)

    def __init__(self):

        self.redis = None

    @staticmethod
    def register_user():
        friends = itchat.get_friends(update=True)[0:]
        for _f in friends:
            Application.user_dict.setdefault(_f.UserName, dict(job_booking=True,
                                                               mark_remind={},
                                                               notice_chock_in=True,
                                                               NickName=_f.NickName))
        print("=======>>>好友列表:{}".format(','.join([_a['NickName'] for _a in Application.user_dict.values()])))

    def init_redis(self):
        self.redis = RedisServer()

    @staticmethod
    def loop_send():
        while True:
            l_time = time.localtime(time.time())
            if l_time.tm_wday in [0, 1, 2, 3, 4]:
                if l_time.tm_hour == 8 and l_time.tm_min == 20:
                    while l_time.tm_hour == 8 and l_time.tm_min < 30:
                        for _u in Application.user_dict:
                            if Application.user_dict[_u]['notice_chock_in']:
                                itchat.send_msg('该打卡了~亲', _u)
                        time.sleep(60)
                if l_time.tm_hour == 18 and l_time.tm_min == 35:
                    while l_time.tm_hour == 18 and l_time.tm_min < 40:
                        for _u in Application.user_dict:
                            if Application.user_dict[_u]['job_booking']:
                                itchat.send_msg('早报工、早回家、记得打卡哦', _u)
                        time.sleep(60)
                if l_time.tm_hour == 23 and l_time.tm_min == 59:
                    for _u in Application.user_dict:
                        Application.user_dict[_u].update(dict(job_booking=True,
                                                              notice_chock_in=True))
            time.sleep(60)

    def start(self):
        itchat.auto_login(True)
        itchat.run(True)
        self.init_redis()

    @staticmethod
    @itchat.msg_register(FRIENDS)
    def add_friend(msg):
        Application.user_dict.setdefault(msg.user.UserName, dict(job_booking=True,
                                                                 mark_remind={},
                                                                 notice_chock_in=True,
                                                                 NickName=''))
        msg.user.verify()
        msg.user.send('白茶清欢无别事、我在等风、也在等你\n回复【功能列表】即可查看现阶段已开发功能')

    @staticmethod
    @itchat.msg_register(TEXT)
    def text_reply(msg):
        with open("log.text", 'a') as f:
            f.write("在{}接收到了【{}】发来的消息:{}\n".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
                                                   msg.User.NickName, msg.text))
        f.close()
        if msg.text == "功能列表":
            with open("function.text", 'r') as f:
                data = f.read()
            msg.user.send(data)
            f.close()
        elif msg.text.find("你是谁") != -1:
            msg.user.send("那些都是我,或者那些都不是我,peace and love~")
        elif msg.text == "刷新好友":
            Application.register_user()
            msg.user.send("已刷新好友")
        elif msg.text == "开启功能":
            Application.executor.submit(Application.loop_send)
            msg.user.send("已开启功能")
        elif msg.text == "我已打卡":
            Application.user_dict[msg.FromUserName]['notice_chock_in'] = False
            msg.user.send("今天也是元气满满的一天")
        elif msg.text == "我已报工":
            Application.user_dict[msg.FromUserName]['job_booking'] = False
            msg.user.send("下班路上注意安全~")
        elif msg.text.find("多少分") != -1:
            msg.user.send("{}".format(randint(0, 100)))
        else:
            try:
                data = ''.join([_w for _w in msg.text if _w not in ['不', '吗', '?', '？']])
                msg.user.send(data.replace("我", "你"))
            except Exception as e:
                if msg.User.Sex == 1:
                    msg.user.send("我不知道你在说什么,但是你今天很帅")
                else:
                    msg.user.send("我不知道你在说什么,但是你今天真好看")
                logging.error('========>>>>error:{}'.format(e))

    @staticmethod
    @itchat.msg_register([PICTURE, RECORDING, ATTACHMENT, VIDEO])
    def download_files(msg):
        msg.download(msg.fileName)
        type_symbol = {PICTURE: 'img', VIDEO: 'vid', }.get(msg.type, 'fil')
        return '@%s@%s' % (type_symbol, msg.fileName)


if __name__ == '__main__':
    app = Application()
    app.start()
