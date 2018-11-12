list1= [1,0.5,1,0.25,0.5 ]
list2 = [2,1,1,0.5,2]
list3 = [1,1,1,0.5,2]
list4 = [4,2,2,1,2]
list5 = [2,0.5,0.5,0.5,1]
get_sum1=sum(list1)
get_sum2 = sum(list2)
get_sum3 = sum(list3)
get_sum4 = sum(list4)
get_sum5 = sum(list5)
for i in range(len(list1)):
    list1[i] = float(list1[i]/get_sum1)
for i in range(len(list2)):
    list2[i] = float(list2[i]/get_sum2)
for i in range(len(list3)):
    list3[i] = float(list3[i]/get_sum3)
for i in range(len(list4)):
    list4[i] = float(list4[i]/get_sum4)
for i in range(len(list5)):
    list5[i] = float(list5[i]/get_sum5)
print(list1)
print(list2)
print(list3)
print(list4)
print(list5)


