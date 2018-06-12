__author__ = '3tral'
def getnum():
	num = int(raw_input("please give a number of numbers for Fibonacci:(should more than 1)\n"))
	return num

def fibonacci(nums):
	a = [1, 1]
	if nums == 2:
		print a
	elif nums > 2:
		for i in range(2, nums):
			c = a[i-1] + a[i-2]
			a.append(c)
		print a
	else:
		print "please input a right number"
		fibonacci(getnum())

fibonacci(getnum())

#https://www.practicepython.org/exercise/2014/04/30/13-fibonacci.html