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

#A clean answear
##num = int(raw_input('Insert a number: '))
##a = [x for x in range(2, num) if num % x == 0]
##
##
##def is_prime(n):
##	if num > 1:
##		if len(a) == 0:
##			print 'prime'
##		else:
##			print 'NOT prime'
##	else:
##		print 'NOT prime'
##
##
##is_prime(num)


#and the answer:
#def get_number(prompt):
#	'''Returns integer value for input. Prompt is displayed text'''
#	return int(input(prompt))


#def is_prime(number):
#	'''Returns True for prime numbers, False otherwise'''
#	# Edge Cases
#	if number == 1:
#		prime = False
#	elif number == 2:
#		prime = True
#	# All other primes
#	else:
#		prime = True
#		for check_number in range(2, (number / 2) + 1):
#			if number % check_number == 0:
#				prime = False
#				break
#	return prime


#def print_prime(number):
#	prime = is_prime(number)
#	if prime:
#		descriptor = ""
#	else:
#		descriptor = "not "
#	print(number, " is ", descriptor, "prime.", sep = "", end = "\n\n")
##sep and end are python3 command.


# never ending loop

#while 1 == 1:
#	print_prime(get_number("Enter a number to check. Ctl-C to exit."))
#
#https://www.practicepython.org/exercise/2014/04/16/11-check-primality-functions.html