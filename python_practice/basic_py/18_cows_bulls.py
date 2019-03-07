__author__ = '3tral'
import random
Rightvalue = random.randint(1000,9999)
print(Rightvalue)

counter = 0

def urinput():
	userValue = input("please input a 4-digits number\n")
	return userValue

def asser1(r1, r2):


	l1 =list(str(r1))
	l2 =list(str(r2))
	l3 =[]
	cowCounter = 0
	bull = [i for i in l2 for x in l1 if i == x]
	e = [l3.append(i) for i in bull if i not in l3]
	bullCounter = len(l3)
	for i in range(0,4):
		if l2[i] == l1[i]:
			cowCounter += 1
	if cowCounter > 0:
		bullCounter = bullCounter - cowCounter
	print(cowCounter, bullCounter)
	return cowCounter, bullCounter
def asser2():
	global counter
	l1=[]

	counter = counter +1

	l1=asser1(Rightvalue, urinput())

	if l1[0] != 4:

		print('guessed %s time(s), guess again\n' %counter)
		asser2()
	elif l1[0] == 4:
		print('bingo!')
if __name__ == "__main__":

	asser2()


#https://www.practicepython.org/exercise/2014/07/05/18-cows-and-bulls.html