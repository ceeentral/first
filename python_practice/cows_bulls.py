__author__ = '3tral'
import random
def asser():

	Rightvalue = random.randint(1000,9999)
	print(Rightvalue)
	l1 = list(str(Rightvalue))
	print(l1)
	userValue = urinput()
	l2 = list(str(userValue))
	guesstimeC = 0
	cowCounter = 0
	bullCounter = 0
	cc = [i for i in l2 for x in l1 if i == x]
	bullCounter = len(cc)
	for i in range(0,4):
		if l2[i] == l1[i]:
			cowCounter+=1
	if cowCounter > 0:
		bullCounter = bullCounter - cowCounter
	print('cow:' + str(cowCounter) + ' bull:' + str(bullCounter))
	if cowCounter != 4:
		aaa

def urinput():
	userValue = input("please input a 4-digits number\n")
	return userValue
def rannum():
	Rightvalue = random.randint(1000,9999)
	print(Rightvalue)
	return Rightvalue

def asser1(r1, r2):
	l1 =list(str(r1))
	l2 =list(str(r2))
	l3 =[]
	cowCounter = 0
	bull = [i for i in l2 for x in l1 if 1 == x]
	e = [l3.append[i] for i in bull if i not in l3]
	bullCounter = len(l3)
	for i in range(0,4):
		if l2[i] == l1[i]:
			cowCounter += 1
	if cowCounter > 0:
		bullCounter = bullCounter - cowCounter
	print(cowCounter, bullCounter)
	return cowCounter, bullCounter
if __name__ == "__main__":
	l1=[]
	l1=asser1(rannum(),urinput())
	if l1[0] != 4:
		print('aaa')
	print(l1)


#https://www.practicepython.org/exercise/2014/07/05/18-cows-and-bulls.html