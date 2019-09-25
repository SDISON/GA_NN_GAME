#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 14:03:48 2019

@author: root
"""
import random
import math
class simulated:
    def __init__(self):
        self.board = 6
        self.intial = [i for i in range(0,self.board)]
        self.energy = self.evaluate(self.intial)
        self.temp = 100
        self.rate = 0.1
        self.temp_lim=0.5
    def evaluate(self,temp):
        summ=0
        for i in range(0,self.board):    
            for j in range(i+1,self.board):
                if (self.intial[j]-self.intial[i])==(j-i):
                    summ+=1
                elif (self.intial[j]-self.intial[i])==-(j-i):
                    summ+=1
        return summ
    def loop(self):
        temp = self.intial
        random.shuffle(temp)
        tmp = self.evaluate(temp)
        if tmp<self.energy:
            self.energy=tmp
            self.intial=temp
        elif math.exp((self.energy-tmp)/self.temp) > random.random():
            self.energy=tmp
            self.intial=temp
        self.temp-=self.rate*self.temp
    def end(self):
        if self.energy==0:
            return 1
        return 0

obj=simulated()
i=1
while(obj.temp>obj.temp_lim):
    print((obj.intial),obj.energy)
    if obj.end()==1:
        break
    obj.loop()
    i+=1
    
        
        
