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

#official answer: just like my answer
#def gen_fib():
#	count = int(raw_input("how many fibonacci numbers would you like to generate?"))
#	i = 1
#	if count == 0:
#		fib[]
#	elif count == 1:
#		fib = [1]
#	elif count == 2:
#		fib = [1, 1]
#	elif count > 2:
#		fib = [1,1]
#		while i < (count - 1):
#			fib.append(fib[i] + fib[i-1])
#			i +=1
#	return fib
#https://www.practicepython.org/exercise/2014/04/30/13-fibonacci.html