#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 18 10:23:35 2019

@author: root
"""
import random
import string
class gene:
    def __init__(self):
        self.gene_material=string.ascii_lowercase + ' '

class chromosome:
    def __init__(self,size):
        self.size=size
        self.li=[]
    def create(self):
        self.li=[random.choice(gene().gene_material) for i in range(self.size)]
        return self.li

class fitness:
    def __init__(self):
        self.fit_score=0
    def calculate_function(self,compareTo,compareFrom):
        for i in range(len(compareTo)):
            if compareTo[i]==compareFrom[i]:
                self.fit_score+=1
        return (self.fit_score)/len(compareTo)

class mating_pool:
    def __init__(self):
        self.element=[]
    def fill(self,chromosome):
        (self.element).append(chromosome)

class genetic:
    def __init__(self):
        self.pop_size=100
        self.target='beauty is just a word you define it better'
    def creation(self):
        self.pop_element = [((chromosome(len(self.target))).create()) for i in range(self.pop_size)]
    def evaluate(self):
        self.pop_score=[(fitness()).calculate_function(i,self.target) for i in self.pop_element]    
    def selection(self):
        self.pool=mating_pool()
        for i in range(10000):
            pos=random.randint(0,self.pop_size-1)
            if((self.pop_score[pos])>=random.random()):
                (self.pool).fill(self.pop_element[pos])
    def crossover(self):
        self.new_pop_element=[]
        for i in range(len(self.pool.element)):
            i1=random.randint(0,len(self.pool.element)-1)
            i2=random.randint(0,len(self.pool.element)-1)
            temp1=[]
            temp2=[]
            for j in range(len(self.target)):
                if (self.pool.element[i1])[j]==self.target[j]:
                    temp1.append(self.target[j])
                    temp2.append(self.target[j])
                elif (self.pool.element[i2])[j]==self.target[j]:
                    temp1.append(self.target[j])
                    temp2.append(self.target[j])
                else:
                    temp1.append((self.pool.element[i1])[j])
                    temp2.append((self.pool.element[i1])[j])
            self.new_pop_element.append(temp1)
            self.new_pop_element.append(temp2)
    def mutation(self):
        for i in self.new_pop_element:
            i[random.randint(0,len(i)-1)]=random.choice(gene().gene_material)

obj=genetic()
obj.creation()
for i in range(1000):
    obj.evaluate()
    try:
        if (obj.pop_score).index(1.0):
            print(''.join(obj.pop_element[(obj.pop_score).index(max(obj.pop_score))]))
            break
    except:
        print(''.join(obj.pop_element[(obj.pop_score).index(max(obj.pop_score))]))
    obj.selection()
    obj.crossover()
    obj.mutation()
    obj.pop_element=obj.new_pop_element