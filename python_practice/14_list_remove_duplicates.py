__author__ = '3tral'
def noduplist():
	a = [1, 2, 2, 3, 3, 3]
	print list(set(a))
noduplist()

#extra1
def loopnodup():
	a = [1, 1, 1, 55, 55, 55,'cuihua']
	b =[]
	for i in a:
		if i not in b:
			b.append(i)
	print b
loopnodup()

#extral2
def listoverlap():
     a = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
     b = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
     c =[i for i in a for x in b if i==x]
     print list(set(c))
listoverlap()

#answer:
##def dedupe_v1(x):
##  y = []
##  for i in x:
##    if i not in y:
##      y.append(i)
##  return y
##
###this one uses sets
##def dedupe_v2(x):
##    return list(set(x))
##
##a = [1,2,3,4,3,2,1]
##print a
##print dedupe_v1(a)
##print dedupe_v2(a)

#https://www.practicepython.org/exercise/2014/05/15/14-list-remove-duplicates.html