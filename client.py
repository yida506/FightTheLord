# -*- coding: utf-8 -*-

"""
@author: lan

@contact: 服务端 用于接收

@Created on: 2022/5/26
"""

from feapder.utils.log import log
import socket


client = socket.socket() #定义协议类型,相当于生命socket类型,同时生成socket连接对象
client.connect(('127.0.0.1',9999))
while True:
    msg = input("")
    client.send(msg.encode("utf8"))
    data = client.recv(1024)
    log.info(f"{data.decode()}")

client.close()

