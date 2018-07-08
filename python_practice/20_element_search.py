__author__ = '3tral'
import random
l1 = random.sample(range(1,1000), random.randint(10,20))
l1.sort()
print(l1)
usrnm = int(input("please input a number that you want to guess:\n"))
midd = l1[int(len(l1) / 2)]


def asser():
	if usrnm < midd:
		for i in l1[0:int(len(l1) / 2)]:
			if usrnm == i:
				value = True
				break
			else:
				value = False
	else:
		for i in l1[int(len(l1) / 2):]:
			if usrnm == i:
				value = True
				break
			else:
				value = False
	return value
#while asser():
#
#	print("bingo, %s is in the list" %usrnm)
#	break
#else:
#	print("%s is not in the list" %usrnm)

#最后终于明白了binary search是什么意思
#意思是2分法来找这个数字，看中间那个数字是不是，然后不是的话再找其一半
def binsearch():
	global l1
	midd = l1[int(len(l1) / 2)]
	if usrnm < midd:
		l1 = l1[0:int(len(l1) / 2)]
	else:
		l1 = l1[int(len(l1) / 2):]
	return l1
def panduan():
	counter =0
	if usrnm != midd:
		binsearch()
		panduan()
	else:
		print('bingo')

#https://www.practicepython.org/exercise/2014/11/11/20-element-search.html