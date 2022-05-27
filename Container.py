# -*- coding: utf-8 -*-

"""
@author: lan

@contact: 

@Created on: 2022/5/25 21:58
"""
from Card import *
from Rule import *
import random
from feapder.utils.log import log
from setting import *
import time

class People:

    BOSS = "BOSS"
    NORMAL = "NORMAL"

    def __init__(self, name):
        self.name = name
        self.ready_status = False

    def set_ready_status(self, status: bool):
        self.ready_status = status

    def get_ready_status(self):
        return self.ready_status

    def set_peopletype(self, peopletype: str):
        if peopletype:
            self.peopletype = People.BOSS
        else:
            self.peopletype = People.NORMAL

    def set_item(self, item):
        self.item = item

    def delete_seq(self, sequence):
        sequencelist = sequence.split()
        for j in sequencelist:
            if j in self.item:
                self.item.pop(self.item.index(j))

class RoomItem:

    def __init__(self, name):
        self.roomlist = []
        self.name = name

    def setuser(self, user):
        if len(self.roomlist) >= 3:
            raise Exception("the room is full, you can choose other room")
        self.roomlist.append(user)

    # def __str__(self):
    #     return "now the people num is " + str(len(self.roomlist)) + " and now the room status is " + str(self.roomstatus)

    def show_info(self):
        if self.roomstatus:
            for i in self.roomlist:
                log.debug("now , " + str(i.name) + " has " + str(len(i.item)) + " left ")
                # raise Exception("The geme isn't start please wait")
        else:
            raise Exception("The geme isn't start please wait")

    @property
    def roomstatus(self):
        if len(self.roomlist) == 3:
            for i in self.roomlist:
                if i.ready_status == False:
                    return False
            return True
        return False

class Container:

    def __init__(self):
        self.carditem = Card().basecard + Card().kingcard

    def assignCard(self):
        '''
        :return:
        '''
        random.shuffle(self.carditem)
        normalitem1 = self.carditem[:17]
        normalitem2 = self.carditem[17:34]
        bossitem = self.carditem[34:]
        return bossitem,normalitem1,normalitem2

    def run(self):

        # create user
        people1 = People('lan') #boss
        people2 = People('lan2')
        prople3 = People('lan3')

        # 创建房间
        room = RoomItem()
        room.setuser(people1)
        # log.info(room)
        room.setuser(people2)
        room.setuser(prople3)

        random.shuffle(room.roomlist)
        bossitem, normalitem1, normalitem2 = self.assignCard()

        room.roomlist[0].set_item(bossitem)
        room.roomlist[0].set_peopletype(True)
        room.roomlist[1].set_item(normalitem1)
        room.roomlist[1].set_peopletype(False)
        room.roomlist[2].set_item(normalitem2)
        room.roomlist[2].set_peopletype(False)

        room.show_info()
        # 存放整体链表 用于打印日志
        linkitem = []
        game_on = True
        index = 0
        while game_on:
            link_on = True
            while link_on:
                linklist = Linklist()
                # 轮询
                linklist.initvaluelist()
                # log.info(room.roomlist)
                while linklist.linkstatus:
                    if len(room.roomlist[0].item) == 0:
                        game_on = False
                        link_on = False
                        break
                    if index % 3 == 0:
                        value = room.roomlist[0].item[0]
                        linklist.nodeadd(Node(f"{value}", people=room.roomlist[index % 3]))
                        room.roomlist[0].delete_seq(f"{value}")
                    else:
                        linklist.nodeadd(Node(False, people=room.roomlist[index % 3]))
                    linklist.initvaluelist()
                    index += 1
                linkitem.append(linklist)
                # linklist.nodeadd(Node(False, people=room.roomlist[1]))
                # linklist.nodeadd(Node(False, people=room.roomlist[2]))
                linkitem.append(linklist)


        # for i in linkitem:
        #     i.show_all()

class Node:

    def __init__(self, seq, people=None, next=None):
        self.seq = seq
        self._next = next
        self._people = people

    def getname(self):
        return self._people

    def getNext(self):
        return self._next

    def setname(self, new_people):
        self._people = new_people

    def setNext(self, new_next):
        self._next = new_next

class Linklist:

    def __init__(self):
        self.node = Node(True)

    def nodeadd(self, node):
        if self.node._next == None:
            self.node.setNext(node)
            return
        else:
            currentnode = self.node
            while currentnode._next is not None:
                currentnode = currentnode._next
            log.info(f"current seq is {currentnode.seq}")
            currentnode.setNext(node)

    def initvaluelist(self):
        self.value_list = []
        currentnode = self.node._next
        while currentnode is not None:
            self.value_list.append(currentnode.seq)
            currentnode = currentnode._next


    @property
    def last_value(self):
        if not self.value_list:
            return None
        if self.value_list > 2:
            if self.value_list[len(self.value_list)-1] == False:
                return self.value_list[len(self.value_list)-2]
            else:
                return self.value_list[len(self.value_list)-1]


    @property
    def linkstatus(self):
        if not self.value_list:
            return True
        if len(self.value_list) >= 3:
            if self.value_list == False and self.value_list[len(self.value_list-2)] == False:
                return False
        return True


    def get_length(self):
        length = 1
        currentnode = self.node._next
        while currentnode is not None:
            length += 1
            currentnode = currentnode._next
        return length

    def show_all(self):
        currentnode = self.node._next
        while currentnode is not None:
            log.info("current people is " + currentnode._people.name + " the input is " + currentnode.seq)

            currentnode = currentnode._next


if __name__ == "__main__":
    # a = Container()
    # eval("a.run()")

    index = 0
    roomitem = []
    while index < 10:
        input_str = input()
        try:
            result = input_str.split()
            if result[0] not in commandlist:
                raise Exception("the input don't obey the rules")

            if result[0] == "createuser":
                if len(result) != 2:
                    raise Exception("createuser only need a param, please try again")
                people = People(result[1])
                log.info(f"now people's name is {people.name}, and now status is {people.ready_status}")

            elif result[0] == "createroom":
                if len(result) != 2:
                    raise Exception("createroom only need a param, please try again")
                nowroom = RoomItem(result[1])
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
                            log.info(f"now people's name is {people.name}, and now status is {people.ready_status}, now room status ")
                            findroom = True
                    if findroom == False:
                        raise Exception("the room isn't exist, please create room")
                else:
                    raise Exception("there isn't any user, please create")

            elif result[0] == "ready":
                if people:
                    log.info(f"now people's name is {people.name}, and now status is {people.ready_status}")
                    people.ready_status = True
                else:
                    raise Exception("there isn't any user, please create")

            elif result[0] == "help":
                if len(result) != 1:
                    raise Exception("help cmd doesn't need any param")
                for keys in commanddict.keys():
                    log.debug(f" {keys} : {commanddict[keys]}")


        except Exception as e:
            log.error(e)



