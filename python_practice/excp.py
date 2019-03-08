try:
	x = input('enter the first number: ')
	y = input('enter the second number: ')
	print x/y
except ZeroDivisionError:
	print "the second number can't be zero!"
