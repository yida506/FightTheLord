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
from Manager import *
from setting import *


# 用于存放当前创建的房间
room_pool = []
user_pool = []

def get_user(user_pool, user_addr):
    for i in user_pool:
        if i.address == user_addr:
            return i
    return False

def get_room(room_pool, roomname):
    for i in room_pool:
        if i.name == roomname:
            return i
    return False



class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.ip = ""            # ip地址
        self.port = 0           # 端口
        self.client_addr = []   # 链接客户端地址
        self.client_socket = [] # socket链接对象
        self.manager = Manager()
        super().__init__(request, client_address, server)

    def setup(self,):
        self.ip = self.client_address[0].strip()     # 获取客户端的ip
        self.port = self.client_address[1]           # 获取客户端的port
        log.debug(self.ip+" : "+str(self.port)+" 连接到服务器！")
        self.client_addr.append(self.client_address) # 保存到队列中
        self.client_socket.append(self.request)      # 保存套接字socket

    def handle(self):
        while True:
            time.sleep(1)
            try:
                data = self.request.recv(1024).decode('utf8')
                result = data.split()
                if result:    # 判断是否接收到数据
                    if result[0] not in commandlist:
                        message = "the input don't obey the rules"
                        raise Exception("the input don't obey the rules")

                    # 创建逻辑
                    elif result[0] == "CREATE":
                        if len(result) > 3:
                            message = "error"
                            raise Exception("error")
                        elif len(result) == 2:
                            param = result[1]
                            if param == "ROOM":
                                message = "create room"
                            elif param == "USER":
                                message = "create user"
                        elif len(result) == 3:
                            param = result[1]
                            if param == "ROOM":
                                message = "create room success"
                                nowroom = RoomItem(result[2])
                                room_pool.append(nowroom)

                            elif param == "USER":
                                message = "create user"
                                # 防止重名


                                nowuser = User(result[2])
                                nowuser.set_add(self.client_addr)
                                user_pool.append(nowuser)

                    elif result[0] == "SELECT":
                        if len(result) > 2:
                            message = "error"
                            raise Exception("error")
                        elif len(result) == 2:
                            param = result[1]
                            if param == "ROOM":
                                message = f"there are {len(room_pool)} rooms :"

                                # for i in room_pool:
                                #     message += f", {i.name}"
                            elif param == "USER":
                                for j in user_pool:
                                    if j.address == self.client_addr:
                                        message = f"{self.client_addr} binding user {j.name}"

                    elif result[0] == "REGISTER":
                        if len(result) == 2:
                            for i in user_pool:
                                if i.name == result[1]:
                                    i.set_add(self.client_addr)
                                    message = "binding success"

                        else:
                            message = f"{self.client_addr}, the input don't obey the rules"
                            raise Exception("the input don't obey the rules")

                    # 准备逻辑
                    elif result[0] == "READY":
                        if len(result) == 1:
                            nowuser = get_user(user_pool, self.client_address)
                            # 添加未绑定的逻辑
                            if not nowuser:
                                message = "the input don't obey the rules"
                            else:
                                nowuser.set_ready_status()
                                message = f"now {nowuser.name} is ready"
                            # todo 房间状态都为ready后，manager下发牌, 以及顺序队列

                        else:
                            message = "the input don't obey the rules"
                            raise Exception("the input don't obey the rules")

                    elif result[0] == "JOIN":
                        if len(result) == 2:
                            nowuser = get_user(user_pool, self.client_address)
                            nowroom = get_room(room_pool, result[1])
                            # TODO 用户状态异常捕获
                            nowroom.setuser(nowuser)
                            nowroom.show_info()

                    # CARD
                    elif result[0] == "PUT":
                        pass


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