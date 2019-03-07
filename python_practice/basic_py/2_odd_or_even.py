num = raw_input("please reinput your number: ")
if (int(num) % 2 == 0):
	if(int(num)%4 ==0):
		print( str(num) + " is a multiple of 4")
	else:
		print ( str(num) + " is even")
else:
	print (str(num) + " is odd")

