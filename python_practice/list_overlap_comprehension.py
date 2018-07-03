__author__ = '3tral'
a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
c = [i for i in a for x in b if i == x ]
print(c)
#it's better to use f, actually c == f
f = [i for i in a if i in b]
print(f)
d = []
#filter the extra 1 in list c
e = [d.append(i) for i in c if i not in d]

print(d)
print(e)

#extra
import random

l1 = random.sample(range(1,100), random.randint(1,10))
l2 = random.sample(range(1,100), random.randint(1,10))
print(l1)
print(l2)
fl1 = [ i for i in l1 if i in l2]
print(fl1)
fl2 = []
fl3 = [fl2.append(i) for i in fl1 if i not in fl2]
print(fl2)
print(fl3)
#https://www.practicepython.org/exercise/2014/04/10/10-list-overlap-comprehensions.html