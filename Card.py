# -*- coding: utf-8 -*-

"""
@author: lan

@contact: 

@Created on: 2022/5/25 21:56
"""
class Config:
    priority = {
        '3': 1,
        '4': 2,
        '5': 3,
        '6': 4,
        '7': 5,
        '8': 6,
        '9': 7,
        '10': 8,
        'J': 9,
        'Q': 10,
        'K': 11,
        'A': 12,
        '2': 13,
        'smallking': 14,
        'bigking': 15
    }



class Card:
    #初始化类,包含所有卡片
    def __init__(self):
        self.basecard = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] * 4
        self.kingcard = ['smallking', 'bigking']



if __name__ == "__main__":
    a = Card()
    print(a.basecard)