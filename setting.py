# -*- coding: utf-8 -*-

"""
@author: lan

@contact: 配置

@Created on: 2022/5/27
"""
from feapder.utils.log import log
from Container import *

commandlist = ["createuser", "createroom", "joinroom", "help", "ready"]
commanddict = {
    "createuser": "cmdname username (need two params), it can create a user",
    "createroom": "cmdname roomname (need two params), it can create a room",
    "joinroom ": "cmdname roomname (need two params), it can join a room"
}







 