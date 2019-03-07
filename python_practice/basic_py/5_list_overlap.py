__author__ = '3tral'
a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
print a
print b
l1 = []
for i in a:
	if i in b:
		l1.append(i)
print l1

#extra-1
import random
a = random.sample(range(1,100), 10)
print a
b = random.sample(range(1,100), 10)
print b
commonList = set()
[commonList.add(x)for x in a for y in b if x == y]
print(list(commonList))

#https://www.practicepython.org/exercise/2014/03/05/05-list-overlap.html