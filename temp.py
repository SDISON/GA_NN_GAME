import random

arr = [[0 for i in range(10)] for j in range(10)]
        
for i in range(10):
    for j in range(10):
        arr[i][j] = random.randint(1,2)*random.randint(1, 100)

li = [[0,1,2,3,4,6,7,9,8,5]]
for i in range(20):
    temp = li[0][:]
    random.shuffle(temp)
    li.append(temp)
    
li2=[]
for i in li:
    summ=0
    for j in range(9):
        if(arr[i[j]][i[j+1]]==0):
            summ=1e18
            continue
        else:
            summ+=arr[i[j]][i[j+1]]
    li2.append(summ)

total = sum(li2)
for i in range(len(li2)):
    li2[i] = round(float(li2[i])/total, 4)
    
di = {}
for i in range(len(li2)):
    di[i]=li2[i]


