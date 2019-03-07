__author__ = '3tral'
import random
l1 = random.sample(range(1,1000), random.randint(10,20))
print(l1)
l2 = [1,2,3,4,5,6,7]

i = input("input a number:\n")
print('ha')
if i not in l1:
	print('bingo')
else:
	print('cao')

if i in l2:
	print('ainiyo')
else:
	print('qunima')