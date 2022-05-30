# -*- coding: utf-8 -*-

"""
@author: lan

@contact: 

@Created on: 2022/5/25 21:58
"""
from Card import *

class SeqType:

    SINGLE = "single" # 单牌
    GROUP = "group" # 对子
    TRIPLE = "triple" # 3个一样、3带1、三带2
    SEQUENCE = "sequence" # 顺子
    BOOM = "boom" # 炸弹
    SEQGROUP = "seqgroup" # 连对

    @classmethod
    def is_group(cls, sequenctlist):
        if len(sequenctlist) == 2 :
            if sequenctlist[0] == sequenctlist[1]:
                return True

    @classmethod
    def is_triple(cls, sequenctlist):
        if len(sequenctlist) == 3:
            if len(set(sequenctlist)) == 1:
                return True
        elif len(sequenctlist) == 4 or len(sequenctlist) == 5:
            count = {}
            for i in sequenctlist:
                if i not in count.keys():
                    count[i] = 1
                else:
                    count[i] += 1
            for j in count.keys():
                if count[j] == 3:
                    return True

    @classmethod
    def is_sequence(cls, sequenctlist):
        if len(sequenctlist) >= 5 and len(sequenctlist) <= 13:
            if len(set(sequenctlist)) == len(sequenctlist):
                if max(sequenctlist) - min(sequenctlist) == len(sequenctlist) - 1:
                    return True

    @classmethod
    def is_boom(cls, sequenctlist):
        if len(sequenctlist) == 4:
            if len(set(sequenctlist)) == 1:
                return True
        elif len(sequenctlist) == 2 and "smallking" in sequenctlist and "bigking" in sequenctlist:
            return True

    @classmethod
    def is_seqgroup(cls, sequenctlist):
        if len(sequenctlist) >= 6 and len(sequenctlist) % 2 == 0:
            if len(set(sequenctlist)) == int(len(sequenctlist)/2):
                if (max(sequenctlist) - min(sequenctlist)) == len(set(sequenctlist))-1:
                    return True

class Rule:
    """
    判断当前类别
    """

    def __init__(self, sequence):
        self.sequencelist = sequence.split()
        self.targetlist = [Config.priority[i] for i in self.sequencelist]

    @property
    def seqtype(self):
        '''
        :return: 返回输入类型
        '''
        if len(self.targetlist) == 1:
            return SeqType.SINGLE
        if SeqType.is_group(self.targetlist):
            return SeqType.GROUP
        if SeqType.is_triple(self.targetlist):
            return SeqType.TRIPLE
        if SeqType.is_boom(self.targetlist):
            return SeqType.BOOM
        if SeqType.is_sequence(self.targetlist):
            return SeqType.SEQUENCE
        if SeqType.is_seqgroup(self.targetlist):
            return SeqType.SEQGROUP
        raise Exception("The input don't obey the rules")

    def playcard(self, clazz):
        '''
        :param clazz:
        :return:
        '''
        if self.seqtype == clazz.seqtype:
            if min(self.targetlist) > min(clazz.targetlist):
                return True
        elif self.seqtype == 'boom':
            return True
        raise Exception("The input don't obey the rules, please try again")


    def giveup(self):
        return False



if __name__ == "__main__":
    a = Rule("3 3 3 3 ")
    b = Rule("4 4 5 5 6 6")
    print(a.playcard(b))