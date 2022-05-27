# -*- coding: utf-8 -*-

"""
@author: lan

@contact:  客户端

@Created on: 2022/5/26
"""
import socketserver
from feapder.utils.log import log
import socket
import threading
import time
from Container import *
from setting import *


# 用于存放当前创建的房间
roomitem = []
people_pool = []

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.ip = ""            # ip地址
        self.port = 0           # 端口
        self.client_addr = []   # 链接客户端地址
        self.client_socket = [] # socket链接对象
        super().__init__(request, client_address, server)

    def setup(self,):
        self.ip = self.client_address[0].strip()     # 获取客户端的ip
        self.port = self.client_address[1]           # 获取客户端的port
        log.debug(self.ip+" : "+str(self.port)+" 连接到服务器！")
        self.client_addr.append(self.client_address) # 保存到队列中
        self.client_socket.append(self.request)      # 保存套接字socket

    def handle(self):
        while True:
            try:
                time.sleep(1)
                data = self.request.recv(1024).decode('utf8')
                result = data.split()
                if result:    # 判断是否接收到数据
                    if result[0] not in commandlist:
                        message = "the input don't obey the rules"
                        raise Exception("the input don't obey the rules")

                    if result[0] == "createuser":
                        if len(result) != 2:
                            message = "createuser only need a param, please try again"
                            raise Exception("createuser only need a param, please try again")
                        people = People(result[1])
                        message = f"now people's name is {people.name}, and now status is {people.ready_status}"
                        log.info(f"now people's name is {people.name}, and now status is {people.ready_status}")

                    elif result[0] == "createroom":
                        if len(result) != 2:
                            message = "createroom only need a param, please try again"
                            raise Exception("createroom only need a param, please try again")
                        nowroom = RoomItem(result[1])
                        message = f"now room's name is {nowroom.name}, and now status is {nowroom.roomstatus}"
                        log.info(f"now room's name is {nowroom.name}, and now status is {nowroom.roomstatus}")
                        roomitem.append(nowroom)

                    elif result[0] == "joinroom":
                        if people:
                            log.info(f"now people's name is {people.name}, and now status is {people.ready_status}")
                            roomname = result[1]
                            findroom = False
                            for i in roomitem:
                                if i.name == roomname:
                                    i.roomlist.append(people)
                                    message = f"now people's name is {people.name}, and now status is {people.ready_status}, now room status "
                                    log.info(f"now people's name is {people.name}, and now status is {people.ready_status}, now room status ")
                                    findroom = True
                            if findroom == False:
                                message = "the room isn't exist, please create room"
                                raise Exception("the room isn't exist, please create room")
                        else:
                            message = "there isn't any user, please create"
                            raise Exception("there isn't any user, please create")

                    elif result[0] == "ready":
                        if people:
                            people.ready_status = True
                            message = f"now people's name is {people.name}, and now status is {people.ready_status}"
                            log.info(f"now people's name is {people.name}, and now status is {people.ready_status}")
                        else:
                            message = "there isn't any user, please create"
                            raise Exception("there isn't any user, please create")

                    elif result[0] == "help":
                        if len(result) != 1:
                            message = "help cmd doesn't need any param"
                            raise Exception("help cmd doesn't need any param")
                        for keys in commanddict.keys():
                            self.request.sendall((f" {keys} : {commanddict[keys]} \n ").encode("utf8"))
                    if message:
                        self.request.sendall(message.encode("utf8"))

            except Exception as e:
                log.error(e)
                if message:
                    self.request.sendall(message.encode("utf8"))

    def finish(self):
        log.error(self.ip+" : "+str(self.port)+"断开连接！")
        self.client_addr.remove(self.client_address)
        self.client_socket.remove(self.request)


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999 #windows

    server = socketserver.ThreadingTCPServer((HOST, PORT), ThreadedTCPRequestHandler)   #线程
    server.serve_forever() # 永远运行
