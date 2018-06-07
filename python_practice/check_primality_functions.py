__author__ = '3tral'

num = raw_input('please input a number:\n')
if num.isdigit():
	l1 = []
	for i in range(2, int(num)):
		if int(num) % i == 0 :
			l1.append(i)
	
	if l1 == []:
		print (str(num) + " is a prime number!")
	else:
		print (str(num) + " is NOT a prime number!")
else:
	print "we need a number!"



#https://www.practicepython.org/exercise/2014/04/16/11-check-primality-functions.html