# -*- coding: utf-8 -*-

"""
@author: lan

@contact: 

@Created on: 2022/5/26
"""

import socket
#创建一个socket对象
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "127.0.0.1"
port = 9999
#连接服务端
client.connect((host, port))

while True:
    send_msg = input("发送: ")
    #设置退出条件
    if send_msg == "q":
        break
    send_msg = send_msg
    #发送数据，编码
    client.send(send_msg.encode("utf-8"))
    #接收服务端返回的数据
    msg = client.recv(1024)
    #解码
    print("接收：%s"% msg.decode("utf-8"))
#关闭客户端
client.close()
